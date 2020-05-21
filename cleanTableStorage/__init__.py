import os
import json
import time
import logging
from azure.cosmosdb.table.tableservice import TableService
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
import azure.functions as func
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name= req.headers.get('name')

    if not name: #If name wasnt added as header, search for it in the parameters
        name = req.params.get('name')

    if name:
        retrieved_secret = getConnectionString()

        table_service = TableService(connection_string=retrieved_secret.value)
        
        table_service.delete_table(name)
        time.sleep(1)
        existe = False
        while(not existe):
            logging.info("Intentando crearla...")
            time.sleep(5)
            existe = table_service.create_table(name)

        logging.info("Listo!!")

        ret = dict()
        ret['resultado'] = 'Listo!'
        return func.HttpResponse(
             json.dumps(ret),
             status_code=200
        )
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
