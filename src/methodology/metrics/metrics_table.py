from dataclasses import dataclass
from typing import List

from pylatex import Table, Tabular, NoEscape, Label, Marker, Command


@dataclass
class TableEntry:
    name: str = None
    symbol: str = None
    expression: str = None
    variables: str = None
    unit: str = None


def create_metrics_table(header: List[str], entries: List[TableEntry], caption: str, marker: Marker):
    metric_tabular = Tabular("|" + "".join("c|" for _ in range(len(header))))
    metric_tabular.add_hline()
    metric_tabular.add_row(*header)
    metric_tabular.add_hline()

    for entry in entries:
        fields = [NoEscape(field) for field in [entry.name, entry.symbol, entry.expression, entry.variables, entry.unit] if field is not None]
        metric_tabular.add_row(*fields)
        metric_tabular.add_hline()

    table = Table(position="H")
    table.append(NoEscape(r'\centering'))
    table.append(NoEscape(r"{\makegapedcells"))
    table.append(metric_tabular)
    table.append(NoEscape(r"}"))
    table.add_caption(caption)
    table.append(Label(marker))
    return table
