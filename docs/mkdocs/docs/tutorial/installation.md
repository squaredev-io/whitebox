# Installation

## Docker

Install whitebox server and all of its dependencies using `docker-compose`

Copy the following code in a file named `docker-compose.yml`:

```yaml
version: "3.10"
name: Whitebox
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
    networks:
      - whitebox

  whitebox:
    image: sqdhub/whitebox:main
    restart: unless-stopped
    environment:
      - APP_NAME=Whitebox | Docker
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres
      - SECRET_KEY=<add_your_own> # Optional, if not set the API key won't be encrypted
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - whitebox

volumes:
  wb_data:

networks:
  whitebox:
    name: whitebox
```

With your terminal navigate to `docker-compose.yml`'s location and then run the following command:

<div class="termy">

```console
$  docker-compose up

```

</div>

## Kubernetes

You can also install Whitebox server and all of its dependencies in your k8s cluster using `helm`

```bash
helm repo add squaredev https://chartmuseum.squaredev.io/
helm repo update
helm install whitebox squaredev/whitebox
```
