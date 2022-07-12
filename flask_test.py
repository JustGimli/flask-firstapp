import mainFlaskCore.core_app as core_app
import mainFlaskCore.config1 as config1
import os
import unittest
import tempfile


class FlaskUnitCase(unittest.TestCase):
    
    def setUp(self) :
        path = os.path.dirname(__file__)
        self.db_fd, path = tempfile.mkstemp()
        # config1.Config['TESTING'] = True
        self.app = core_app.app.test_client()
        core_app.init_db()

    
    def tearDown(self):
        os.close(self.db_fd)


    def test_empty_db(self):
        rv = self.app.get('/')
        assert   rv.data, 'не найдена главная страница'

    def login(self,username,password):
        return self.app.post('/login', data=dict(
            username = username,
            password = password
        ),follow_redirects = True)

    def logout(self):
        return self.app.get('/logout', follow_redirects = True)


    def test_login(self):
        rv = self.login('admin', 'default')
        assert 'Вы вошли', rv.data
        rv = self.logout()
        rv = self.login('adminx', 'default')
        assert rv.data, 'неправильный логин'
        rv = self.logout()
        rv = self.login('admin', '11')
        assert rv.data, 'неправильный пароль'
        rv = self.logout()

    def test_entries(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data = dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ),follow_redirects=True)
        assert 'No entries here so far', rv.data
        assert '&lt;Hello&gt;', rv.data
        assert '<strong>HTML</strong> allowed here', rv.data



if __name__ == '__main__':
    unittest.main()