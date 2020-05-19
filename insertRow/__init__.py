import os
import json
import logging
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    KeyVault_DNS = os.environ["KeyVault_DNS"]
    SecretName = os.environ["SecretName"]

    
    table_name= req.headers.get('name')
    
    value = req.get_json()

    
    if table_name:
        try: # Try with managed identity, otherwise to with Service Principal
            creds = ManagedIdentityCredential()
            client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
            retrieved_secret = client.get_secret(SecretName)
        except:
            creds = ClientSecretCredential( client_id=os.environ["SP_ID"],
                                            client_secret=os.environ["SP_SECRET"],
                                            tenant_id=os.environ["TENANT_ID"])
            client = SecretClient(vault_url=KeyVault_DNS, credential=creds)
            retrieved_secret = client.get_secret(SecretName)

        table_service = TableService(connection_string=retrieved_secret.value)

        if table_service.exists(table_name):
            if 'PartitionKey' not in value.keys(): #This is mandatory
                value['PartitionKey'] = 'reference'
            
            if 'RowKey' not in value.keys(): #This is mandatory too
                value['RowKey'] = '001'
            try:
                table_service.update_entity(table_name=table_name, entity=value)
            except:
                table_service.insert_entity(table_name=table_name, entity=value)
        else:
            ret = dict()
            ret['result'] = "Please create the table!"
            return func.HttpResponse(
             json.dumps(ret),
             status_code=400
        )
        ret = dict()
        ret['result'] = "Success"
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
