import os
import json
import logging
from azure.cosmosdb.table.tableservice import TableService
import azure.functions as func
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString
from utilities.pandasDataframe import get_dataframe_from_table_storage_table

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_name = req.headers.get('name')
    column = req.headers.get('column')
    pattern = req.headers.get('pattern')
    if not table_name:  #If name wasnt added as header, search for it in the parameters
        table_name = req.params.get('name')
    if not column:  #If column wasnt added as header, search for it in the parameters
        column = req.params.get('column')
    if not pattern:  #If pattern wasnt added as header, search for it in the parameters
        pattern = req.params.get('pattern')
    ret = dict()

    if table_name:
        retrieved_secret = getConnectionString()

        table_service = TableService(connection_string=retrieved_secret.value)
        df = get_dataframe_from_table_storage_table(table_service, table_name)

        #Filter dataframe by pattern
        to_delete = df[df[column].str.contains(pattern).fillna(value=False)]

        #Loop over the dataframe and delete records
        for i, o in to_delete.iterrows():
            logging.info('Deleting {}'.format(i+1))
            table_service.delete_entity(table_name,
                                        partition_key=o['PartitionKey'],
                                        row_key=o['RowKey'])
        ret['result'] = "Deleted {} rows!".format(to_delete.shape[0])
        return func.HttpResponse(
             json.dumps(ret),
             status_code=200
        )
    else:
        ret['result'] = "Please pass a table name!!"
        return func.HttpResponse(
             json.dumps(ret),
             status_code=400
        )

