from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_friend(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.friended.all(), [])
        self.assertEqual(u1.friends.all(), [])

        u1.friend(u2)
        db.session.commit()
        self.assertTrue(u1.is_friend(u2))
        self.assertEqual(u1.friended.count(), 1)
        self.assertEqual(u1.friended.first().username, 'susan')
        self.assertEqual(u2.friends.count(), 1)
        self.assertEqual(u2.friends.first().username, 'john')

        u1.unfriend(u2)
        db.session.commit()
        self.assertFalse(u1.is_friend(u2))
        self.assertEqual(u1.friended.count(), 0)
        self.assertEqual(u2.friends.count(), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
