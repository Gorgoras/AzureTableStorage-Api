import os
import json
from datetime import datetime
import logging
import pandas as pd
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential


def get_data_from_table_storage_table(table_service, table_name):
    """ Retrieve data from Table Storage """
    SOURCE_TABLE = table_name
    for record in table_service.query_entities(
        SOURCE_TABLE
    ):
        yield record
        
def get_dataframe_from_table_storage_table(table_service, table_name):
    """ Create a dataframe from table storage data """
    return pd.DataFrame(get_data_from_table_storage_table(table_service, table_name))


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    KeyVault_DNS = os.environ["KeyVault_DNS"]
    SecretName = os.environ["SecretName"]

    if(req.method == 'POST'):
        name= req.headers.get('name')
        col = req.headers.get('column')
    else:
        name = req.params.get('name')
        name = req.params.get('column')
    if name:
        creds = ManagedIdentityCredential()
        client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
        retrieved_secret = client.get_secret(SecretName)

        table_service = TableService(connection_string=retrieved_secret.value)

        df = get_dataframe_from_table_storage_table(table_service, name)
        maximo = df[col].max()
        dateMax = datetime.fromtimestamp(maximo.timestamp())
        dateRet = dateMax

        ret = dict()
        ret['max'] = dateRet.strftime("%Y%m%d %H:%M:%S")
        return func.HttpResponse(
             json.dumps(ret),
             status_code=200
        )
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
