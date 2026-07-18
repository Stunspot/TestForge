import unittest

from access_policy import Document, User, can_edit


class AccessPolicyTests(unittest.TestCase):
    def setUp(self):
        self.document = Document(owner_id="owner-1", tenant_id="tenant-a")

    def test_owner_can_edit(self):
        user = User("owner-1", "tenant-a", frozenset())
        self.assertTrue(can_edit(user, self.document))

    def test_editor_can_edit(self):
        user = User("editor-1", "tenant-a", frozenset({"editor"}))
        self.assertTrue(can_edit(user, self.document))

    def test_viewer_cannot_edit(self):
        user = User("viewer-1", "tenant-a", frozenset({"viewer"}))
        self.assertFalse(can_edit(user, self.document))


if __name__ == "__main__":
    unittest.main()
