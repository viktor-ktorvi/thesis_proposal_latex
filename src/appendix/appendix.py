import os
from typing import List

import numpy as np

from mlpf.data.data import create_pyg_data
from mlpf.data.loading.load_data import load_data
from numpy.typing import NDArray
from pylatex import Command, Subsection, Tabular, Table, NoEscape, Label, Marker, Tabularx
from pylatex.section import Chapter

from methodology.metrics.metrics import math
from methodology.models.results_table import sci_notation


def create_tabular(header: List[str], contents: List[List[str]]):
    tabular = Tabular("|" + "".join("c|" for _ in range(len(header))))
    tabular.add_hline()
    tabular.add_row(*header)
    tabular.add_hline()

    for row in contents:
        tabular.add_row(*row)
        tabular.add_hline()

    return tabular


def create_multitable(tabulars: List[Tabular], subcaptions: List[str], caption: str, marker: Marker):
    table = Table(position="H")
    table.append(NoEscape(r'\centering'))

    for i in range(len(tabulars)):
        tabular = NoEscape(r"\scalebox{0.7}{") + tabulars[i].dumps() + NoEscape(r"}")
        table.append(NoEscape(rf"\subfloat[{subcaptions[i]}]{{{tabular}}}"))
        table.append(Command("quad"))

    table.add_caption(caption)
    table.append(Label(marker))

    return table


def create_contents(contents_array: NDArray, num_decimals: int, mask: NDArray = None, to_color: str = "both") -> List[List[str]]:
    contents: List[List[str]] = []
    for i, row in enumerate(contents_array):
        row_list = []
        for column in row:
            if column == int(column):
                row_list.append(str(int(column)))
            else:
                row_list.append(str(np.round(column, num_decimals)))

        if mask is not None:
            for j in range(len(row_list)):
                if mask[i, j] and to_color in ["ones", "both"]:
                    row_list[j] = NoEscape(r"\cellcolor{blue!25}" + row_list[j])

                if not mask[i, j] and to_color in ["zeros", "both"]:
                    row_list[j] = NoEscape(r"\cellcolor{red!25}" + row_list[j])

        contents.append(row_list)
        # contents.append(list(np.round(row, num_decimals).astype(str)))
        # contents.append([NoEscape(math(sci_notation(num, num_decimals))) for num in row])

    return contents


def create_appendix():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    appendix = Chapter("Appendix", numbering=False, label="appendix")
    appendix.append(Command("input", "appendix/dataset"))

    appendix.append(Subsection("Model pipeline", numbering=False))
    appendix.append(Command("input", "appendix/model_diagram"))

    opf_ppc = load_data("../../mlpf/examples/datasets/solved_opf_ppcs_case30_10k", max_samples=1)[0]
    data = create_pyg_data(ppc=opf_ppc)

    num_decimals = 3

    header = [NoEscape(r"\cellcolor{gray!40}" + h) for h in ["P", "Q", "V", r"$\theta$"]]

    pqva = create_tabular(
        header=header,
        contents=create_contents(data.PQVA_matrix.numpy(), num_decimals=num_decimals, mask=data.PQVA_mask.numpy(), to_color="both")
    )

    pqva_const = create_tabular(
        header=header,
        contents=create_contents(data.PQVA_mask.numpy() * data.PQVA_matrix.numpy(), num_decimals=num_decimals,
                                 mask=data.PQVA_mask.numpy(), to_color="ones")
    )

    pqva_var = create_tabular(
        header=header,
        contents=create_contents(~data.PQVA_mask.numpy() * data.PQVA_matrix.numpy(), num_decimals=num_decimals,
                                 mask=data.PQVA_mask.numpy(), to_color="zeros")
    )

    table = create_multitable([pqva, pqva_const, pqva_var], [NoEscape(r"$\pqva$"), NoEscape(r"$\pqva_{const}$"), NoEscape(r"$\pqva_{var}$")],
                              NoEscape(
                                  r"Data sample example - shown are the $\pqva$, $\pqva_{const}$ and $\pqva_{var}$ of an actual data sample. The cells are colored with respect " +
                                  r"to $\maskconstvar$, with the color \textcolor{blue!75}{blue} representing a constant value and the color " +
                                  r"\textcolor{red!75}{red} representing a variable in the optimization problem."
                              ),
                              Marker("dataexample", prefix="tab"))

    appendix.append(table)

    appendix.append(Command("input", "appendix/model_workflow"))
    appendix.append(Command("input", "appendix/linear_local"))
    appendix.append(Command("input", "appendix/gnn"))
    appendix.append(Command("input", "appendix/linear_global"))

    appendix.append(Command("input", "appendix/on_scaling"))

    appendix.append(Command("input", "appendix/model_selection"))

    with open(os.path.join(current_directory, "appendix.tex"), "w") as f:
        f.write(appendix.dumps())
