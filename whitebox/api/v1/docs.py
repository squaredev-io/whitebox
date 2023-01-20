from whitebox.schemas.utils import ErrorResponse


tags_metadata = [
    {
        "name": "Health",
        "description": "Health endpoints are used for checking the status of the service",
    },
    {
        "name": "Models",
        "description": "This set of endpoints handles the models that a user creates.",
    },
    {
        "name": "Dataset Rows",
        "description": "This set of endpoints handles the dataset rows.",
    },
    {
        "name": "Inference Rows",
        "description": "This set of endpoints handles a model's inference rows.",
    },
    {
        "name": "Performance Metrics",
        "description": "This set of endpoints handles a model's performance metrics.",
    },
    {
        "name": "Drifting Metrics",
        "description": "This set of endpoints handles a model's drifting metrics.",
    },
    {
        "name": "Model Integrity Metrics",
        "description": "This set of endpoints handles a model's integrity metrics.",
    },
    {
        "name": "Model Monitors",
        "description": "This set of endpoints handles a model's model monitors.",
    },
    {
        "name": "Alerts",
        "description": "This set of endpoints handles a model's alerts.",
    },
    {
        "name": "Users",
        "description": "This is a helper endpoint to create and delete an admin user in tests.",
    },
    {
        "name": "Cron Tasks",
        "description": "This is a helper endpoint to trigger cron tasks for tests.",
    },
]


bad_request: ErrorResponse = {
    "title": "BadRequest",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

validation_error: ErrorResponse = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

authorization_error: ErrorResponse = {
    "title": "AuthorizationError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

not_found_error: ErrorResponse = {
    "title": "NotFoundError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

conflict_error: ErrorResponse = {
    "title": "ConflictError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

conflict_error: ErrorResponse = {
    "title": "ConflictError",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}

content_gone: ErrorResponse = {
    "title": "ContentGone",
    "type": "object",
    "properties": {
        "error": {"title": "Error Message", "type": "string"},
        "status_code": {"title": "Status code", "type": "integer"},
    },
}
