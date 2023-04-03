from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Service, Booking
import datetime


class TestPostModel(TestCase):
    """
    A class for testing blog app models
    """

    def setUp(self):
        """
        Set Up function to create user, login user, post and comment
        """
        self.user = User.objects.create_user(
            username="Admin", email="sam@gmail.com", password="02031977q"
        )
        self.user.save()
        self.client.login(username="Admin", password="02031977q")
        self.post = Post.objects.create(
            title="test", slug="test", author=self.user, status=1
        )
        self.post.save()
        self.comment = Comment.objects.create(
            post=self.post, name="Admin", body="Test comment body"
        )
        self.comment.save()
        self.service = Service.objects.create(
            service_name="Visit Exibition Room",
            price=3,
        )
        self.service.save()
        self.booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            name="John",
            date=datetime.date(2023, 4, 23),
        )

    def test_post_string_method_returns_title(self):
        """
        Test to check string method for Model app
        """
        post = self.post
        self.assertEqual(str(post), "test")

    def test_comment_string_method_returns_right_string(self):
        """
        Test to check string method for function for Model app
        """
        comment = self.comment
        self.assertEqual(
            str(comment), f"Comment {comment.body} by {self.user.username}"
        )

    def test_booking__returns(self):
        """
        Test to check method return for Model app
        """
        booking = self.booking
        self.assertEqual(str(booking), "John")
