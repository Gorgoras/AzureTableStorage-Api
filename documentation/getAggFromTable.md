# getAggFromTable

Used to get the aggregation of a column from a table. 

Accepted aggregations are: max, min and average.

**URL** : `/api/getAggFromTable/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[existing table in lake]",
    "column": "[existing column in table]",
    "aggregation": "max" or "maximum"
                   "min" or "minimum"
                   "avg" or "mean"
}
```

**Data example**

```json
{
    "name": "testAzureTableStorage",
    "column": "RowKey",
    "aggregation": "max"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "max": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```
