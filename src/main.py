from pylatex import Document, Command, NoEscape, Package, Subsection

from introduction.introduction import create_introduction
from methodology.methodology import create_methodology


def main():
    doc = Document(documentclass="report")

    doc.preamble.append(Package("amsmath"))
    doc.preamble.append(Package("amssymb"))
    doc.preamble.append(Package("float"))
    doc.preamble.append(Package("indentfirst"))
    doc.preamble.append(Package("makecell"))
    doc.preamble.append(NoEscape(r"\setcellgapes{5pt}"))
    doc.preamble.append(NoEscape(r"\makegapedcells"))

    doc.append(NoEscape(r"\renewcommand\bibname{References}"))

    doc.preamble.append(Command("title", "Master thesis proposal"))
    doc.preamble.append(Command("author", "Viktor Todosijevic"))
    doc.preamble.append(Command("date", "August 2023"))
    doc.append(NoEscape(r"\maketitle"))

    doc.append(NoEscape(r"This is a reference to an equation~\ref{eq:four}"))
    doc.append(Command("input", "equation/equation"))

    create_introduction()
    doc.append(Command("input", "introduction/introduction"))

    literature_overview = Subsection("Overview of the literature", numbering=False)
    literature_overview.append(Command("input", "literature_overview/literature_overview"))
    doc.append(literature_overview)

    create_methodology()
    doc.append(Command("input", "methodology/methodology"))

    doc.append(Command("bibliography", "main"))
    doc.append(Command("bibliographystyle", "plain"))

    with open("main.tex", "w") as f:
        f.write(doc.dumps())


if __name__ == "__main__":
    main()
