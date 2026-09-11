# Lakekeeper Binary

Iniciamos docker compose:

```bash
docker compose up  -d --build --force-recreate
```



Creamos base de datos `catalog_database`:

```bash
docker exec -it postgres psql -U postgres
```

```postgresql
CREATE DATABASE catalog_database;
```

For single node deployments, a basic configuration via environment variables would look like this:

```bash
export LAKEKEEPER__PG_DATABASE_URL_READ="postgres://postgres:postgres@localhost:5434/catalog_database"
export LAKEKEEPER__PG_DATABASE_URL_WRITE="postgres://postgres:postgres@localhost:5434/catalog_database"
export LAKEKEEPER__PG_ENCRYPTION_KEY="MySecretEncryptionKeyThatIBetterNotLoose"

./lakekeeper migrate
./lakekeeper serve
```



```bash

```

