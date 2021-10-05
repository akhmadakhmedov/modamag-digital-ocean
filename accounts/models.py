from django.core.exceptions import RequestAborted
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, name, surname, phone_number, password):
        if not phone_number:
            raise ValueError('User must have a phone number')

        user = self.model(
                name = name,
                surname = surname,
                phone_number = phone_number,
            )
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_superuser(self, name, surname, phone_number,  password):
        user = self.create_user(
            name = name,
            surname = surname,
            phone_number = phone_number,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self.db)
        return user


class Account(AbstractBaseUser):
    name            = models.CharField(max_length=20)
    surname         = models.CharField(max_length=20)
    email           = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    phone_number    = models.CharField(max_length=14, unique=True)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [ 'name', 'surname']

    objects = MyAccountManager()

    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, object = None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class forgotPassword(models.Model):
    name            = models.CharField(max_length=100, verbose_name="Имя")
    surname         = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_number    = models.CharField(max_length=50, verbose_name="Телефон номер")

    def __str__(self):
        return self.phone_number

class UserProfile(models.Model):
    user            = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1  = models.CharField(max_length=100, blank=True)
    address_line_2  = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to = 'images/users/')
    city            = models.CharField(max_length=20, blank=True)
    state           = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"