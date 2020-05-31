# createTable

Creates a new table in the data lake's table storage service.

**URL** : `/api/createTable/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[name for your table]"
}
```

**Data example**

```json
{
    "name": "testAzureTableStorage"
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
