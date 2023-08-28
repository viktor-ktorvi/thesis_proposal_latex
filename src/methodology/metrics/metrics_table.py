from pylatex import Table, Tabular, NoEscape, Label, Marker, Command


def create_metrics_table(marker: Marker):
    metric_tabular = Tabular("|c|c|c|")
    metric_tabular.add_hline()
    metric_tabular.add_row("Name", "Mathematical expression", "Unit")
    metric_tabular.add_hline()

    def error(symbol: str) -> str:
        return f"\\Delta {symbol}"

    def absolute(symbol: str) -> str:
        return f"\\left|{symbol}\\right|"

    def relative(symbol: str) -> str:
        return r"\displaystyle" + Command("frac", [NoEscape(error(symbol)), NoEscape(symbol)]).dumps()

    def math(symbol: str) -> str:
        return f"${symbol}$"

    names = [
        "absolute active power error",
        "absolute reactive power error",
        "absolute relative active power error",
        "absolute relative reactive power error",
    ]

    expressions = [
        math(absolute(error("P"))),
        math(absolute(error("Q"))),
        math(absolute(relative("P"))),
        math(absolute(relative("Q")))
    ]

    units = [
        "p.u.",
        "p.u.",
        r"$\cdot$",
        r"$\cdot$"
    ]

    for i in range(len(names)):
        metric_tabular.add_row(names[i], NoEscape(expressions[i]), NoEscape(units[i]))
        metric_tabular.add_hline()

    table = Table(position="h")
    # table.append(NoEscape(r"\renewcommand{\arraystretch}{2}"))
    table.append(NoEscape(r'\centering'))
    table.append(metric_tabular)
    table.add_caption("Proposed metrics.")
    table.append(Label(marker))
    return table
