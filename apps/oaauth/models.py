from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField


# Create your models here.

class UserStatusChoices(models.IntegerChoices):
    ACTIVATED = 1
    INACTIVATED = 2
    LOCKED = 3
class OAUserManager(BaseUserManager
                    ):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not realname:
            raise ValueError("The realname must be set")
        email = self.normalize_email(email)
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('status',UserStatusChoices.ACTIVATED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)




class OAUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    uid=ShortUUIDField(primary_key=True)
    realname = models.CharField(
        max_length=150,
        unique=False
    )
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(max_length=20, blank=True)
    is_staff = models.BooleanField(default=True)
    status = models.IntegerField(choices=UserStatusChoices, default=UserStatusChoices.INACTIVATED)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    department=models.ForeignKey('OADepartment', null=True,on_delete=models.SET_NULL,
                                 related_name='staffs',related_query_name='staffs')
    objects = OAUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["realname", 'password']


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        """Return the short name for the user."""
        return self.realname


class OADepartment(models.Model):
    name=models.CharField(max_length=100)
    intro=models.CharField(max_length=200)
    #leader
    leader=models.OneToOneField(OAUser,null=True, on_delete=models.SET_NULL,related_name="leader_department",
                                related_query_name='leader_department')
    manager=models.ForeignKey(OAUser,null=True, on_delete=models.SET_NULL,related_name="manager_departments",
                              related_query_name='manager_departments')


