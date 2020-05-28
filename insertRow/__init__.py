import os
import json
import logging
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting insert row.')

    table_name= req.headers.get('name')
    if not table_name:  #If name wasnt added as header, search for it in the parameters
        table_name = req.params.get('name')

    value = req.get_json()

    
    if table_name:
        retrieved_secret = getConnectionString()

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
