# Setup
## Environment
Best practice is to create a virtual environment and install relevant dependencies in there to develop and run the code.

```
conda create -n <env_name> python=3.11
conda activate <env_name>
pip install -r requirements.txt -r requirements_linting.txt
```

Ensure that the env variable `OPENAI_API_KEY` provides a valid API key.

## Pre-commit
Install `pre-commit` in your local dev environment.
```
pip install pre-commit
pre-commit install
```
This makes applies various hooks before when you commit code. These hooks check the linting and formatting of your code and ensure that code is formatted properly following `flake8` and `black` standards.

You can read more [here](https://pre-commit.com/).

When you get stuck/annoyed by pre-commit rejecting your commit, you may choose to run `git commit -m "your message" --no-verify` or `-n` to skip the hooks. This is not recommended because it bypasses the linting and can introduce trouble for other devs.

# Tasks

- Send Request To Model
- Get Text Input From Shell
- Run Bash Commands with approval

# Demo
Export your `OPENAI_API_KEY`. Run `python main.py`.

## Use Case 1: List All Files In ~/Downloads
DONE

## Use Case 2: List Only PDF Files In Downloads
DONE

## Use Case 3: Run Docker-Compose in another repo & Get Model Predictions
(not completed/tested)
