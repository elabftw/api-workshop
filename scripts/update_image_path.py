import nbformat
from pathlib import Path

OLD_PREFIX = "../../images/en/"
NEW_PREFIX = "../../images/jp/"

def update_notebook_image_paths(nb_path: Path) -> bool:
    """
    Update image paths inside markdown cells of a Jupyter notebook.
    Returns True if the notebook was modified.
    """
    nb = nbformat.read(nb_path, as_version=4)
    modified = False

    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue

        if OLD_PREFIX in cell.source:
            cell.source = cell.source.replace(OLD_PREFIX, NEW_PREFIX)
            modified = True

    if modified:
        nbformat.write(nb, nb_path)

    return modified


def process_directory(notebooks_dir: Path):
    notebooks = notebooks_dir.rglob("*.ipynb")

    for nb_path in notebooks:
        changed = update_notebook_image_paths(nb_path)
        if changed:
            print(f"✔ Updated: {nb_path}")
        else:
            print(f"– No change: {nb_path}")


if __name__ == "__main__":
    # Adjust this if needed
    NOTEBOOKS_DIR = Path("notebooks")

    if not NOTEBOOKS_DIR.exists():
        raise FileNotFoundError(f"{NOTEBOOKS_DIR} does not exist")

    process_directory(NOTEBOOKS_DIR)
