from rich.console import Console
from rich.table import Table

table = Table()
# Explicitly add columns
table.add_column("a")
table.add_column("b")

# Add rows one by one
table.add_row("1", "2")
table.add_row("3", "4")

console = Console()
console.print(table)
