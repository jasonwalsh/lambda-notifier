import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEMA = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "repositories": {
      "items": {
        "type": "string"
      },
      "type": "array"
    }
  },
  "type": "object"
}
"""
