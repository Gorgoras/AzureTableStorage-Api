import os
import json
import logging
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting bulk insert.')
    ret = dict()

    table_name = req.headers.get('name')

    values = req.get_json()      

    if table_name:
        retrieved_secret = getConnectionString()

        table_service = TableService(connection_string=retrieved_secret.value)
        batch = TableBatch()
        for i in range(0, len(values)):
            batch.insert_entity(values[i])

        table_service.commit_batch(table_name, batch)

        return func.HttpResponse(
            json.dumps(ret),
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Please pass a table name!",
             status_code=400
        )
