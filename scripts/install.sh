VENV_PATH=./.venv

rm -rf ${VENV_PATH}
python3 -m venv ${VENV_PATH}

source ${VENV_PATH}/bin/activate
pip install --upgrade pip setuptools pipenv

pipenv install --dev

pip install -e .
