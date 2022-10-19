description = """

# Introduction

### Welcome to the API reference!

The reference provides a detailed explanation of all resources accessible through the App Simulator API.
Our API is designed around REST, has predictable resource-oriented URLs and uses standard HTTP verbs and status codes.

### Versioning
The API base URL contains a version identifier. The current version is v1. 
**New properties and data models are continuously added, but the API will remain backwards compatible with this specification until deprecated.**

### Message formats
Requests are sent as JSON or in some cases form-encoded. 
String properties are encoded using UTF-8, and date properties are represented by UNIX Epoch time in milliseconds, or in some cases ISO 8601 strings.

"""


tags_metadata = [
    {
        "name": "Health",
        "description": "Health endpoints are used for checking the status of the service",
    },
    {
        "name": "XML",
        "description": "XML endpoints are used for generating XML samples",
    },
]
