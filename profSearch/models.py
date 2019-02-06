from profSearch import db

subject_association = db.Table('subject_association_table', db.Model.metadata,
    db.Column('subj_id', db.Integer, db.ForeignKey('subjects_table.id')),
    db.Column('prof_id', db.Integer, db.ForeignKey('professors_table.id')),
    db.PrimaryKeyConstraint('subj_id', 'prof_id')
)
lesson_association = db.Table('lesson_association_table', db.Model.metadata,
    db.Column('lesson_id', db.Integer, db.ForeignKey('lessons_table.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups_table.id')),
    db.PrimaryKeyConstraint('lesson_id', 'group_id')
)

class Professor(db.Model):
    __tablename__ = 'professors_table'
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    mName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Professor('{self.lName} {self.fName} {self.mName}')"

class Subject(db.Model):
    __tablename__ = 'subjects_table'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    subj_type = db.Column(db.Integer, db.ForeignKey('subject_type.id'))
    professors = db.relationship("Professor", secondary=subject_association,
                                 backref='subjects')
    lessons = db.relationship("Lesson", backref="subject", lazy='dynamic')
    dateFrom = db.Column(db.DateTime, nullable=True)
    dateTo = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Subject('{self.title}')"

class Subject_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Group(db.Model):
    __tablename__ = 'groups_table'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)
    spec_id = db.Column(db.Integer, db.ForeignKey('specialisations_table.id'))

class Specialisation(db.Model):
    __tablename__ = 'specialisations_table'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100), nullable=False)

class Lesson(db.Model):
    __tablename__ = 'lessons_table'
    id = db.Column(db.Integer, primary_key=True)
    tStart = db.Column(db.DateTime, nullable=True)
    tEnd = db.Column(db.DateTime, nullable=True)
    subj_id = db.Column(db.Integer, db.ForeignKey('subjects_table.id'), nullable=True)
    prof_id = db.Column(db.Integer, db.ForeignKey('professors_table.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    dayOfWeek = db.Column(db.Integer, db.ForeignKey('weekday.id'),nullable=True)
    isEvenWeek = db.Column(db.Boolean, db.ForeignKey('week_type.isEvenWeek'), nullable=True)
    subGroup = db.Column(db.Integer)

    groups = db.relationship("Group", backref='lessons',
                                secondary=lesson_association, lazy='joined')
    professor = db.relationship('Professor', backref='lessons')


class Week_type(db.Model):
    isEvenWeek = db.Column(db.Boolean, primary_key=True)
    title = db.Column(db.String(11))

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(15), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    lessons = db.relationship('Lesson', backref='classroom', lazy='joined')

class Weekday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(11), nullable=False)

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=True)