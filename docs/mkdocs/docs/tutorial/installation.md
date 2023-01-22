# Installation

## Docker

Install whitebox server and all of its dependencies using `docker-compose`

Copy the folloing code in a file named `docker-compose.yml`:

```yaml
version: "3.10"
services:
  postgres:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_MULTIPLE_DATABASES=test # postgres db is created by default
    logging:
      options:
        max-size: 10m
        max-file: "3"
    ports:
      - "5432:5432"
    volumes:
      - wb_data:/var/lib/postgresql/data

  whitebox:
    profiles: ["whitebox"]
    image: sqdhub/whitebox:main
    restart: unless-stopped
    environment:
      - APP_NAME=Whitebox | Docker
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres
    ports:
      - "8000:8000"
    depends_on:
      - postgres

volumes:
  wb_data:
```

and then run the following command:

<div class="termy">

```console
$  docker compose up

```

</div>

## Kubernetes

!!! info

    As kubernetes deployment is part of our Professional offering please [contact us](https://forms.office.com/pages/responsepage.aspx?id=-XXSgSIX1keVdU9wdH0U-XphvBYZ6r5PmfX1dlo1e3tUOFQyNkVNQkZRVUo0WTNXRkZTNVlPSzhJQy4u).
