class CreateRewardModel:
    def __init__(self, **kwargs):
        self.model = {
            "name": kwargs.get("name"),
            "point": kwargs.get("point", 0),
            "cooldown": "NO_COOLDOWN"
        }
