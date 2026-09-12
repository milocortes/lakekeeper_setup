import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import requests

    # This CATALOG_URL and MANAGEMENT_URL work for the "docker compose" testing and development environment.
    # Change 'lakekeeper' if you are not running on "docker compose" (f. ex. 'localhost' if Lakekeeper is running locally).
    CATALOG_URL = "http://localhost:8181/catalog"
    MANAGEMENT_URL = "http://localhost:8181/management"
    return CATALOG_URL, MANAGEMENT_URL, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creamos Warehouse
    """)
    return


@app.cell
def _(MANAGEMENT_URL, requests):
    response = requests.post(f"{MANAGEMENT_URL}/v1/warehouse",
                  json={
                    # Name of the new warehouse
                    "warehouse-name": "cepcan",
                    # Physical location of this warehouse
                    "storage-profile": {
                        "type": "s3",
                        "bucket": "iceberg",
                        "flavor": "minio", # For AWS Warhouses, use flavor "aws"
                        # you can change the prefix to something else, f. ex. f"{WAREHOUSE}
                        # as long as it is unique in the bucket
                        #"key-prefix": "path/to/new-warehouse/",
                        "assume-role-arn": None,
                        "endpoint": "http://localhost:9001",
                        #"sts-endpoint": "http://seaweedfs:8333",
                        #"sts-role-arn": "arn:aws:iam::000000000000:role/LakekeeperVendedRole",
                        "region": "us-east-1",
                        "path-style-access": True,
                        "sts-enabled": True
                    },
                    # Storage Credentials for the profile specified above.
                    # These credentials are used to grant clients access to specific files in the storage.
                    # Clients do not need to know those credentials and will never obtain them directly.
                    "storage-credential": {
                        "type": "s3",
                        "credential-type": "access-key",
                        "access-key-id": "rustfsadmin",
                        "secret-access-key": "rustfsadmin"
                    }
                })
    print(f"{response.status_code}: {response.reason}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Crea tabla
    """)
    return


@app.cell
def _(CATALOG_URL):
    from pyiceberg.catalog.rest import RestCatalog
    import logging

    # logging.basicConfig(level=logging.DEBUG)

    import pandas as pd
    import pyarrow.parquet as pq
    import pyarrow as pa

    DEMO_WAREHOUSE = "cepcan"

    catalog = RestCatalog(
        name="my_catalog",
        warehouse=DEMO_WAREHOUSE,
        uri=CATALOG_URL,
        token="dummy",
    )
    return RestCatalog, catalog, pa, pd


@app.cell
def _(catalog):
    # Create a new namespace if it doesn't already exist
    test_namespace = ("pyiceberg_namespace",)
    if test_namespace not in catalog.list_namespaces():
        catalog.create_namespace(test_namespace)
    return (test_namespace,)


@app.cell
def _(catalog, pa, pd, test_namespace):
    # Write data
    test_table = ("pyiceberg_namespace", "my_table")
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "data": ["a", "b", "c"],
        }
    )
    pa_df = pa.Table.from_pandas(df)

    if test_table in catalog.list_tables(namespace=test_namespace):
        catalog.drop_table(test_table)

    table = catalog.create_table(
        test_table,
        schema=pa_df.schema,
    )

    table.append(pa_df)
    return (test_table,)


@app.cell
def _(catalog, test_table):
    # Read data
    catalog.load_table(test_table).scan().to_pandas()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Carga otro dataset
    """)
    return


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(pl):
    datos = pl.read_parquet("data/download.parquet")
    datos
    return (datos,)


@app.cell
def _(catalog, datos, pa, test_namespace):
    # Write data
    write_table = ("pyiceberg_namespace", "cdata")

    pa_cdata = pa.Table.from_pandas(datos.to_pandas())

    if write_table in catalog.list_tables(namespace=test_namespace):
        catalog.drop_table(write_table)

    table_cdata = catalog.create_table(
        write_table,
        schema=pa_cdata.schema,
    )

    table_cdata.append(pa_cdata)
    return (write_table,)


@app.cell
def _(catalog, write_table):
    # Read data
    catalog.load_table(write_table).scan().to_pandas()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creamos Warehouse en AWS
    """)
    return


@app.cell
def _(MANAGEMENT_URL, requests):
    response_aws = requests.post(f"{MANAGEMENT_URL}/v1/warehouse",
                #headers={
                #    "Authorization": f"Bearer {access_token}"
                #},
                  json={
                    # Name of the new warehouse
                    "warehouse-name": "cepcan-aws",
                    # Physical location of this warehouse
                    "storage-profile": {
                        "type": "s3",
                        "bucket": "polaris-milo",
                        "flavor": "aws", # For AWS Warhouses, use flavor "aws"
                        # you can change the prefix to something else, f. ex. f"{WAREHOUSE}
                        # as long as it is unique in the bucket
                        "key-prefix": "iceberg-data/",
                        #"assume-role-arn": None,
                        #"endpoint": "http://rustfs:9000",
                        #"sts-endpoint": "http://seaweedfs:8333",
                        #"sts-role-arn": "arn:aws:iam::000000000000:role/LakekeeperVendedRole",
                        "region": "us-east-2",
                        #"path-style-access": True,
                        "sts-enabled": True, 
                        "sts-role-arn": ""
                    },
                    # Storage Credentials for the profile specified above.
                    # These credentials are used to grant clients access to specific files in the storage.
                    # Clients do not need to know those credentials and will never obtain them directly.
                    "storage-credential": {
                        "type": "s3",
                        "credential-type": "access-key",
                        "access-key-id": "",
                        "secret-access-key": ""
                    }
                })
    print(f"{response_aws.status_code}: {response_aws.reason}")
    return


@app.cell
def _(CATALOG_URL, RestCatalog):
    catalog_aws = RestCatalog(
        name="my_catalog",
        warehouse="cepcan-aws",
        uri=CATALOG_URL,
        token="dummy",
    )
    return (catalog_aws,)


@app.cell
def _(catalog_aws):
    # Create a new namespace if it doesn't already exist
    namespace_aws = ("pyiceberg_namespace",)
    if namespace_aws not in catalog_aws.list_namespaces():
        catalog_aws.create_namespace(namespace_aws)
    return


@app.cell
def _(catalog_aws, datos, pa, test_namespace):
    # Write data
    write_table_aws = ("pyiceberg_namespace", "cdata")

    pa_cdata_aws = pa.Table.from_pandas(datos.to_pandas())

    if write_table_aws in catalog_aws.list_tables(namespace=test_namespace):
        catalog_aws.drop_table(write_table_aws)

    table_cdata_aws = catalog_aws.create_table(
        write_table_aws,
        schema=pa_cdata_aws.schema,
    )

    table_cdata_aws.append(pa_cdata_aws)
    return (write_table_aws,)


@app.cell
def _(catalog_aws, write_table_aws):
    # Read data
    catalog_aws.load_table(write_table_aws).scan().to_pandas()
    return


if __name__ == "__main__":
    app.run()
