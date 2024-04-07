# Backend API Usage Guide

This guide describes how to interact with the backend API to submit questions and receive answers.

## Endpoint

### POST /ask

You can use this API to pose questions to the e_TA bot, which will then provide the answers.

**Request Header**

- Content-Type: application/json

**Request Body**

- The body of the request should be a JSON object containing the **question** and **courseID**.
- courseID: ask for the specific course bot
- Example:

```sjson
{
  "question": "Your Question Here",
  "courseID": "EE450"
}
```

**Response**

- The API returns a JSON object with the answer. The response will look like this:

```Json
{
  "answer": "Answer from sBert",
  "llamaIndexAnswer": "Answer from llamaIndex",
  "question": "Your Question Here"
}
```

### POST /upload-json

You can use this API to upload new content to the e_TA bot, which will then store the embeddings of the new content in the database.

**Request Header**

- Content-Type: application/json

**Request Body**

- The body of the request should be a JSON object containing the courseID, fileID, content(a list of QA pair).
- courseID: table you want to upload to
- fileID: source of this upload
- Content: list of the knowledge

```
{
    "courseID": "EE450",
    "fileID": "EE450_Piazza",
    "content":{
        "0": "Question: xxx Answer: yyy.",
        "1": "Question: xxx Answer: yyy.",
        ...
    }
}
```

**Response**

- The API returns a JSON object with the status. The response will look like this:

```
{
    "message": "Table EE450 write finished."
}
```

### POST /readDB

You can use this API to read from database.

**Request Header**

- Content-Type: application/json

**Request Body**

- The body of the request should be a JSON object containing the hasStartKey, courseID, startKey, readLimit.
- `hasStartKey`: Boolean to start reading from `startKey` (true) or the first item (false).
- `startKey`: JSON key to begin reading from, required if `hasStartKey` is true.
- `courseID`: Identifies the table to read from.
- `readLimit`: Optional, sets the number of items to read at once.

```
{
    "hasStartKey": false, 
    "startKey": {"ID": "8085941781210758542", "CreatedTime":"2024-03-04T14:23:53.473605"},
    "courseID": "EE450",
    "readLimit": "5"
}
```

**Response**

- The API returns a JSON object with the status, message, and list of items.
- `message`: Status message of the scan, e.g., "scan successful".
- `result`: Contains the scan output with the following fields:
  - `items`: Array of data items fetched, each with `CreatedTime`, `Embedding`, `ID`, `OriginalText`, and `UploadSource`.
  - `message`: Echoes the scan status message.
  - `returned_count`: Number of items returned in the scan.
  - `startKey`: Key to start the next scan from, matching the last item's `CreatedTime` and `ID`.
  - `status`: HTTP status code of the scan operation, e.g., 200.
- The response will look like this:

```
{
    "message": "scan successful",
    "result": {
        "items": [
            {
                "CreatedTime": "2024-03-04T14:23:53.473185",
                "Embedding": "[xxx]",
                "ID": "4881078145242564971",
                "OriginalText": "Q&A pair",
                "UploadSource": "EE450_Piazza"
            }
        ],
        "message": "scan successful",
        "returned_count": 1,
        "startKey": {
            "CreatedTime": "2024-03-04T14:23:53.473185",
            "ID": "4881078145242564971"
        },
        "status": 200
    }
}
```

### POST /itemQuery

Read a specific item from the database

**Request Header**

- Content-Type: application/json

**Request Body**

- `courseID`: Specifies the table to target the request.
- `primary_key`: JSON object representing the primary key to locate the item, including `ID` and `CreatedTime`.

```
{  
    "courseID":"EE450",
    "primary_key": {"ID": "3290800591763312446", "CreatedTime":"2024-03-04T14:23:53.473560"}
}
```

**Response**

- `data`: Contains the details of the retrieved item, including:
  - `CreatedTime`: Timestamp of when the item was created.
  - `Embedding`: The embedding vector associated with the item.
  - `ID`: Unique identifier of the item.
  - `OriginalText`: The text content of the item, such as a question and answer.
  - `UploadSource`: Source identifier where the item was uploaded from.
- `message`: Describes the result of the operation, e.g., "Item found".
- `status`: HTTP status code indicating the result, e.g., 200 for success.

```
{
    "data": {
        "CreatedTime": "2024-03-04T14:23:53.473560",
        "Embedding": "[xxx]",
        "ID": "3290800591763312446",
        "OriginalText": "Q&A pair",
        "UploadSource": "EE450_Piazza"
    },
    "message": "Item found",
    "status": 200
}
```

### POST /itemUpdate

Update a specific item from the database

**Request Header**

- Content-Type: application/json

**Request Body**

- `courseID`: Specifies the table to target the request.
- `primary_key`: JSON object representing the primary key to locate the item, including `ID` and `CreatedTime`.
- `updateContent`: Updated content

```
{  
    "courseID":"EE450",
    "primary_key": {"ID": "3290800591763312446", "CreatedTime":"2024-03-04T14:23:53.473560"},
    "updateContent": "Question: how old is Mario Answer: 200"
}
```

**Response**
- `message`: Describes the result of the operation, e.g., "Item found".
- `status`: HTTP status code indicating the result, e.g., 200 for success.

```
{
    "message": "Item updated successfully",
    "status": 200
}
```

### POST /itemDelete

Delete a specific item from the database

**Request Header**

- Content-Type: application/json

**Request Body**

- `courseID`: Specifies the table to target the request.
- `primary_key`: JSON object representing the primary key to locate the item, including `ID` and `CreatedTime`.

```
{  
    "courseID":"EE450",
    "primary_key": {"ID": "3290800591763312446", "CreatedTime":"2024-03-04T14:23:53.473560"},
}
```

**Response**
- `message`: Describes the result of the operation, e.g., "Deleted successfully".
- `status`: HTTP status code indicating the result, e.g., 200 for success.

```
{
    "message": "Deleted successfully",
    "status": 200
}
```

### POST /upload-video

Upload transcript to the database

**Request Header**

- Content-Type: application/json

**Request Body**

- `courseID`: table you want to upload to
- `fileID`: source of this upload
- `Content`: list of the knowledge
    - Each item in content list shoudl contain:
        - 'timestamp'
        - 'content'
        - 'keyframe URL'

```
{
    "courseID": "EE599",
    "fileID": "lecture video",
    "content": [
        {
            "timestamp": "0:11- 1:11",
            "content": "Hi this is Mario, I'm the TA of EE599, and I'll help you anything about EE599",
            "keyframe URL": "None"
        },
        {
            "timestamp": "1:11- 2:11",
            "content": "EE599 is the Electrical Engineering class, maninly about VLSI design.",
            "keyframe URL": "None"
        }
    ]
}
```

**Response**
- `message`: Describes the result of the operation, e.g., "Deleted successfully".

```
{
    "message": "Table EE599 write finished."
}
```