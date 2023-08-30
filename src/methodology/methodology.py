import os

from pylatex import Command, Subsection, NewPage

from methodology.metrics.metrics import create_metrics


def create_methodology():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    methodology = Subsection("Methodology", numbering=False)

    methodology.append(Command("input", "methodology/datasets"))

    create_metrics()
    methodology.append(Command("input", "methodology/metrics/metrics"))

    # methodology.append(NewPage())
    methodology.append(Command("input", "methodology/models"))

    with open(os.path.join(current_directory, "methodology.tex"), "w") as f:
        f.write(methodology.dumps())
