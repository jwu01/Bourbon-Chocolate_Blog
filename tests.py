import unittest
import os
import util.config as config
import util.accounts as accounts
import util.posts as posts

config.use_test_db()  # Use a test database

class TestAccounts(unittest.TestCase):
    def setUp(self):
        accounts.create_table()

    def tearDown(self):
        try:
            os.remove(config.DB_FILE)
        except FileNotFoundError:
            pass

    def test_user_exists(self):
        self.assertFalse(accounts.user_exists('foo'))

    def test_add_user(self):
        self.assertFalse(accounts.user_exists('foo'))
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.user_exists('foo'))
        accounts.add_user('new_user', 'bar')
        self.assertTrue(accounts.user_exists('new_user'))

    def test_auth_user(self):
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.auth_user('foo', 'bar'))
        self.assertFalse(accounts.auth_user('foo', 'bad_pass'))
        self.assertFalse(accounts.auth_user('not_a_user', 'bar'))
        self.assertFalse(accounts.auth_user('not_a_user', 'not_a_pass'))

    def test_remove_user(self):
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.user_exists('foo'))
        accounts.remove_user('foo')
        self.assertFalse(accounts.user_exists('foo'))
        accounts.remove_user('foo')
        self.assertFalse(accounts.user_exists('foo'))


class TestAccounts(unittest.TestCase):
    def setUp(self):
        posts.create_table()
        #  posts.db_file()

    def tearDown(self):
        try:
            os.remove(config.DB_FILE)
        except FileNotFoundError:
            pass

    def test_post_exists(self):
        self.assertFalse(posts.post_exists('foo'))

    def test_author_exists(self):
        posts.create_post('', '', '', 'anon')
        self.assertTrue(posts.author_exists('anon'))
        self.assertFalse(posts.author_exists('nobody'))

    def test_create_post(self):
        posts.create_post('post', 'title', 'content', 'anon')
        self.assertTrue(posts.post_exists('post'))

    def test_get_post(self):
        posts.get_post('nothing')
        posts.create_post('foo', 'title', 'content', 'anon')
        self.assertEqual(posts.get_post('foo'), 'content')

    #  def test_get_author_posts(self):
        #  posts.get_author_posts('nobody')
        #  posts.create_post('foo', 'title', 'content', 'anon')
        #  posts.get_author_posts('anon')

    def test_delete_post(self):
        posts.delete_post('fake_post')
        posts.create_post('foo', 'title', 'content', 'anon')
        self.assertTrue(posts.post_exists('foo'))
        posts.delete_post('foo')
        self.assertFalse(posts.post_exists('foo'))

    def test_edit_post(self):
        posts.create_post('foo', 'title', 'content', 'anon')
        posts.edit_post('ads1', 'hi','bye')
        posts.edit_post('oops', 'hi','bye')


if __name__ == '__main__':
    unittest.main()
