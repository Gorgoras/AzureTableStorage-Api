# bulkInsert

Inserts more than 1 row into an existing table.

**URL** : `/api/bulkInsert/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

 * Header

 ```json
{
    "name": "[existing table in lake]"
}
```

 * Body

All the columns with its values.
```json
{
    "PartitionKey": "[anything]", 
    "RowKey": "[anything]",
    "Value1": "[anything]"
}
```

**Data example**
* Header example
```json
{
    "name": "testAzureTableStorage"
}
```

* Body example
```json
{
    "PartitionKey": "Part1", 
    "RowKey": "001",
    "Value1": "myvalue"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "result": "Success"
}
```
