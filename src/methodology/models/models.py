import os

from pylatex import Subsection, Subsubsection, Command, NoEscape, Marker, NewLine


def create_models():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    models = Subsection("Models", numbering=False)
    models.append(Command("input", "methodology/models/current_results"))

    models.append(NewLine())
    models.append(NewLine())

    models.append(Command("input", "methodology/models/models_todo"))

    with open(os.path.join(current_directory, "models.tex"), "w") as f:
        f.write(models.dumps())
