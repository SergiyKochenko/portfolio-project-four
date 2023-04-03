from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Service, Booking, Post
from blog.models import Booking
from blog.forms import BookingForm
from blog.forms import CreatePostForm

import datetime
import tempfile
import unittest
import datetime


class TestBookingViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sem", email="sem@gmail.com", password="02031977q"
        )
        self.user.save()
        self.client.login(username="sem", password="02031977q")
        self.service = Service.objects.create(
            service_name="Terrarium",
            price=10,
        )
        self.service.save()
        self.booking = Booking.objects.create(
            user=self.user,
            service=self.service,
            name="test",
            email="test@g.com",
            phone="+5355554433",
            date=datetime.date(2023, 4, 12),
            time="10:00",
        )
        self.post = Post.objects.create(
            title="Test Create",
            excerpt="test",
            content="test",
            author=self.user,
            featured_image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        )
        self.post.save()

    def test_get_booknow_page(self):
        response = self.client.get(reverse("booknow"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booknow.html")

    def test_user_can_book(self):
        response = self.client.post(
            reverse("booknow"),
            {
                "user": self.user,
                "service": self.service.id,
                "name": "test",
                "email": "test@gmail.com",
                "phone": "+5355554433",
                "date": datetime.date(2023, 4, 11),
                "time": "10:00",
            },
        )
        self.assertRedirects(response, "/bookings/")

    def test_can_edit_booking(self):
        id = self.booking.id
        response = self.client.post(
            reverse("change_booking", args=[id]),
            {
                "user": self.user,
                "service": self.service.id,
                "name": "test",
                "email": "test@g.com",
                "phone": "+3805554433",
                "date": datetime.date(2023, 4, 11),
                "time": "11:00",
            },
        )
        self.assertEquals(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEquals(self.booking.time, "11:00")

    def test_can_edit_return_booking(self):
        id = self.booking.id
        response = self.client.post(
            reverse("change_booking", args=[id]),
            {
                "user": self.user,
                "service": self.service.id,
                "name": "test",
                "email": "test@g.com",
                "phone": "+3805554433",
                "date": datetime.date(2022, 4, 11),
                "time": "11:00",
            },
        )
        self.assertEquals(response.status_code, 200)

    def test_can_get_edit_booking(self):
        id = self.booking.id
        response = self.client.get(reverse("change_booking", args=[id]))
        self.assertEquals(response.status_code, 200)

    def test_get_delete_booking_page(self):
        id = self.booking.id
        response = self.client.get(reverse("delete_booking", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete-booking.html")

    def test_can_delete_booking(self):
        id = self.booking.id
        response = self.client.post(reverse("delete_booking", args=[id]))

    def test_can_show_message_if_date_exists(self):
        response = self.client.post(
            reverse("booknow"),
            {
                "user": self.user,
                "service": self.service,
                "name": "test",
                "email": "test@g.com",
                "phone": "+3805554433",
                "date": datetime.date(2023, 4, 12),
                "time": "10:00",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_can_show_message_if_date_exists_when_user_edit_bookings(self):
        id = self.booking.id
        response = self.client.post(
            reverse("change_booking", args=[id]),
            {
                "user": self.user,
                "service": self.service.id,
                "name": "test",
                "email": "test@g.com",
                "phone": "+3805554433",
                "date": datetime.date(2023, 4, 12),
                "time": "10:00",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_get_usersblog_page(self):
        response = self.client.get(reverse("usersblog"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usersblog.html")

    def test_user_can_create_post(self):
        """
        Test to create post and redirect to 'usersblog' page
        """
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        response = self.client.post(
            reverse("create-post"),
            {
                "title": "Test jest",
                "excerpt": "test",
                "content": "test",
                "author": self.user,
                "featured_image": image,
            },
        )

        self.assertRedirects(response, "/usersblog/")

    def test_can_edit_post(self):
        """
        Test to edit post
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse("blog-edit", args=[slug]),
            {
                "title": "Edited Post Test",
                "excerpt": "test",
                "content": "test",
                "slug": self.post.slug,
                "author": self.user,
                "featured_image": "image",
            },
        )
        self.assertEquals(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEquals(self.post.title, "Edited Post Test")

    def test_can_edit_return_post(self):
        """
        Test to edit post
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.get(reverse("blog-edit", args=[slug]))
        self.assertEquals(response.status_code, 200)

    def test_can_delete_post(self):
        """
        Test to delete post
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(reverse("blog-delete", args=[slug]))
        self.assertRedirects(response, reverse("usersblog"), status_code=302)

    def test_can_delete_return_post(self):
        """
        Test to delete post
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.get(reverse("blog-delete", args=[slug]))
        self.assertEquals(response.status_code, 200)

    def test_get_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_get_pricing_page(self):
        response = self.client.get(reverse("pricing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pricing.html")

    def test_get_contact_page(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")


class TestBlogViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Bob", email="bob@gmail.com", password="02031977q"
        )
        self.user.save()
        self.client.login(username="Bob", password="02031977q")
        self.post = Post.objects.create(title="test", slug="test", author=self.user)
        self.post.save()

    def test_open_post_detail(self):
        """
        test open post detail page
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.get(reverse("post_detail", args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_post(self):
        """
        test post method for blog page
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(reverse("post_detail", args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_detail.html")


class TestUsersBlogViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Bob", email="bob@gmail.com", password="02031977q"
        )
        self.user.save()
        self.client.login(username="Bob", password="02031977q")
        self.post = Post.objects.create(title="test", slug="test", author=self.user)
        self.post.save()

    def test_open_users_post_detail(self):
        slug = self.post.slug
        response = self.client.get(reverse("usersblog_detail", args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usersblog_detail.html")

    def test_can_comment(self):
        """
        Test for comment functionality
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse("post_detail", args=[slug]), {"body": "test comment"}
        )
        self.assertEquals(response.status_code, 200)

    def test_can_comment_userblog(self):
        """
        Test for comment functionality
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse("usersblog_detail", args=[slug]), {"body": "test comment"}
        )
        self.assertEquals(response.status_code, 200)

    def test_comment_form_post_detail(self):
        """
        Test for likes functionality
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse("post_detail", args=[slug]), {"liked": "test"}
        )
        self.assertEquals(response.status_code, 200)

    def test_comment_form_usersblog_detail(self):
        """
        Test for likes functionality
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(
            reverse("usersblog_detail", args=[slug]), {"liked": "test"}
        )
        self.assertEquals(response.status_code, 200)

    def test_can_like(self):
        """
        test for like functionality
        """
        slug = self.post.slug
        response = self.client.post(reverse("post_like", args=[slug]), {})
        self.assertEquals(response.status_code, 302)

    def test_can_remove_like(self):
        """
        test for remove like
        """
        slug = self.post.slug
        self.post.likes.add(self.user)
        response = self.client.post(reverse("post_like", args=[slug]), {})
        self.assertEquals(response.status_code, 302)

    def test_create_post_invalid_form(self):
        """
        Test that a new blog post cannot be created with invalid form data
        """
        user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        data = {}
        response = self.client.post(reverse("create-post"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(Post.objects.filter(author=user).exists())

    def test_booknow_view_with_invalid_data(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/booknow/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booknow.html")

        data = {
            "date": "2023-04-02",
            "time": "10:00",
            "name": "",
            "email": "test@example.com",
        }
        response = self.client.post("/booknow/", data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter correct data")
        self.assertFalse(
            Booking.objects.filter(
                date=datetime.date(2023, 4, 2),
                time=datetime.time(10, 0),
                user=self.user,
            ).exists()
        )


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("create-post")

    def test_create_post_with_valid_data(self):
        self.client.login(username="testuser", password="testpass")
        data = {"title": "Test post", "content": "Lorem ipsum dolor sit amet."}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_create_post_with_invalid_data(self):
        self.client.login(username="testuser", password="testpass")
        data = {"title": "", "content": ""}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)

    def test_create_post_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_post_with_get_request(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIsInstance(form, CreatePostForm)
