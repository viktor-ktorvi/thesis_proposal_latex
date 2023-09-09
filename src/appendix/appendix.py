import os

from pylatex import Command
from pylatex.section import Chapter


def create_appendix():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    appendix = Chapter("Appendix", numbering=False, label="appendix")
    appendix.append(Command("input", "appendix/dataset"))
    appendix.append(Command("input", "appendix/model_workflow"))
    appendix.append(Command("input", "appendix/model_diagram"))
    appendix.append(Command("input", "appendix/model_selection"))

    with open(os.path.join(current_directory, "appendix.tex"), "w") as f:
        f.write(appendix.dumps())
