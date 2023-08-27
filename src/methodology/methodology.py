import os

from pylatex import Command, Subsection


def create_methodology():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    methodology = Subsection("Methodology", numbering=False)
    methodology.append(Command("input", "methodology/metrics"))

    with open(os.path.join(current_directory, "methodology.tex"), "w") as f:
        f.write(methodology.dumps())
