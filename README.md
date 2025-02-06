# socketio_quiz


[![Test Suite](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml/badge.svg)](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml)



    python -m venv venv && source venv/Scripts/activate
    python -m pip install --upgrade pip && pip install -r requirements/dev.requirements.txt


    pre-commit run --all-files


coverage run -m pytest

pytest --cov=src
