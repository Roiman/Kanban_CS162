import app, kanban_models
from app import app

import os
import unittest

from mock import patch, Mock, MagicMock


def mock_add(user): return user

class creation_testing(unittest.TestCase):
# access create page
    @patch('app.session')
    def test_create_connect(self, mock_connect_db):
        response = app.test_client().get('/create')
        self.assertEqual(response.status_code, 200)

# pass/user too short:
# not checking for errors in the form
# since the validate_on_submit should
    @patch('app.EmailPasswordForm')
    @patch('app.session')
    def test_short_username(self, mock_connect_db,mock_form):

        mock_form().validate_on_submit = MagicMock(return_value=True)
        mock_form().username.data = "name"
        mock_form().password.data = " pass"
        mock_connect_db.commit = MagicMock(return_value=True)
        mock_connect_db.add = mock_add
        self.app = app.test_client()
        rv = self.app.post("/create")
        
        assert rv

    def test_short_password(self):
        pass

# user exists
    def test_exising_user(self):
        pass

# sql injection while creating a user
    def test_sql_injection(self):
        pass


class login_testing(unittest.TestCase):
    # access login page
    def test_login(self):
        pass

    # providing wrong pswd for username
    def test_wrong_password(self):
        pass

    # providing an sql injection to phish the pswd
    def test_sql_injection_pswd(self):
        pass

    # provide wrong username to pswd
    def test_wrong_username(self):
        pass

    # try logging out when logged in
    def test_authenticated_logout(self):
        pass

    # try logging out when not logged in
    def test_unauthenticated_logout(self):
        pass

    # access index when logged in
    def test_authenticated_index(self):
        pass

    # access index when logged out
    def test_unauthenticated_index(self):
        pass


class task_testing(unittest.TestCase):
    # add task with no title
    def test_titless_task(self):
        pass

    # add task without StatusID
    def test_no_statusID(self):
        pass

    # add task without user_id
    def test_no_user_id(self):
        pass

    # add task with user id that doesn't exist
    def test_add_task_incorrect_userid(self):
        pass

    # provide incorrect id to update()
    def test_incorrect_id_update(self):
        pass

    # update status ID to the same status
    def test_fake_update(self):
        pass

    # check if update is correct with two ids with the same name
    def test_double_name_update(self):
        pass




if __name__ == '__main__':
    unittest.main()
