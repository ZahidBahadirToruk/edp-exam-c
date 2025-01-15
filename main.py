class Event:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

class ApplicationSentEvent(Event):
    def __init__(self, student_id, university_id):
        super().__init__("application_sent", {"student_id": student_id, "university_id": university_id})

class ApplicationApprovedEvent(Event):
    def __init__(self, student_id, university_id):
        super().__init__("application_approved", {"student_id": student_id, "university_id": university_id})

class ApplicationRejectedEvent(Event):
    def __init__(self, student_id, university_id, reason):
        super().__init__("application_rejected", {"student_id": student_id, "university_id": university_id, "reason": reason})

