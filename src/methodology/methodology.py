import os

from pylatex import Command, Subsection, Marker

from methodology.metrics.metrics_table import create_metrics_table


def create_methodology():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    methodology = Subsection("Methodology", numbering=False)
    methodology.append(Command("input", "methodology/metrics"))

    methodology.append(create_metrics_table(Marker("metrictable", prefix="tab")))

    with open(os.path.join(current_directory, "methodology.tex"), "w") as f:
        f.write(methodology.dumps())
