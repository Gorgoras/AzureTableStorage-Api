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

A list named rows, that contains every row in json format. 

**IMPORTANT**: Every row must include "PartitionKey" and "RowKey" attributes.
```json
{"rows":[
    {
    "PartitionKey": "[anything]", 
    "RowKey": "[anything]",
    "Value1": "[anything]"},
    ]
}
```

**Data example**
* Header example
```json
{
    "name": "testingTable"
}
```

* Body example
```json
{"rows":[{
        "PartitionKey": "tasksSeattle",
        "RowKey":"100",
        "Description":"Task-random"
      },{
        "PartitionKey": "tasksSeattle",
        "RowKey":"101",
        "Description": "Task-random2"}
       ]
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
