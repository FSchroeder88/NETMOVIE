from msilib.schema import ListView
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from PIL import Image

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(email=self.normalize_email(email), username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.jpg"}'

def get_default_profile_image():
    return "static/images/default.png"

class User(AbstractBaseUser):

    email               = models.EmailField(verbose_name="email" , max_length=60, unique=True)
    username            = models.CharField(max_length=30, unique=True)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin            = models.BooleanField(default=True)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=True)
    is_superuser        = models.BooleanField(default=True)
    profile_image       = models.ImageField(upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=True)
    ordering = ('email',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']
    

    objects= AccountManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm , obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Cascade Delete profile when user is deleted
    image = models.ImageField(default=get_default_profile_image, null=True, blank=True, upload_to=get_profile_image_filepath)

    def __str__(self):
        return f'{self.user.username} Profile' 

def save(self, *args, **kwargs):
    super(Profile, self).save(*args, **kwargs)
    img = Image.open(self.image.path) # Open image
        
        # resize image
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size) # Resize image
        img.save(self.image.path) # Save it again and override the larger image

