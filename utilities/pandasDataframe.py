import pandas


def get_data_from_table_storage_table(table_service, table_name):
    """ Retrieve data from Table Storage """
    SOURCE_TABLE = table_name
    for record in table_service.query_entities(
        SOURCE_TABLE
    ):
        yield record
        
def get_dataframe_from_table_storage_table(table_service, table_name):
    """ Create a dataframe from table storage data """
    return pandas.DataFrame(get_data_from_table_storage_table(table_service, table_name))

