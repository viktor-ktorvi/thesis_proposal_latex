import copy
import os.path
import wandb

from dataclasses import dataclass
from pprint import pprint


def create_results_table():
    pass


@dataclass
class SweepInfo:
    model_name: str
    sweep_id: str


@dataclass
class Metric:
    key: str
    symbol: str
    value: float = None


def main():
    path = "thesis-proposal"

    # model_names = ["GCN", "GCN-JK"]

    sweeps_infos = [
        SweepInfo(model_name="GCN", sweep_id="r4ised6c"),
        SweepInfo(model_name="GCN-JK", sweep_id="ur539u0i"),

    ]

    metric_dir = "val/"

    metrics = [
        Metric(key="mean relative active power error [ratio]", symbol="symbol"),
        Metric(key="mean relative reactive power error [ratio]", symbol="symbol")
    ]

    for metric in metrics:
        metric.key = metric_dir + metric.key
        # metric.key = f"'{metric.key}'"

    api = wandb.Api()

    sweep_metrics = []
    for sweep_info in sweeps_infos:
        sweep = api.sweep(os.path.join(path, sweep_info.sweep_id).replace("\\", "/"))

        best_metrics = copy.deepcopy(metrics)

        for run in sweep.runs:
            if run.state == "failed":
                continue

            for metric in best_metrics:
                if run.summary[metric_dir + "r2 score"] > 0.75:
                    if metric.value is None:
                        metric.value = run.summary[metric.key]
                    else:
                        metric.value = min(metric.value, run.summary[metric.key])

        sweep_metrics.append(best_metrics)

    pprint(sweep_metrics)


if __name__ == "__main__":
    main()
