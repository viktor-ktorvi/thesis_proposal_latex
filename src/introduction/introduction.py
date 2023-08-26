import os

from pylatex import Subsection, Marker, NoEscape, Command, NewLine

from introduction.node_type_masks_table import node_type_mask_table


def create_introduction():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    introduction = Subsection("Introduction", numbering=False)

    introduction.append(NoEscape(r"This is a reference to Table~\ref{tab:nodemasks}"))

    introduction.append(NewLine())
    introduction.append(NewLine())

    introduction.append(Command("input", "introduction/basic_problem_statement"))
    introduction.append(Command("input", "introduction/motivation"))

    introduction.append(NewLine())
    introduction.append(NewLine())

    introduction.append(Command("input", "introduction/mathematical_formulation"))

    introduction.append(NewLine())
    introduction.append(NewLine())

    introduction.append(Command("input", "introduction/about_node_types_and_masks"))

    introduction.append(NewLine())
    introduction.append(NewLine())

    introduction.append(node_type_mask_table(Marker("nodemasks", prefix="tab")))

    introduction.append(Command("input", "introduction/ml_methods"))

    with open(os.path.join(current_directory, "introduction.tex"), "w") as f:
        f.write(introduction.dumps())
