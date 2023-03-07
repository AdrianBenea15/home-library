from django.conf import settings
from django.db import models
import uuid
import os

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


def book_image(instance, filename):
    return 'images/{0}.jpg'.format(instance.id)



def user_image(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'user', filename)


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save new superuser with details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255,
                              unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_image, default='profile/default/default.png')


    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class Category(models.Model):
    """Database model for category of books"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Editor(models.Model):
    """Database model for books editors"""
    editor_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.editor_name


class Books(models.Model):
    """Database models for books"""
    class Meta:
        verbose_name_plural = 'Books'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6,
        decimal_places=2)
    description = models.TextField(blank=True)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    release_date = models.DateField(blank=True, null=True)
    category = models.ManyToManyField('Category')
    image = models.ImageField(upload_to=book_image, null=True, blank=True)

    def __str__(self):
        return self.title + ', ' + str(self.id)


class ReadBooks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    book = models.OneToOneField(Books, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title + ', ' + self.book.author

    @property
    def book_title(self):
        return self.book.title + ', ' + self.book.author

    def book_image(self):
        if self.book.image:
            return self.book.image
