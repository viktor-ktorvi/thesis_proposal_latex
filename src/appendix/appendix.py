import os

from pylatex import Command, Subsection, NewPage

from methodology.metrics.metrics import create_metrics
from methodology.models.models import create_models


def create_appendix():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    methodology = Subsection("Methodology", numbering=False)

    with open(os.path.join(current_directory, "appendix.tex"), "w") as f:
        f.write(methodology.dumps())
