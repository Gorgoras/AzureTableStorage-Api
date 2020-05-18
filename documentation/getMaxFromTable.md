# getMaxFromTable

Used to get the max of a column from a table.

**URL** : `/api/getMaxFromTable/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[existing table in lake]",
    "column": "[existing column in table]"
}
```

**Data example**

```json
{
    "name": "testAzureTableStorage",
    "column": "RowKey"
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
