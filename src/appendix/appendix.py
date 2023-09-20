import os

from pylatex import Command, Subsection
from pylatex.section import Chapter


def create_appendix():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    appendix = Chapter("Appendix", numbering=False, label="appendix")
    appendix.append(Command("input", "appendix/dataset"))

    appendix.append(Subsection("Model pipeline", numbering=False))
    appendix.append(Command("input", "appendix/model_diagram"))
    appendix.append(Command("input", "appendix/model_workflow"))
    appendix.append(Command("input", "appendix/linear_local"))
    appendix.append(Command("input", "appendix/gnn"))
    appendix.append(Command("input", "appendix/linear_global"))


    appendix.append(Command("input", "appendix/on_scaling"))

    appendix.append(Command("input", "appendix/model_selection"))

    with open(os.path.join(current_directory, "appendix.tex"), "w") as f:
        f.write(appendix.dumps())
