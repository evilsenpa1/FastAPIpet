# books/openapi_schemas.py
from schemas.book_schema import BookCreateRequest

UPLOAD_BOOK_OPENAPI = {
    "requestBody": {
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "file": {
                            "type": "string",
                            "format": "binary"
                        },
                        "data": BookCreateRequest.model_json_schema()
                    },
                    "required": ["data"]
                }
            }
        },
        "required": True
    }
}