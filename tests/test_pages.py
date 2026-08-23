import unittest
from app import app, db


class ErrorPageTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404_error_page_renders_custom_template(self):
        response = self.client.get('/this-route-does-not-exist')
        self.assertEqual(response.status_code, 404)
        response_text = response.get_data(as_text=True)
        self.assertIn('404 Error', response_text)
        self.assertIn('/static/img/project.png', response_text)
        self.assertIn('Empty line, no bite!', response_text)
        self.assertIn('Back to Dashboard', response_text)

    def test_static_asset_serves_project_png(self):
        response = self.client.get('/static/img/project.png')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')
        self.assertTrue(len(response.data) > 0)
        response.close()


if __name__ == '__main__':
    unittest.main()
