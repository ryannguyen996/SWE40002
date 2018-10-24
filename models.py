from app import db


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    unit_number = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=False)
    satisfaction = db.Column(db.Integer, nullable=False)
    assessment_topic = db.Column(db.Integer, nullable=False)
    class_topic = db.Column(db.Integer, nullable=False)
    teacher_topic = db.Column(db.Integer, nullable=False)
    other_topic = db.Column(db.Integer, nullable=False)
    resource_topic = db.Column(db.Integer, nullable=False)
    sentiment = db.Column(db.Integer, nullable=False)

    def __init__(self, student_id, unit_number, comment, satisfaction,  assessment_topic, class_topic, teacher_topic, other_topic, resource_topic,sentiment):
        self.student_id = student_id
        self.unit_number = unit_number
        self.comment = comment
        self.satisfaction = satisfaction
        self.assessment_topic = assessment_topic
        self.class_topic = class_topic
        self.teacher_topic = teacher_topic
        self.other_topic = other_topic
        self.resource_topic = resource_topic
        self.sentiment = sentiment

    def __repr__(self):
        return '<id {}>'.format(self.id)
