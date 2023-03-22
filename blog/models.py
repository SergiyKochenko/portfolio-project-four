from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from enum import unique
from django.core.validators import RegexValidator
from datetime import timedelta


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField("image", default="placeholder")
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)
    likes = models.ManyToManyField(User, related_name="blogpost_like", blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Service(models.Model):
    """The model is used to display data about the services
    provided by the community
    """

    service_name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = (
            "service_name",
            "price",
        )
        ordering = ["-price"]

    def __str__(self):
        return f"{self.service_name}, {self.price}"


HOURS = (
    ("10:00", "10:00"),
    ("10:30", "10:30"),
    ("11:00", "11:00"),
    ("11:30", "12:30"),
    ("12:00", "12:00"),
    ("12:30", "12:30"),
    ("13:00", "13:00"),
    ("13:30", "13:30"),
    ("14:00", "14:00"),
    ("14:30", "14:30"),
    ("15:00", "15:00"),
    ("15:30", "15:30"),
    ("16:00", "16:00"),
    ("16:30", "16:30"),
    ("17:00", "17:00"),
    ("17:30", "17:30"),
    ("18:00", "18:00"),
    ("18:30", "18:30"),
    ("19:00", "19:00"),
)


class Booking(models.Model):

    """Model that is used to store the data that the user enters in the
    booking form
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phoneRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$",
        message="Please enter a valid phone number,"
        "e.g. 123456789. Up to 15 digits allowed.",
        code="invalid",
    )
    phone = models.CharField(
        validators=[phoneRegex], max_length=16, null=True, blank=True
    )
    date = models.DateField()
    time = models.CharField(max_length=30, choices=HOURS, default="10:00")

    class Meta:
        unique_together = ("user", "date", "time", "service")

    def __str__(self):
        return self.name
