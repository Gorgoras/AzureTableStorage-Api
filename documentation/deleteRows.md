# deleteRows

Deletes rows from an existing table, based on matching a pattern of a column.

**URL** : `/api/deleteRows/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

 * Header

 ```json
{
    "name": "[existing table in lake]",
    "column": "[existing column in table]",
    "pattern": "[words to filter which row to delete]"
}
```


**Data example**
* Header example
```json
{
    "name": "Feedback",
    "column": "PartitionKey",
    "pattern": "PK"
}
```


## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "result": "Deleted 100 rows!"
}
```
