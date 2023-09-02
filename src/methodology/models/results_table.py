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


def results_table(header: List[str],
                  metric_symbols: List[str],
                  table_contents: NDArray,
                  table_contents_mask: NDArray,
                  caption: str,
                  marker: Marker) -> Table:
    tabular = Tabular("|" + "".join("c|" for _ in range(len(header))))
    tabular.add_hline()
    tabular.add_row(*header)
    tabular.add_hline()

    for i in range(len(metric_symbols)):
        tabular.add_row(
            NoEscape(metric_symbols[i]),
            *[bold(table_contents[i, j]) if table_contents_mask[i, j] else table_contents[i, j] for j in range(table_contents.shape[1])]
        )
        tabular.add_hline()

    table = Table(position="H")
    table.append(NoEscape(r'\centering'))
    table.append(tabular)
    table.add_caption(caption)
    table.append(Label(marker))

    return table


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


def wandb_path(path: str, id_: str) -> str:
    return os.path.join(path, id_).replace("\\", "/")


def get_contents(path: str,
                 sweeps_infos: List[SweepInfo],
                 metric_dir: str,
                 main_metric: Metric,
                 metrics: List[Metric]) -> Tuple[NDArray, ...]:
    api = wandb.Api()

    for metric in metrics:
        metric.key = metric_dir + metric.key

    for sweep_info in sweeps_infos:
        sweep = api.sweep(wandb_path(path, sweep_info.sweep_id))

        best_metric = copy.deepcopy(main_metric)  # metric to choose run in sweep

        for run in sweep.runs:
            if run.state == "failed":
                continue

            current_run_metric = run.summary[best_metric.key]

            # TODO could incorporate custom filters
            if run.summary[metric_dir + "r2 score"] > 0.75:  # filter by R2 score cause the pf errors can be low without anything being learned
                # compare and keep the better one
                if best_metric.value is None:
                    best_metric.value = current_run_metric
                    best_metric.run_id = run.id
                else:
                    if best_metric.compare(current_run_metric):
                        best_metric.value = current_run_metric
                        best_metric.run_id = run.id

        sweep_info.best_run_id = best_metric.run_id

    table_contents = np.zeros((len(metrics), len(sweeps_infos)), dtype=float)

    # fill the content table with metric values (rows-metrics; columns-models)
    for j in range(len(sweeps_infos)):
        run = api.run(wandb_path(path, sweeps_infos[j].best_run_id))
        for i in range(len(metrics)):
            table_contents[i, j] = run.summary[metrics[i].key]

    table_contents_mask = np.zeros_like(table_contents, dtype=bool)

    # mark the best value in each row
    for i in range(len(metrics)):
        if metrics[i].compare_func == max:
            column_idx = np.argmax(table_contents[i, :], axis=0)
        elif metrics[i].compare_func == min:
            column_idx = np.argmin(table_contents[i, :], axis=0)
        else:
            raise ValueError(f"{metrics[i].compare_func} not supported. Expected [min, max]")

        table_contents_mask[i, column_idx] = True

    return table_contents, table_contents_mask


def create_results_table() -> Table:
    path = "thesis-proposal"

    sweep_infos = [
        SweepInfo(model_name="GCN", sweep_id="r4ised6c"),
        SweepInfo(model_name="GCN-JK", sweep_id="ur539u0i"),

    ]

    metric_dir = "val/"

    num_decimals = 3

    # which metrics to fetch
    metrics = [
        Metric(key="r2 score", symbol=math("R^2"), compare_func=max),
        Metric(key="mean relative active power error [ratio]", symbol=math(r"\overline{\relativeabsoluteerror{P}}")),
        Metric(key="mean relative reactive power error [ratio]", symbol=math(r"\overline{\relativeabsoluteerror{Q}}"))
    ]

    main_metric = Metric(key=metric_dir + "mean relative active power error [ratio]", symbol="symbol")

    table_contents, table_contents_mask = get_contents(path=path,
                                                       sweeps_infos=sweep_infos,
                                                       metric_dir=metric_dir,
                                                       main_metric=main_metric,
                                                       metrics=metrics)

    table_contents = np.round(table_contents, num_decimals)

    header = ["Metric"] + [sweep_info.model_name for sweep_info in sweep_infos]
    metric_symbols = [metric.symbol for metric in metrics]

    table = results_table(header, metric_symbols, table_contents, table_contents_mask,
                          caption="This is a results table",
                          marker=Marker("results_table_ref", prefix="tab", del_invalid_char=True))

    # print(table.dumps())
    return table


if __name__ == "__main__":
    create_results_table()
