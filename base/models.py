from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
# Create your models here.


# ======================================================
# Custom User Model
# Extends Django's AbstractUser
# ======================================================
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    ROLE_CHOICES = (
        ("author", "Author"),
        ("reader", "Reader"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    class Meta:
        swappable = 'AUTH_USER_MODEL'  


# ======================================================
# Category Model
# ======================================================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ======================================================
# Tag Model
# ======================================================

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# ======================================================
# Blog Post Model
# ======================================================
class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft")
    publication_date = models.DateTimeField(auto_now_add=True)



# ======================================================
# Comment Model (Threaded)
# ======================================================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    # Parent comment for nested threads
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    created_date = models.DateTimeField(auto_now_add=True)