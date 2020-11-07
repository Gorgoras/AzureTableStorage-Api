import os
import logging
import pandas as pd
from pandasql import sqldf
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString
from utilities.pandasDataframe import get_dataframe_from_table_storage_table

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting SqlQuery.')

    
    name = req.headers.get('name')
    query = req.headers.get('query')
    logging.info('Name: {}'.format(name))
    logging.info('Query: {}'.format(query))

    if name:
        retrieved_secret = getConnectionString()

        logging.info('Getting table from azure storage')
        table_service = TableService(connection_string=retrieved_secret.value)

        df = get_dataframe_from_table_storage_table(table_service, name)

        logging.info('Applying query')
        result = sqldf(query, locals())

        return func.HttpResponse(
            result.to_json(), 
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Something went wrong! :(",
             status_code=400
        )
