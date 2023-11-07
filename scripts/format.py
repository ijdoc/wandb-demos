import argparse
import nbformat
from black import format_str, FileMode, NothingChanged


def process_cell_source(source):
    # Split the cell content by lines
    lines = source.split("\n")
    # Temporarily replace shell and magic commands
    replacements = []
    for i, line in enumerate(lines):
        if line.strip().startswith(("!", "%")):
            # Replace the line with a marker
            replacements.append((i, line))
            lines[i] = f"# SHELL_OR_MAGIC_COMMAND_{i}"

    processed_source = "\n".join(lines)
    try:
        # Format with black
        formatted_source = format_str(processed_source, mode=FileMode())
        # Restore the shell and magic commands
        formatted_lines = formatted_source.split("\n")
        for i, original in replacements:
            formatted_lines[i] = original  # Put the original line back
        return "\n".join(formatted_lines).rstrip()
    except NothingChanged:
        return source


def main(notebook):
    # Load the notebook
    with open(notebook, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Iterate over the cells
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            # Process and format the cell content
            cell["source"] = process_cell_source(cell["source"])

    # Save the notebook
    with open(notebook, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    print(f"{notebook} formatted with black")


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Format a notebook in-place with black."
    )
    parser.add_argument(
        "notebook",
        type=str,
        help="The notebook to format",
    )

    # Parse the arguments
    args = parser.parse_args()

    main(args.notebook)
