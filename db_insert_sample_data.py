from alayatodo import db
from alayatodo.models import Users, Todos


class FillData(object):
    def __init__(self):
        """ in case the tables haven't been created already"""
        db.drop_all()
        db.create_all()

    def insert_data(self):
        """insert data in db"""
        self.insert_users()
        self.insert_todos()

    def insert_todos(self):
        """ insert todos sample data"""
        data_todos = [(1, 'Vivamus tempus', False),
                      (1, 'lorem ac odio', False),
                      (1, 'Ut congue odio', False),
                      (1, 'Sodales finibus', False),
                      (1, 'Accumsan nunc vitae', False),
                      (2, 'Lorem ipsum', False),
                      (2, 'In lacinia est', False),
                      (2, 'Odio varius gravida', False)]
        for x in data_todos:
            row = Todos(user_id=x[0], description=x[1], is_completed=x[2])
            db.session.add(row)
            db.session.commit()

    def insert_users(self):
        """ insert users sample data"""
        data_users = [('user1', 'user1'),
                      ('user2', 'user2'),
                      ('user3', 'user3')]
        for y in data_users:
            row = Users(username=y[0], password=y[1])
            db.session.add(row)
            db.session.commit()