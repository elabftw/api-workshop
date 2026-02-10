#!/usr/bin/env python
# © Deltablot 2026
# License: MIT

"""
This script normalizes and localizes image paths in Jupyter notebooks.

What it does:
- Scans Jupyter notebooks (.ipynb) under the notebooks/ directory
- Only modifies Markdown cells (code cells are never touched)
- Replaces image paths that still reference the legacy ../../assets/ directory
  with the new standardized image layout under ../../images/

Path rules:
- Notebooks under notebooks/en/ will use:
    ../../images/en/
- Notebooks under notebooks/jp/ will use:
    ../../images/jp/

This allows English and Japanese notebooks to share the same content
structure while referencing language-specific image assets.

The script is safe to run multiple times (idempotent) and will only
update notebooks that actually require changes.
"""

import nbformat
from pathlib import Path

OLD_PREFIX = "../../images/jp/"
NEW_PREFIX = "../../images/en/"

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
