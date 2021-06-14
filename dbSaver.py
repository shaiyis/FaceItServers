import uuid


class DBSaver:
    def __init__(self):
        self.conversation_id = uuid.uuid4()
        self.date = None
        self.username = ""
        self.feelings_dict = {}  # from participant to behaviors object
        self.total_checks = 0
        self.total_matches = 0
        # self.db = None
