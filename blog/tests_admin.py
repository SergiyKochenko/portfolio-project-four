from django.test import TestCase
from django.urls import reverse
from .models import Post, Comment
from .admin import CommentAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User


class Test_Admin_Comment_Model(TestCase):
    """
    A class for testing blog app admin
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
            title="test blog",
            author=self.user,
        )
        self.post.save()
        self.comment = Comment.objects.create(
            name="Admin", post=self.post, body="Test comment body"
        )
        self.comment.save()
        self.site = AdminSite()
        self.commentModelAdmin = CommentAdmin(Comment, self.site)

    def test_admin_can_approve_comments(self):
        """
        test function to approve comments
        """
        comment = self.comment
        queryset = Comment.objects.filter(body="Test comment body")
        self.commentModelAdmin.approve_comments(comment, queryset)
        self.assertTrue(Comment.objects.get(body="Test comment body").approved)
