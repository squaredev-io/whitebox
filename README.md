Update June 19, 2023: Whitebox is now prioritizing monitoring LLMs. This repo is no longer maintained, but our commitment to building fair and responsible AI applications remains. If you're passionate about ML or React and want to join us as a founding engineer, reach out to Kostas on Discord.

---

# Whitebox - E2E machine learning monitoring

<p align="center">
    <em>Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes
</em>
</p>

---

**Documentation**: <a href="https://whitebox-ai.github.io/whitebox/" target="_blank">https://whitebox-ai.github.io/whitebox</a>

**Source Code**: <a href="https://github.com/whitebox-ai/whitebox" target="_blank">https://github.com/whitebox-ai/whitebox</a>

**Roadmap**: <a href="https://github.com/whitebox-ai/whitebox/milestones" target="_blank">https://github.com/whitebox-ai/whitebox/milestones</a>

**Issue tracking** <a href="https://github.com/orgs/whitebox-ai/projects/1/views/3" target="_blank">https://github.com/orgs/whitebox-ai/projects/1/views/3</a>

**Discord**: <a href="https://discord.gg/G5TKJMmGUt" target="_blank">https://discord.gg/G5TKJMmGUt</a>

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

Install the server using `docker compose`. See the [docs](https://whitebox-ai.github.io/whitebox/tutorial/installation) for more info.

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

Now you're ready to start using Whitebox! Read the [documentation](https://whitebox-ai.github.io/whitebox/) to learn more about the SDK.

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

**Documentation is hosted bby GitHub here**: <a href="https://whitebox-ai.github.io/whitebox/" target="_blank">https://whitebox-ai.github.io/whitebox</a>

```
mkdocs serve -f docs/mkdocs/mkdocs.yml -a localhost:8001
```

# Deploy Whitebox

## Using docker

Whitebox uses postgres as its database. They need to run in the same docker network. An example docker-compose file is located in the `examples` folder. Make sure you replace the SECRET_KEY with one of your own. Look below for more info.

```bash
docker-compose -f examples/docker-compose/docker-compose.yml up
```

If you just need to run Whitebox, make sure you set the `DATABASE_URL` in the environment.

```bash
docker run -dp 8000:8000 sqdhub/whitebox:main -e DATABASE_URL=postgresql://user:password@host:port/db_name
```

To save the api key encrypted in the database, provide a SECRET_KEY variable in the environment that is consisted of a 16 bytes string.

```bash
python -c "from secrets import token_hex; print(token_hex(16))"
```

**_Save this token somewhere safe._**

The api key can be retrieved directly from the postgres database:

```bash
API_KEY=$(docker exec <postgres_container_id> /bin/sh -c "psql -U postgres -c \"SELECT api_key FROM users WHERE username='admin';\" -tA")

echo $API_KEY
```

If you've set the `SECRET_KEY` in the environment get the decrypted key using:

```bash
docker exec <whitebox_container_id> /usr/local/bin/python scripts/decrypt_api_key.py $API_KEY
```

## Using Helm

You can also install Whitebox server and all of its dependencies in your k8s cluster using `helm`

```bash
helm repo add squaredev https://chartmuseum.squaredev.io/
helm repo update
helm install whitebox squaredev/whitebox
```

# Contributing

We happily welcome contributions to Whitebox. You can start by opening a new issue!
