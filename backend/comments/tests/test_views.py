import random
from typing import List

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from ..models import Comment


class CommentsTestDataMixin:
    model = Comment

    @classmethod
    def create_main_comments(cls, number_of_comments: int) -> List[Comment]:
        comments = []
        for i in range(number_of_comments):
            comments.append(cls.model(text=f'main_comment{i}', username=f'user{i}', email=f'test_m{i}.mail.com'))
        cls.model.objects.bulk_create(comments)
        return comments

    @classmethod
    def create_answers(cls, comments_to_answer: List[Comment], answer_depth: int, answer_quantity: int) -> List[Comment]:
        created_answers = []
        for i in range(answer_depth):
            answers = []
            for comment in comments_to_answer:
                for j in range(answer_quantity):
                    answers.append(
                        Comment(text=f'answer{i}_{j}', username=f'user{i}', email=f'test{i}.mail.com', parent=comment))
            Comment.objects.bulk_create(answers)
            created_answers.extend(answers)
            comments_to_answer = answers
        return created_answers


class CommentTests(APITestCase, CommentsTestDataMixin):
    comment_create_data = {}

    @classmethod
    def setUpTestData(cls):
        comments = cls.create_main_comments(number_of_comments=40)

        cls.comment_with_answers = comments[0]
        comments_to_answer = [comments[0]]
        cls.create_answers(comments_to_answer, answer_depth=5, answer_quantity=2)

    def test_list_paginated(self):
        url = reverse('comment-list')
        main_comments = self.model.objects.filter(parent=None).order_by('-created_at')
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)
        self.assertIn('count', response_data)
        self.assertIn('results', response_data)
        self.assertIn('previous', response_data)
        self.assertIn('next', response_data)
        self.assertEqual(len(main_comments), response_data.get('count'))

        comments_from_response = response_data.get('results')
        self.assertNotEqual(len(main_comments), len(comments_from_response))
        self.assertTrue(response_data.get('next'))

    def test_list_return_only_main_comments(self):
        url = reverse('comment-list')
        main_comments = self.model.objects.filter(parent=None).order_by('-created_at')

        response = self.client.get(url)
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)
        self.assertEqual(len(main_comments), response_data.get('count'))

        comments_from_response = response_data.get('results')
        self.assertTrue(comments_from_response)
        self.assertEqual(main_comments[0].id, comments_from_response[0].get('id'))

    def test_list_comments_lifo_sorted(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)

        comments_from_response = response_data.get('results')
        self.assertTrue(comments_from_response)

        first_comment, last_comment = comments_from_response[0], comments_from_response[-1]
        self.assertNotEqual(first_comment, last_comment)
        self.assertTrue(first_comment.get('created_at') > last_comment.get('created_at'))

    def test_create_with_valid_data_without_homepage(self):
        data = {'email': 'test_case@gmail.com', 'username': 'testuser', 'text': 'test text'}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)

        comment_id = response_data.get('id')
        comment = self.model.objects.filter(id=comment_id).first()
        self.assertTrue(comment)
        self.assertEqual(comment.email, data.get('email'))
        self.assertIsNone(comment.homepage)

    def test_create_with_valid_data_with_homepage(self):
        data = {'email': 'test_case@gmail.com', 'username': 'testuser', 'text': 'test text',
                'homepage': 'https://test.com'}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)

        comment_id = response_data.get('id')
        comment = self.model.objects.filter(id=comment_id).first()
        self.assertTrue(comment)
        self.assertEqual(comment.email, data.get('email'))
        self.assertIsNotNone(comment.homepage)
        self.assertEqual(comment.homepage, data.get('homepage'))

    def test_create_with_invalid_email(self):
        data = {'email': 'invalid_email', 'username': 'testuser', 'text': 'test text'}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response_data)

        comment_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comment_exists)

    def test_create_with_invalid_homepage_format(self):
        data = {'email': 'test_case@gmail.com', 'username': 'testuser', 'text': 'test text',
                'homepage': 'invalid_homepage'}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response_data)

        comment_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comment_exists)

    def test_create_answer_to_comment(self):
        comment_to_answer = self.model.objects.all().first()
        self.assertTrue(comment_to_answer)

        data = {'email': 'test_case@gmail.com', 'username': 'testuser', 'text': 'test text',
                'parent': comment_to_answer.id}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)

        comment_id = response_data.get('id')
        comment = self.model.objects.filter(id=comment_id).first()
        self.assertTrue(comment)
        self.assertEqual(comment.email, data.get('email'))
        self.assertEqual(comment.parent.pk, comment_to_answer.id)

    def test_create_answer_to_not_existed_comment(self):
        data = {'email': 'test_case@gmail.com', 'username': 'testuser', 'text': 'test text',
                'parent': 999}
        url = reverse('comment-list')
        comments_already_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comments_already_exists)

        response = self.client.post(url, data)
        response_data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response_data)

        comment_exists = self.model.objects.filter(email=data.get('email')).exists()
        self.assertFalse(comment_exists)

    def test_retrieve_comment(self):
        comment = self.model.objects.all().first()
        self.assertTrue(comment)

        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)
        self.assertEqual(comment.pk, response_data.get('id'))
        self.assertEqual(comment.email, response_data.get('email'))

    def test_retrieve_not_existing_comment(self):
        url = reverse('comment-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response_data)

    def test_get_replies(self):
        answers = self.comment_with_answers.replies.all().order_by('-created_at').values()
        self.assertTrue(answers)

        url = reverse('comment-get-replies', kwargs={'pk': self.comment_with_answers.pk})
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)
        self.assertEqual(len(answers), len(response_data))
        self.assertEqual(answers[0].get('id'), response_data[0].get('id'))

    def test_get_replies_for_comments_without_answers(self):
        comment_without_answers = self.model.objects.filter(pk=2).first()
        self.assertTrue(comment_without_answers)
        self.assertFalse(comment_without_answers.replies.all())

        url = reverse('comment-get-replies', kwargs={'pk': comment_without_answers.pk})
        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_data)

    def test_get_replies_for_non_existing_comment(self):
        url = reverse('comment-get-replies', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertFalse(response.data)
