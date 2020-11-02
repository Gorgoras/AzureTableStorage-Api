import os
import json
from datetime import datetime
import logging
import pandas as pd
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
import sys

#These are necessary to import from a parent folder because of venv
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utilities.login import getConnectionString
from utilities.pandasDataframe import get_dataframe_from_table_storage_table

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting getAggFromTable.')

    
    name= req.headers.get('name')
    col = req.headers.get('column')
    agg = req.headers.get('aggregation')

    if not name:  #If name wasnt added as header, search for it in the parameters
        name= req.params.get('name')
        col = req.params.get('column')
        agg = req.params.get('aggregation')
    if name:
        retrieved_secret = getConnectionString()

        table_service = TableService(connection_string=retrieved_secret.value)
 
        df = get_dataframe_from_table_storage_table(table_service, name)

        if agg == 'max' or agg=='maximum':
            ret_val = df[col].max()
        if agg == 'min' or agg=='minimum':
            ret_val = df[col].min()
        if agg == 'avg' or agg=='mean':
            ret_val = df[col].mean()

        ret = dict()
        try:
            dateMax = datetime.fromtimestamp(ret_val.timestamp())
            dateRet = dateMax            
            ret['result'] = dateRet.strftime("%Y%m%d %H:%M:%S")
        except:
            ret['result'] = ret_val
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
