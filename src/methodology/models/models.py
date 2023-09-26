import os
from typing import List

from pylatex import Subsection, Command, NoEscape, Marker, Table, Label
from pylatex.utils import bold

from methodology.metrics.metrics import math
from methodology.models.results_table import SweepInfo, Metric, get_contents, results_tabular


def create_models():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    models = Subsection("Current model results", numbering=False)
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

    # which metrics to fetch
    equality_metrics = [
        Metric(key="relative active power error [ratio]", symbol=math(r"\relativeabsoluteerror{P}")),
        Metric(key="active power error [p.u.]", symbol=math(r"\absoluteerror{P}")),
        Metric(key="relative reactive power error [ratio]", symbol=math(r"\relativeabsoluteerror{Q}")),
        Metric(key="reactive power error [p.u.]", symbol=math(r"\absoluteerror{Q}")),

    ]

    upper_inequality_metrics = [
        Metric(key="upper active power error [p.u.]", symbol=math(r"\uppererror{P}")),
        Metric(key="upper reactive power error [p.u.]", symbol=math(r"\uppererror{Q}")),
        Metric(key="upper voltage error [p.u.]", symbol=math(r"\uppererror{V}")),
    ]

    lower_inequality_metrics = [
        Metric(key="lower active power error [p.u.]", symbol=math(r"\lowererror{P}"), compare_func=max),
        Metric(key="lower reactive power error [p.u.]", symbol=math(r"\lowererror{Q}"), compare_func=max),
        Metric(key="lower voltage error [p.u.]", symbol=math(r"\lowererror{V}"), compare_func=max),
    ]

    objective_function_metrics = [
        Metric(key="active power cost [$ per h]", symbol=math(r"C")),
        Metric(key="relative active power cost [ratio]", symbol=math(r"\relativecost"))
    ]

    main_metric = Metric(key=metric_dir + "mean relative active power error [ratio]", symbol="symbol")

    models.append(create_results_table(
        path,
        sweep_infos,
        metric_dir,
        main_metric,
        [[metric.mean() for metric in equality_metrics],
         [metric.worst_case() for metric in equality_metrics]],
        num_decimals,
        "Equality constraint metrics.",
        Marker("equalityconstraintsresults", prefix="tab", del_invalid_char=True),
        subcaptions=["Mean errors", "Worst case errors"]
    ))

    models.append(create_results_table(
        path,
        sweep_infos,
        metric_dir,
        main_metric,
        [[metric.mean() for metric in upper_inequality_metrics],
         [metric.worst_case() for metric in upper_inequality_metrics],
         [metric.mean() for metric in lower_inequality_metrics],
         [metric.worst_case() for metric in lower_inequality_metrics]
         ],
        num_decimals,
        "Inequality constraint metrics.",
        Marker("inequalityconstraintsresults", prefix="tab", del_invalid_char=True),
        subcaptions=["Mean upper bound errors",
                     "Worst case upper bound errors",
                     "Mean lower bound errors",
                     "Worst case lower bound errors",
                     ]
    ))

    models.append(create_results_table(
        path,
        sweep_infos,
        metric_dir,
        main_metric,
        [[metric.mean() for metric in objective_function_metrics],
         [metric.worst_case() for metric in objective_function_metrics]],
        num_decimals,
        "Objective function metrics.",
        Marker("objectivefunctionresults", prefix="tab", del_invalid_char=True),
        subcaptions=["Mean value", "Worst case value"]
    ))

    with open(os.path.join(current_directory, "models.tex"), "w") as f:
        f.write(models.dumps())


def create_results_subtable(header: List[str], path: str, sweep_infos: List[SweepInfo], metric_dir: str, main_metric: Metric, metrics: List[Metric], num_decimals: int):
    table_contents, table_contents_mask = get_contents(path=path,
                                                       sweeps_infos=sweep_infos,
                                                       metric_dir=metric_dir,
                                                       main_metric=main_metric,
                                                       metrics=metrics)

    metric_symbols = [bold("Metric")] + [NoEscape(metric.symbol) for metric in metrics]

    tabular1 = results_tabular(metric_symbols, header, table_contents.T, table_contents_mask.T,
                               num_decimals=num_decimals)

    return tabular1


def create_results_table(path: str,
                         sweep_infos: List[SweepInfo],
                         metric_dir: str,
                         main_metric: Metric,
                         metrics: List[List[Metric]],
                         num_decimals: int,
                         caption: str,
                         marker: Marker,
                         subcaptions: List[str]):
    header = [sweep_info.model_name for sweep_info in sweep_infos]
    header = [bold(h) for h in header]

    tabulars = [create_results_subtable(header, path, sweep_infos, metric_dir, main_metric, metrics[i], num_decimals) for i in range(len(metrics))]

    table = Table(position="H")
    table.append(NoEscape(r'\centering'))

    for i in range(len(tabulars)):
        table.append(NoEscape(r"{\makegapedcells"))
        table.append(NoEscape(rf"\subfloat[{subcaptions[i]}]{{{tabulars[i].dumps()}}}"))
        table.append(NoEscape(r"}"))
        table.append(Command("quad"))

    table.add_caption(caption)
    table.append(Label(marker))

    return table
