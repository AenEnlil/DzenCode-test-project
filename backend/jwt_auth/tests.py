from rest_framework.test import APITestCase


class CommentTests(APITestCase):

    def test_access_token_created(self):
        url = '/api/v1/tokens/create/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertIn('access', response_data)
        self.assertIn('refresh', response_data)

    def test_refresh_token(self):
        access_url = '/api/v1/tokens/create/'
        refresh_url = '/api/v1/tokens/refresh/'
        response = self.client.post(access_url)
        self.assertEqual(response.status_code, 200)
        access_token, refresh_token = response.data.get('access'), response.data.get('refresh')

        data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, data)
        self.assertEqual(response.status_code, 200)
        new_access_token = response.data.get('access')
        self.assertTrue(new_access_token)
        self.assertNotEqual(access_token, new_access_token)
