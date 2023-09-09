import os

from pylatex import Command, Subsection, NewPage

from methodology.metrics.metrics import create_metrics
from methodology.models.models import create_models


def create_methodology():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    methodology = Subsection("Methodology", numbering=False)

    methodology.append(Command("input", "methodology/datasets"))

    create_metrics()
    methodology.append(Command("input", "methodology/metrics/metrics"))

    # create_models()
    methodology.append(Command("input", "methodology/models/models"))

    with open(os.path.join(current_directory, "methodology.tex"), "w") as f:
        f.write(methodology.dumps())
