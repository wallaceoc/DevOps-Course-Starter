# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

Module
TRELLO
Step 1
Create a new TRELLO account
Visit ['https://trello.com/signup'](https://trello.com/signup) in your browser and follow the setup instructions for a new account

Step 2
Create a new TRELLO API KEY and TOKEN
Visit ['https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/'](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) for detailed instructions on how to both create an API_KEY and TOKEN

## TESTING
Add pytest as a dependency of our project by running poetry add pytest. This should download pytest and also update pyproject.toml for you.
NOTE: This will only need to be run by one person and anyone following this should not need to as long as they run the "poetry install" command to update their dependencies.
This will get pulled in automatically for following users because it's now registered in the pyproject.toml
'''bash
$ poetry add pytest
'''

Run ALL the tests by typing pytest from the command line
'''bash
$ poetry run pytest
'''

Run the tests from a specific class
'''bash
poetry run pytest todo_app/tests/<file.py>
'''bash

## Selenium tests
Install the selenium python package (this should be unnecessary as it is being tracked by Poetry but I had some issues and had to do this)
$ pip install -U selenium
$ poetry add selenium

Run the End to End tests
$ poetry run pytest todo_app/tests_e2e

## Ansible Provisioning
Run the below command to provision a VM from a Host node.
Note: you must ensure the necessary files from the playbook (in this case my-ansible-playbook.yml)
exist on the Controller

$ ansible-playbook my-ansible-playbook.yml -i ansible-inventory.ini

## Module 4 stretch goal

$ poetry add gunicorn

## Run in Docker

#### Development Mode

1. Build the development image
   '''bash
   docker build --target development --tag todo-app:dev .
   '''
2. Run the container (2 options)
   2.1 Docker Command
   '''bash
   docker run --env-file .env --publish 5000:80 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app/todo_app todo-app:dev
   '''

   2.2 Docker Compose.  This will start tests (unit, integration and end-to-end).  Tests will be automatically rerun when a file change is detected.  ***Note: If you add the --build option, it is forced to build the images even when not needed
   '''bash
   docker compose up [--build]
   '''

#### Production Mode
1. Build the production image
   '''bash
   docker build --target production --tag todo-app:prod .
   '''

2. Run the container
   '''bash
   docker run --env-file .env --publish 5000:80 todo-app:prod
   '''

