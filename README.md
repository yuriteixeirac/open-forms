# OpenForm

A self-hostable, privacy focused formulary and survey manager that serves as a secure compliant alternative to similar services for gathering data and serving it on visual dashboard and REST API.

It works so that you can create surveys and share away with ease.

## How to install

To install, you need to clone the repository by running:

```
git clone https://github.com/yuriteixeirac/open-forms
cd open-forms
```

For the dependencies needed, activate a virtual environment and install poetry as the following step suggests:

```
python3 -m venv .venv
source .venv/bin/activate

pipx install poetry
poetry install
```

After that, you might wanna set up your database or leave it as a SQLite file. Either way, run migrations like this:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

And finally run the Django local server with:
```
python3 manage.py runserver
```
