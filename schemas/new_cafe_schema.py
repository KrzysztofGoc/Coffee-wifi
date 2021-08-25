new_cafe_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
        },
        "location": {
            "type": "string",
            "minLength": 1,
        },
        "open_time": {
            "type": "string",
            "minLength": 1,
            "pattern": "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        },
        "close_time": {
            "type": "string",
            "minLength": 1,
            "pattern": "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        },
        "coffee_quality": {
            "type": "string",
            "pattern": "^[1-5]{1}$",
        },
        "wifi_speed": {
            "type": "string",
            "pattern": "^[0-5]{1}$",
        },
        "power_socket": {
            "type": "string",
            "pattern": "^[1-5]{1}$",
        },
        "token": {
            "type": "string",
            "minLength": 43,
            "maxLength": 43,
        },
    },
    "required": ["name", "location", "open_time", "close_time", "coffee_quality", "wifi_speed", "power_socket",
                 "token"],
    "additionalProperties": False
}
