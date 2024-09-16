class UDLKeyError(Exception):
    def __init__(self, key: str, udl_dict: dict):
        self.key = key
        self.message = f"'{key}' not found in {udl_dict}"
        super().__init__(self.message)
