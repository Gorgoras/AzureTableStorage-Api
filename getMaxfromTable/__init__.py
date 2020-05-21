import os
import json
from datetime import datetime
import logging
import pandas as pd
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString

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
    logging.info('Starting getMaxFromTable')

    
    name= req.headers.get('name')
    col = req.headers.get('column')
    if not name:  #If name wasnt added as header, search for it in the parameters
        name= req.params.get('name')
        col = req.params.get('column')
    
    if name:
        retrieved_secret = getConnectionString()

        table_service = TableService(connection_string=retrieved_secret.value)

        df = get_dataframe_from_table_storage_table(table_service, name)
        maximo = df[col].max()
        ret = dict()
        try:
            dateMax = datetime.fromtimestamp(maximo.timestamp())
            dateRet = dateMax            
            ret['max'] = dateRet.strftime("%Y%m%d %H:%M:%S")
        except:
            ret['max'] = maximo
        return func.HttpResponse(
             json.dumps(ret),
             status_code=200
        )
    else:
        ret = dict()
        ret['result'] = "Please pass a name!!"
        return func.HttpResponse(
             json.dumps(ret),
             status_code=400
        )
