import os
from typing import List

from pylatex import Subsection, Subsubsection, Command, NoEscape, Marker, NewLine, Table, Label
from pylatex.utils import bold

from methodology.metrics.metrics import math
from methodology.models.results_table import SweepInfo, Metric, get_contents, results_tabular


def create_models():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    models = Subsection("Models", numbering=False)
    models.append(Command("input", "methodology/models/current_results"))

    path = "thesis-proposal"

    sweep_infos = [
        SweepInfo(model_name=NoEscape("Linear" + math(r"_{\boldsymbol{local}}")), sweep_id="j1skq9oe"),
        SweepInfo(model_name="GCN", sweep_id="ngnixgvn"),
        SweepInfo(model_name="GCN-JK", sweep_id="0kcut7oo"),
        SweepInfo(model_name=NoEscape("Linear" + math(r"_{\boldsymbol{global}}")), sweep_id="vq6fbtl9")
    ]

    metric_dir = "eval/"

    num_decimals = 2

    # TODO make a unique constant that ties the keys and symbols so that the chance of error is minimized

    # which metrics to fetch
    equality_metrics = [
        Metric(key="relative active power error [ratio]", symbol=math(r"\relativeabsoluteerror{P}")),
        Metric(key="relative reactive power error [ratio]", symbol=math(r"\relativeabsoluteerror{Q}")),

    ]

    inequality_metrics = [
        Metric(key="upper active power error [p.u.]", symbol=math(r"\uppererror{P}")),
        Metric(key="lower active power error [p.u.]", symbol=math(r"\lowererror{P}"), compare_func=max),
        Metric(key="upper reactive power error [p.u.]", symbol=math(r"\uppererror{Q}")),
        Metric(key="lower reactive power error [p.u.]", symbol=math(r"\lowererror{Q}"), compare_func=max),
        Metric(key="upper voltage error [p.u.]", symbol=math(r"\uppererror{V}")),
        Metric(key="lower voltage error [p.u.]", symbol=math(r"\lowererror{V}"), compare_func=max),
    ]

    cost_metrics = [
        Metric(key="relative active power cost [ratio]", symbol=math(r"\relativecost"))
    ]

    mean_equality_metrics = [metric.mean() for metric in equality_metrics]

    main_metric = Metric(key=metric_dir + "mean relative active power error [ratio]", symbol="symbol")

    models.append(create_results_table(path, sweep_infos, metric_dir, main_metric, equality_metrics, num_decimals))

    models.append(Command("input", "methodology/models/models_todo"))

    with open(os.path.join(current_directory, "models.tex"), "w") as f:
        f.write(models.dumps())


def create_results_table(path: str, sweep_infos: List[SweepInfo], metric_dir: str, main_metric: Metric, metrics: List[Metric], num_decimals: int):
    table_contents, table_contents_mask = get_contents(path=path,
                                                       sweeps_infos=sweep_infos,
                                                       metric_dir=metric_dir,
                                                       main_metric=main_metric,
                                                       metrics=metrics)

    header = [sweep_info.model_name for sweep_info in sweep_infos]
    header = [bold(h) for h in header]
    metric_symbols = [bold("Metric")] + [NoEscape(metric.symbol) for metric in metrics]

    tabular1 = results_tabular(metric_symbols, header, table_contents.T, table_contents_mask.T,
                               num_decimals=num_decimals)

    tabular2 = results_tabular(metric_symbols, header, table_contents.T, table_contents_mask.T,
                               num_decimals=num_decimals)

    table = Table(position="H")
    table.append(NoEscape(r'\centering'))

    table.append(NoEscape(rf"\subfloat[Tabular 1]{{{tabular1.dumps()}}}"))
    table.append(Command("quad"))
    table.append(NoEscape(rf"\subfloat[Tabular 2]{{{tabular2.dumps()}}}"))

    table.add_caption("This is a results table")
    table.append(Label(Marker("results_table_ref", prefix="tab", del_invalid_char=True)))

    return table
