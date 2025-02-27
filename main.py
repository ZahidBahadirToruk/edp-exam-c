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

class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email

    def apply_to_university(self, university_id):
        event = ApplicationSentEvent(self.student_id, university_id)
        return event

    def handle_application_response(self, event):
        if event.name == "application_approved":
            print(f"{self.name}: Application approved to University {event.payload['university_id']}.")
        elif event.name == "application_rejected":
            print(f"{self.name}: Application rejected by University {event.payload['university_id']}. Reason: {event.payload['reason']}")

class University:
    def __init__(self, university_id, name, capacity):
        self.university_id = university_id
        self.name = name
        self.capacity = capacity
        self.current_enrollment = 0

    def handle_application(self, event):
        if event.name == "application_sent":
            print(f"University {self.name} received application from Student {event.payload['student_id']}.")
            
            if self.current_enrollment < self.capacity:
                self.current_enrollment += 1
                return ApplicationApprovedEvent(event.payload["student_id"], self.university_id)
            else:
                return ApplicationRejectedEvent(event.payload["student_id"], self.university_id, "No available seats")

event_queue = []

student1 = Student("S001", "Alice", "alice@example.com")
student2 = Student("S002", "Bob", "bob@example.com")

university = University("U001", "Tech University", capacity=1)


event_queue.append(student1.apply_to_university(university.university_id))
event_queue.append(student2.apply_to_university(university.university_id))


while event_queue:
    event = event_queue.pop(0)

    if isinstance(event, ApplicationSentEvent):
        response_event = university.handle_application(event)
        event_queue.append(response_event)

    elif isinstance(event, ApplicationApprovedEvent):
        student1.handle_application_response(event)
        student2.handle_application_response(event)

    elif isinstance(event, ApplicationRejectedEvent):
        student1.handle_application_response(event)
        student2.handle_application_response(event)
