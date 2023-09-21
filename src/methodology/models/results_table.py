from typing import Callable, List, Tuple

import copy
import os.path
import wandb

import numpy as np

from dataclasses import dataclass
from numpy.typing import NDArray
from pylatex import Table, Tabular, NoEscape, Label, Marker
from pylatex.utils import bold

from methodology.metrics.metrics import math


def sci_notation(number, sig_fig=2):
    ret_string = "{0:.{1:d}e}".format(number, sig_fig)
    a, b = ret_string.split("e")
    # remove leading "+" and strip leading zeros
    b = int(b)
    if b == 0:
        return f"{a}"

    # return a + " * 10^" + str(b)
    return rf"{a} \cdot 10^{{{str(b)}}}"


def results_tabular(header: List[str],
                    metric_symbols: List[str],
                    table_contents: NDArray,
                    table_contents_mask: NDArray,
                    num_decimals: int) -> Tabular:
    tabular = Tabular("|" + "".join("c|" for _ in range(len(header))))
    tabular.add_hline()
    tabular.add_row(*header)
    tabular.add_hline()

    for i in range(len(metric_symbols)):
        contents = [sci_notation(table_contents[i, j], sig_fig=num_decimals) for j in range(table_contents.shape[1])]
        for j in range(len(contents)):
            if table_contents_mask[i, j]:  # contents[j] = bold(contents[j])

                contents[j] = rf"\boldsymbol{{{contents[j]}}}"

        tabular.add_row(NoEscape(metric_symbols[i]), *[NoEscape(math(content)) for content in contents])
        tabular.add_hline()

    # table = Table(position="H")
    # # table.append(NoEscape(r'\centering'))
    # table.append(NoEscape(r"\begin{center}"))
    # table.append(NoEscape(rf"\scalebox{{{scale}}}{{"))
    #
    # table.append(tabular)
    # table.append(NoEscape(r"}"))
    #
    # table.append(NoEscape(r"\end{center}"))
    #
    # table.add_caption(caption)
    # table.append(Label(marker))

    return tabular


@dataclass
class SweepInfo:
    model_name: str
    sweep_id: str
    best_run_id: str = None


@dataclass
class Metric:
    key: str
    symbol: str
    value: float = None
    compare_func: Callable = min
    run_id: str = None

    def compare(self, other: float) -> bool:
        """
        Return true if other is better than self as defined by the self.compare_func.
        :param other: Value.
        :return: Boolean.
        """
        if self.compare_func(self.value, other) == other:
            return True

        return False

    def mean(self):
        new_metric = copy.deepcopy(self)

        new_metric.key = f"mean {new_metric.key}"
        new_metric.symbol = new_metric.symbol.replace("$", "")
        new_metric.symbol = math(rf"\overline{{{new_metric.symbol}}}")

        return new_metric

    def worst_case(self):
        new_metric = copy.deepcopy(self)
        if new_metric.compare_func == min:
            key_prefix = "max"
        elif new_metric.compare_func == max:
            key_prefix = "min"
        else:
            raise ValueError(f"Compare function '{new_metric.compare_func}' not supported.")

        new_metric.key = f"{key_prefix} {new_metric.key}"
        new_metric.symbol = new_metric.symbol.replace("$", "")
        new_metric.symbol = math(rf"\{key_prefix}{{{new_metric.symbol}}}")

        return new_metric


def wandb_path(path: str, id_: str) -> str:
    return os.path.join(path, id_).replace("\\", "/")


def get_contents(path: str,
                 sweeps_infos: List[SweepInfo],
                 metric_dir: str,
                 main_metric: Metric,
                 metrics: List[Metric]) -> Tuple[NDArray, ...]:
    api = wandb.Api()

    for sweep_info in sweeps_infos:
        sweep = api.sweep(wandb_path(path, sweep_info.sweep_id))

        best_metric = copy.deepcopy(main_metric)  # metric to choose run in sweep

        get_best_run(sweep, best_metric, metric_dir, MetricFilter(name="r2 score", value=0.95, comparison="g"))

        if best_metric.run_id is None:
            get_best_run(sweep, best_metric, metric_dir)

        sweep_info.best_run_id = best_metric.run_id

    table_contents = np.zeros((len(metrics), len(sweeps_infos)), dtype=float)

    # fill the content table with metric values (rows-metrics; columns-models)
    for j in range(len(sweeps_infos)):
        run = api.run(wandb_path(path, sweeps_infos[j].best_run_id))
        for i in range(len(metrics)):
            table_contents[i, j] = run.summary[metric_dir + metrics[i].key]

    table_contents_mask = np.zeros_like(table_contents, dtype=bool)

    # mark the best value in each row
    for i in range(len(metrics)):

        if metrics[i].compare_func == max:
            column_idx = np.argwhere(table_contents[i, :] == np.amax(table_contents[i, :]))
        elif metrics[i].compare_func == min:
            column_idx = np.argwhere(table_contents[i, :] == np.amin(table_contents[i, :]))
        else:
            raise ValueError(f"{metrics[i].compare_func} not supported. Expected [min, max]")

        table_contents_mask[i, column_idx] = True

    return table_contents, table_contents_mask


@dataclass
class MetricFilter:
    name: str
    value: float
    comparison: str

    def compare(self, other_value: float):

        if self.comparison == "g":
            return other_value > self.value

        if self.comparison == "l":
            return other_value < self.value

        if self.comparison == "ge":
            return other_value >= self.value

        if self.comparison == "le":
            return other_value <= self.value


def get_best_run(sweep, best_metric: Metric, metric_dir: str, metric_filter: MetricFilter = None):
    for run in sweep.runs:
        if run.state == "failed":
            continue

        current_run_metric = run.summary[best_metric.key]

        if metric_filter is None or metric_filter.compare(run.summary[metric_dir + metric_filter.name]):
            # compare and keep the better one
            if best_metric.value is None:
                best_metric.value = current_run_metric
                best_metric.run_id = run.id
            else:
                if best_metric.compare(current_run_metric):
                    best_metric.value = current_run_metric
                    best_metric.run_id = run.id
