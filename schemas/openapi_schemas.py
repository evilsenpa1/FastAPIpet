# books/openapi_schemas.py
from schemas.book_schema import BookAddSchema

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
                        "data": BookAddSchema.model_json_schema()
                    },
                    "required": ["data"]
                }
            }
        },
        "required": True
    }
}