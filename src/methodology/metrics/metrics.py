import os

from pylatex import Subsection, Subsubsection, Command, NoEscape, Marker, NewLine
from methodology.metrics.metrics_table import create_metrics_table, TableEntry


def error(symbol: str) -> str:
    return rf"\Delta {symbol}"


def absolute(symbol: str) -> str:
    return rf"\left|{symbol}\right|"


def maximum(symbol: str) -> str:
    return "max" + math(rf"\left({symbol}\right)")


def minimum(symbol: str) -> str:
    return "min" + math(rf"\left({symbol}\right)")


def frac(a: str, b: str) -> str:
    return r"\displaystyle" + Command("frac", [NoEscape(a), NoEscape(b)]).dumps()


def math(symbol: str) -> str:
    return f"${symbol}$"


math_var = "X"


def create_metrics():
    current_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    metrics = Subsection("Metrics", numbering=False)
    metrics.append(Command("input", "methodology/metrics/metric_commands"))
    metrics.append(Command("input", "methodology/metrics/metrics_with_regards_to"))

    header = ["Name", "Symbol", "Math expression", "Variables", "Unit"]

    equality_constraints = Subsubsection("Equality constrains", numbering=False)
    equality_constraints.append(Command("input", "methodology/metrics/equality_constraints"))

    equality_constraints.append(
        create_metrics_table(
            header=header,
            entries=[
                TableEntry(name="absolute error",
                           symbol=math(rf"\absoluteerror{{{math_var}}}"),
                           expression=math(absolute(error(math_var))),
                           variables=math(rf"{math_var} \in \left\{{P, Q\right\}}"),
                           unit="p.u."),
                TableEntry(name="relative absolute error",
                           symbol=math(rf"\relativeabsoluteerror{{{math_var}}}"),
                           expression=math(frac(rf"\absoluteerror{{{math_var}}}", absolute(math_var))),
                           variables=math(rf"{math_var} \in \left\{{P, Q\right\}}"),
                           unit=math(r"\cdot"))
            ],
            caption="Metrics with regard to the equality constraints",
            marker=Marker("equalityconstraintmetrics", prefix="tab")
        )
    )
    metrics.append(equality_constraints)

    inequality_constraints = Subsubsection("Inequality constrains", numbering=False)
    inequality_constraints.append(Command("input", "methodology/metrics/inequality_constraints"))

    inequality_constraints.append(
        create_metrics_table(
            header=header,
            entries=[
                TableEntry(name="upper bound error",
                           symbol=math(rf"\uppererror{{{math_var}}}"),
                           expression=maximum(f"0, {math_var} - {math_var}_{{max}}"),
                           variables=math(rf"{math_var} \in \left\{{P, Q, V\right\}}"),
                           unit="p.u."),

                TableEntry(name="lower bound error",
                           symbol=math(rf"\lowererror{{{math_var}}}"),
                           expression=minimum(f"0, {math_var} - {math_var}_{{min}}"),
                           variables=math(rf"{math_var} \in \left\{{P, Q, V\right\}}"),
                           unit="p.u.")
            ],
            caption="Metrics with regard to the inequality constraints",
            marker=Marker("inequalityconstraintmetrics", prefix="tab")
        )
    )
    metrics.append(inequality_constraints)

    objective_function = Subsubsection("Objective function", numbering=False)
    objective_function.append(Command("input", "methodology/metrics/objective_function"))
    objective_function.append(
        create_metrics_table(
            header=["Name", "Symbol", "Math expression", "Unit"],
            entries=[
                TableEntry(name="cost",
                           symbol="C",
                           expression=math(r"\objectivefunction"),
                           unit=math(frac("currency", "h"))),
                TableEntry(name="relative cost",
                           symbol=math(r"\relativecost"),
                           expression=math(frac(r"C", r"C_{target}")),
                           unit=math(r"\cdot"))
            ],
            caption="Metrics with regard to the objective function",
            marker=Marker("objectivefunctionmetrics", prefix="tab")
        )
    )
    metrics.append(objective_function)

    with open(os.path.join(current_directory, "metrics.tex"), "w") as f:
        f.write(metrics.dumps())
