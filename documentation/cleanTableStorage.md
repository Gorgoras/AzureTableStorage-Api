# cleanTableStorage

Deletes everything from a table, similar to truncate but you also lose columns (not an issue as tables are schema flex and can be created on write).

**URL** : `/api/cleanTableStorage/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[existing table in lake]"
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
    "resultado": "Listo!"
}
```
