import unittest

from flaskapp.models import RoleModel, Role
from flaskapp.models.user_model import UserModel
from tests.test_models.db_setup import DbSetup


class TestUserModel(DbSetup):

    def test_user(self):
        users = UserModel.query.filter().all()
        total_users = UserModel.total(UserModel.user_id)
        self.assertEqual(1, total_users)
        saved_user: UserModel = users[0]
        self.assertEqual(saved_user, self.user )
        user_role: RoleModel = RoleModel.find_by_id(Role.USER)
        self.assertTrue(saved_user.has_role(user_role.role_id))


if __name__ == '__main__':
    unittest.main()
