from pylatex import Document, Command, NoEscape, Package, Subsection, Section, NewPage

from appendix.appendix import create_appendix
from introduction.introduction import create_introduction
from methodology.methodology import create_methodology


def main():
    doc = Document(documentclass="report")

    doc.preamble.append(Package("amsmath"))
    doc.preamble.append(Package("amssymb"))
    doc.preamble.append(Package("float"))
    doc.preamble.append(Package("footmisc", options="perpage"))
    doc.preamble.append(Package("graphicx"))
    doc.preamble.append(Package("hyperref"))
    doc.preamble.append(Package("indentfirst"))
    doc.preamble.append(Package("makecell"))
    doc.preamble.append(NoEscape(r"\setcellgapes{5pt}"))
    doc.preamble.append(NoEscape(r"\makegapedcells"))
    doc.preamble.append(Package("subfig"))
    doc.preamble.append(Package("xcolor"))
    doc.preamble.append(Package("circuitikz"))
    doc.preamble.append(Package("yhmath"))

    doc.append(NoEscape(r"\renewcommand\bibname{References}"))

    doc.append(Command("input", "new_commands"))

    doc.preamble.append(Command("title", "Expressive graph neural networks for optimal power flow: a master thesis proposal"))
    doc.preamble.append(Command("author", "Viktor Todosijevic"))
    doc.preamble.append(Command("date", "September 2023"))
    doc.append(NoEscape(r"\maketitle"))

    create_introduction()
    doc.append(Command("input", "introduction/introduction"))
    doc.append(NewPage())

    literature_overview = Section("Overview of the literature", numbering=False)
    literature_overview.append(Command("input", "literature_overview/literature_overview"))
    doc.append(literature_overview)

    doc.append(NewPage())

    # create_methodology()
    doc.append(Command("input", "methodology/methodology"))

    doc.append(NewPage())

    doc.append(Command("input", "conclusion"))

    doc.append(Command("bibliography", "main"))
    doc.append(Command("bibliographystyle", "unsrt"))

    doc.append(NewPage())

    create_appendix()
    doc.append(Command("appendix"))
    doc.append(Command("input", "appendix/appendix"))

    with open("main.tex", "w") as f:
        f.write(doc.dumps())


if __name__ == "__main__":
    main()
