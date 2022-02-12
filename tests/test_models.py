import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

import unittest
from app import create_app, db
from app.Model.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setup(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  
    
    def test_password_hashing(self):
        u = User(username='Haloplayer', email='Haloplayer@wsu.edu')
        u.set_password('Haloplayer')
        self.assertFalse(u.get_password('Xboxplayer'))
        self.assertTrue(u.get_password('Haloplayer'))

    def test_post(self):
        u1 = User(username='Faculty_1', email='Faculty@wsu.edu')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(),[])
        p1 = Post(project_title='TEST', description='TEST TEST TEST', user_id=u1.id, date1='05/20/2022',date2='05/20/2023'
        ,time = '14', requirements = 'TEST')
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().project_title, 'TEST')
        self.assertEqual(u1.get_user_posts().first().description, 'TEST TEST TEST')
        self.assertEqual(u1.get_user_posts().first().date1, '05/20/2022')
        self.assertEqual(u1.get_user_posts().first().date2, '05/20/2023')
        self.assertEqual(u1.get_user_posts().first().time, '14')
        self.assertEqual(u1.get_user_posts().first().requirments, 'TEST')

    def more_test_post(self):
        u1 = User(username='Faculty_1', email='Faculty@wsu.edu')
        u2 = User(username='Dylan', email='Dylan@wsu.edu')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])

        p1 = Post(project_title='TEST', description='TEST TEST TEST', user_id=u1.id, date1='05/20/2022',date2='05/20/2023'
        ,time = '14', requirements = 'TEST')
        db.session.add(p1)
        db.session.commit()

        p2 = Post(project_title='IDK', description='TEST MORE TEST', user_id=u1.id, date1='08/10/2022',date2='03/20/2023'
        ,time = '6', requirements = 'NONE')
        db.session.add(p2)
        db.session.commit()
        #another person
        p3 = Post(project_title='WHY', description='WHY MORE TEST', user_id=u2.id, date1='01/18/2022',date2='08/18/2023'
        ,time = '6', requirements = 'High coding skill')
        db.session.add(p3)
        db.session.commit()

        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[1].title, 'IDK')
        self.assertEqual(u1.get_user_posts().all()[1].body, 'TEST MORE TEST')
        self.assertEqual(u1.get_user_posts().all().date1, '08/10/2022')
        self.assertEqual(u1.get_user_posts().all().date2, '03/20/2023')
        self.assertEqual(u1.get_user_posts().all().time, '6')
        self.assertEqual(u1.get_user_posts().all().requirments, 'NONE')


        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].title, 'WHY')
        self.assertEqual(u2.get_user_posts().all()[0].body, 'WHY MORE TEST')
        self.assertEqual(u1.get_user_posts().all().date1, '01/18/2022')
        self.assertEqual(u1.get_user_posts().all().date2, '08/18/2023')
        self.assertEqual(u1.get_user_posts().all().time, '6')
        self.assertEqual(u1.get_user_posts().all().requirments, 'High coding skill')


if __name__ == '__main__':
    unittest.main(verbosity=2)
