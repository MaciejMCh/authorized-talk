import unittest


class AssignRoleTestCase(unittest.TestCase):
    def test_assign_role(self):
        self.assertEqual(True, False)

    def test_assign_role_for_not_connected_actor(self):
        self.assertEqual(True, False)

    def test_assign_role_as_not_admin(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
