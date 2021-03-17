# fixes some hard coded settings
LANG=C perl -pi -e ‘s/{PWD}/$ENV{PWD}/g’ .vscode/settings.json

# create virtual environment
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

# update pip
pip install --upgrade pip

# install requirements
pip install -r requirements_dev.txt
