# sqlQuery

Experimental feature: send a sql query against a table and return its json representation. Uses sqlite syntax.

In this iteration only one table is supported. The sql query must use "df" as the table name, regardless of its name in the data lake.

How it works: load the whole table in a pandas dataframe, mount a sqlite db, store the table there, run the query, build a pandas dataframe with the response and return it as json.

**URL** : `/api/sqlQuery/`

**Method** : `POST` or `GET`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[existing table in lake]",
    "query": "[sql query using df as table name]"
}
```

**Data example**

```json
{
    "name": "example",
    "column": "select count(*) from df"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "count(*)":{"0":5}
}
```
