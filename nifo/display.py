from rich.console import Console
from rich.table import Table

class Display:
    def __init__(self, results, config_files, binary_count, image_count, verbose=False):
        self.results = results
        self.config_files = config_files
        self.binary_count = binary_count
        self.image_count = image_count
        self.verbose = verbose
        self.console = Console()

    def show(self):
        table = Table(title="Code Analysis Results")
        table.add_column("Language", style="cyan")
        table.add_column("Files", style="magenta")
        table.add_column("Total Lines", style="green")
        table.add_column("Code Lines", style="yellow")
        table.add_column("Comment Lines", style="red")
        table.add_column("% of Codebase", style="blue")

        total_lines = sum(lang_data["total_lines"] for lang_data in self.results.values())

        # Move 'Unknown' to the end
        sorted_results = sorted(self.results.items(), key=lambda x: (x[0] == 'Unknown', x[0]))

        unknown_percentage = 0
        for language, data in sorted_results:
            percentage = (data["total_lines"] / total_lines) * 100 if total_lines > 0 else 0
            if language == 'Unknown':
                unknown_percentage = percentage
            table.add_row(
                language,
                str(data["files"]),
                str(data["total_lines"]),
                str(data["code_lines"]),
                str(data["comment_lines"]),
                f"{percentage:.2f}%"
            )

        self.console.print(table)

        if unknown_percentage > 50:
            self.console.print("[bold red]Warning: More than 50% of the codebase is of unknown type. nifo might be having trouble parsing this folder.[/bold red]")

        self.console.print(f"\nBinary files: {self.binary_count}")
        self.console.print(f"Image files: {self.image_count}")

        if self.verbose:
            self.console.print("\nConfig and Secret Files:")
            for file in self.config_files:
                self.console.print(f"- {file}")