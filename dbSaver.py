import uuid


class DBSaver:
    def __init__(self, db, username):
        self.conversation_id = uuid.uuid4()
        self.date = None
        self.username = username
        self.feelings_dict = {}  # from participant to behaviors object
        self.total_checks = 0
        self.total_matches = 0
        self.db = db

    def save_statistics(self):
        # conversation_id, date, username - same for all participants

        for participant in self.feelings_dict:
            behaviors_object = self.feelings_dict[participant][0]
            is_user = self.feelings_dict[participant][1]

            if is_user:
                total_checks = self.total_checks
                total_matches = self.total_matches
                participant = "user"
            else:
                total_checks = None
                total_matches = None

            self.db.statistics.insert_one(
                {'conversation_id': str(self.conversation_id), 'username': self.username, 'participant': participant,
                 'date': self.date, 'is_user': is_user, 'behaviors': behaviors_object.__dict__, 'checks': total_checks,
                 'matches': total_matches})
