from pylatex import Document, Command, NoEscape, Package

from introduction.introduction import create_introduction


def main():
    doc = Document(documentclass="report")

    doc.preamble.append(Package("amsmath"))
    doc.preamble.append(Package("amssymb"))
    doc.preamble.append(Package("indentfirst"))


    doc.append(NoEscape(r"\renewcommand\bibname{References}"))

    doc.preamble.append(Command("title", "Master thesis proposal"))
    doc.preamble.append(Command("author", "Viktor Todosijevic"))
    doc.preamble.append(Command("date", "August 2023"))
    doc.append(NoEscape(r"\maketitle"))

    doc.append(NoEscape(r"This is a reference to an equation~\ref{eq:four}"))
    doc.append(Command("input", "equation/equation"))

    create_introduction()
    doc.append(Command("input", "introduction/introduction"))

    doc.append(Command("bibliography", "main"))
    doc.append(Command("bibliographystyle", "plain"))

    with open("main.tex", "w") as f:
        f.write(doc.dumps())


if __name__ == "__main__":
    main()
