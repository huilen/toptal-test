from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # remove default fields
    username = None
    first_name = None
    last_name = None

    email = models.EmailField("Email address", unique=True)
    name = models.CharField(max_length=60)
    bio = models.TextField(blank=True)
    image = models.URLField(null=True, blank=True)

    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profile", args=[self.id])

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
