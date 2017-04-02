max_redemption_rule = {
    "type": "object",
    "properties": {
        "status": {
            "type": "boolean"
        },
        "amount": {
            "type": "integer"
        },
        "redemption_time_reset": {
            "type": "string"
        }

    },
    "additionalProperties": False

}

limit_per_view_rule = {
    "type": "object",
    "properties": {
        "status": {
            "type": "boolean"
        },
        "amount": {
            "type": "integer"
        },
        "view_time_reset": {
            "type": "string"
        }

    },
    "additionalProperties": False
}

specify_setting = {
    "type": "object",
    "properties": {
        "status": {
            "type": "boolean"
        },
        "channel_message_end": {
            "type": "string"
        },
        "channel_message_start": {
            "type": "string"
        }

    },
    "additionalProperties": False
}

gift_code = {
    "type": "object",
    "properties": {
        "status": {
            "type": "boolean"
        },
        "total_code": {
            "type": "integer"
        },
        "code_left": {
            "type": "integer"
        },
        "code_number": {
            "type": "integer"
        },
        "list_code": {
            "type": "array"
        }

    },
    "additionalProperties": False
}

redemption_message = {
    "type": "object",
    "properties": {
        "status": {
            "type": "boolean"
        },
        "message": {
            "type": "string"
        }

    },
    "additionalProperties": False
}

time = {
    "type": "object",
    "properties": {
        "date": {
            "type": "string"
        },
        "timezone_type": {
            "type": "integer"
        },
        "timezone": {
            "type": "string"
        }

    },
    "additionalProperties": False
}

updated_at = {
    "date": "2017-04-02 04:12:00.477138",
    "timezone_type": 3,
    "timezone": "UTC"
}

schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "user_id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "description": {
            "type": ["string", "null"]

        },
        "bot_command": {
            "type": ["string", "null"]
        },
        "cooldown": {
            "type": "string"
        },
        "image": {
            "type": ["string", "null"]
        },
        "is_enable": {
            "type": "boolean"
        },
        "point": {
            "type": "integer"
        },
        "max_redemption_rule": max_redemption_rule,
        "limit_per_view_rule": limit_per_view_rule,
        "specify_setting": specify_setting,
        "gift_code": gift_code,
        "redemption_message": redemption_message,
        "reward_overlay_ids": {
            "type": "array"
        },
        "viewer_input_fields": {
            "type": "array"
        },
        "category": {
            "type": "string"
        },
        "template_id": {
            "type": ["integer", "null"]
        },
        "has_next": {
            "type": "boolean"
        },
        "redemption_limit_count": {
            "type": "integer"
        },
        "viewer_limit_count": {
            "type": "integer"
        },
        "last_redemption": {
            "type": ["integer", "null"]
        },
        "is_enable_mod": {
            "type": "boolean"
        },
        "created_at": time,
        "updated_at": time
    },
    "additionalProperties": False
}
