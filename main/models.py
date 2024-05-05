from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
)
from django.utils.crypto import get_random_string, salted_hmac
import unicodedata

# \django\contrib\auth\validators.py

# '''
# full_name  describe   role   mssv  class_school  email   
# '''
class AbstractBaseUser(models.Model):
    password = models.CharField(_("password"), max_length=128)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        return self._get_session_auth_hash()

    def get_session_auth_fallback_hash(self):
        for fallback_secret in settings.SECRET_KEY_FALLBACKS:
            yield self._get_session_auth_hash(secret=fallback_secret)

    def _get_session_auth_hash(self, secret=None):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            secret=secret,
            algorithm="sha256",
        ).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
class ModAdmin(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=30, default=' ', unique=True)
    full_name = models.CharField(max_length=100)
    
    # describe = models.CharField(max_length=255)
    describe = RichTextField()

    MEMBER = 'Member'
    CORE_MEMBER = 'Core Member'
    MENTOR = 'Mentor'
    ALUMNI = 'Alumni'
    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (CORE_MEMBER, 'Core Member'),
        (MENTOR, 'Mentor'),
        (ALUMNI,'Alumni'),
    )
    
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=MEMBER)
    mssv = models.CharField(max_length=20)
    class_school = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    
    # image = models.ImageField(upload_to='main/static/img')
    image = models.CharField(max_length=5000)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
   
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # class Meta:
    #     verbose_name = _("user")
    #     verbose_name_plural = _("users")
    #     abstract = False
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s" % (self.full_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def __str__(self):
        return self.mssv

class Events(models.Model):
    id_event = models.AutoField(primary_key=True, auto_created=True)
    image_avatar = models.ImageField(upload_to='main/static/img')
    name_event = models.CharField(max_length=1000)
    content = RichTextField()
    time = models.DateField()
    id_user = models.ForeignKey(ModAdmin, on_delete=models.CASCADE, related_name='events')
    form_register = models.CharField(max_length=100, default="None")
    def __str__(self):
        return self.name_event


class Paper(models.Model):
    id_paper = models.AutoField(primary_key=True, auto_created=True)
    title = models.TextField(max_length=10000)
    author = models.TextField(max_length=10000)
    abstract = models.TextField(max_length=10000)
    link_paper = models.CharField(max_length=10000, default='None')
    link_github = models.CharField(max_length=10000, default='None')
    institute = models.CharField(max_length=255, default='None')
    interest = models.BooleanField(default=False)
    id_user = models.ForeignKey(ModAdmin, on_delete=models.CASCADE, related_name='papers')
    year = models.IntegerField()

    def __str__(self):
        return self.title
