import os
import json
import time
import logging
from azure.cosmosdb.table.tableservice import TableService
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    KeyVault_DNS = os.environ["KeyVault_DNS"]
    SecretName = os.environ["SecretName"]

    if(req.method == 'POST'):
        name= req.headers.get('name')
    else:
        name = req.params.get('name')

    if name:
        creds = ManagedIdentityCredential()
        client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
        retrieved_secret = client.get_secret(SecretName)

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
