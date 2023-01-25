# Whitebox - E2E machine learning monitoring

<p align="center">
  <a href="https://squaredev-io.github.io/whitebox">
    <img src="https://squaredev-io.github.io/whitebox/img/logo.svg" alt="Whitebox" width="50%">
  </a>
</p>
<p align="center">
    <em>Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes
</em>
</p>

---

**Documentation**: <a href="https://squaredev-io.github.io/whitebox/" target="_blank">https://squaredev-io.github.io/whitebox</a>

**Source Code**: <a href="https://github.com/squaredev-io/whitebox" target="_blank">https://github.com/squaredev-io/whitebox</a>

**Roadmap**: <a href="https://github.com/squaredev-io/whitebox/milestone/2" target="_blank">https://github.com/squaredev-io/whitebox/milestone/2</a>

---

Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes.

The key features are:

- **Classification models metrics**
- **Regression models metrics**
- **Data / model drift monitoring**
- **Alerts**

Design guidelines:

- **Easy**: Very easy to set up and get started with.
- **Intuitive**: Designed to be intuitive and easy to use.
- **Pythonic SDK**: Pythonic SDK for building your own monitoring infrastructure.
- **Robust**: Get production-ready MLOps system.
- **Kubernetes**: Get production-ready code. With automatic interactive documentation.

# Installation

Install the server using `docker compose`. See the [docs](https://squaredev-io.github.io/whitebox/tutorial/installation) for more info.

Install the SDK with `pip`:

```bash
pip install whitebox-sdk
```

# How to use

After you are done installing the server and the SDK, you can start using it.

After you get the API key, all you have to do is create an instance of the Whitebox class adding your host and API key as parameters:

```python
from whitebox import Whitebox

wb = Whitebox(host="127.0.0.1:8000", api_key="some_api_key")
```

Now you're ready to start using Whitebox! Read the [documentation](https://squaredev-io.github.io/whitebox/) to learn more about the SDK.

# Set up locally for development

Whitebox supports Postgres and SQLite. You can use either one of them.
If you want to use SQLite, you need to set up a SQLite database and set the `DATABASE_URL` environment variable to the database URL.
If you want to use Postgres, you don't need to do anything. Just have a Postgres database running and set the `DATABASE_URL` environment variable to the database URL.

### Install packages:

```bash
python -m venv .venv
pip install -r requirements.txt
pre-commit install
```

### Run the server:

```bash
ENV=dev uvicorn whitebox.main:app --reload
```

### Quick way to start a postgres database:

```bash
docker compose up postgres -d
```

### Tests:

- Run: `ENV=test pytest` or `ENV=test pytest -s` to preserve logs.
- Watch: `ENV=test ptw`
- Run test coverage `ENV=test coverage run -m pytest`
- Look at coverage report: `coverage report` or `coverage html` to generate an html. To view it in your browser open the `htmlcov/index.html` file.

### Docs

**Documentation is hosted bby GitHub here**: <a href="https://squaredev-io.github.io/whitebox/" target="_blank">https://squaredev-io.github.io/whitebox</a>

```
mkdocs serve -f docs/mkdocs/mkdocs.yml -a localhost:8001
```

# Contributing

We happily welcome contributions to Whitebox. You can start by opening a new issue!
