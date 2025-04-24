# eLabFTW API Workshop

This repository can be cloned to follow the API workshop proposed by [Deltablot](https://www.deltablot.com).

You can open and run notebooks with [Jupyter](https://jupyter.org/) on your computer (option 1) or use Google Colab (option 2).

## Useful links

* Getting started: https://doc.elabftw.net/api.html
* Api specification documentation: https://doc.elabftw.net/api/v2/
* Python library repository: https://github.com/elabftw/elabapi-python
* HTML documentation: https://doc.elabftw.net/api/elabapi-html/

## Option 1: open notebooks locally with Jupyter

Note: the commands below assume a GNU/Linux or MacOS operating system. If you are using Windows, it is recommended to ~ditch it~ use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

~~~bash
# Clone the repository on your computer
git clone https://github.com/elabftw/api-workshop.git

# Get into the folder
cd api-workshop

# Create a python virtual environment
python -m venv venv

# Activate the environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyterlab
jupyter lab
~~~

If you have followed the above commands, a new window will have opened in your browser. Select `part1-api-workshop-intro.ipynb` in the left pane to get started with the workshop.

## Option 2: open notebooks with Google Colab

You can use Google Colab service to open the Jupyter notebooks.

1. Access https://colab.research.google.com/
2. Select GitHub
3. Enter this GitHub URL in the the search bar: `elabftw/api-workshop` and press enter
4. Select `part1-api-workshop-intro.ipynb`
