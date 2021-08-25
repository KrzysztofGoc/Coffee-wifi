get_cafe_schema = {
    "type": "object",
    "properties": {
        "coffee_quality": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1,
            "pattern": "^[1-5]$",
        },
        "wifi_speed": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1,
            "pattern": "^[0-5]$",
        },
        "power_socket": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1,
            "pattern": "^[1-5]$",
        },
    },
    "additionalProperties": False,
}
