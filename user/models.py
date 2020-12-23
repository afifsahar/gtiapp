from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
import PIL
from PIL import Image, ImageDraw
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        # extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_admin') is not True:
        #     raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=50, unique=True)
    email = models.EmailField(_('email address'))
    phone = models.IntegerField(
        _('phone number'), unique=True, blank=True, null=True)
    # mother_name = models.CharField(max_length=50,verbose_name="Mother's name", blank=True, null=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    objects = UserManager()
    qr_code = models.ImageField(
        upload_to='qr_code', blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,)
        qr.add_data("{0}".format(self.first_name))
        qrcode_img = qrcode.make(qr)
        canvas = Image.new('RGB', (qrcode_img.pixel_size,
                                   qrcode_img.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'code-of-{self.username}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    #     # For checking permissions. to keep it simple all admin have ALL permissons

    #     def has_perm(self, perm, obj=None):
    #         return self.is_admin

    #     # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    #     def has_module_perms(self, app_label):
    #         return True


class user_profile(models.Model):
    userProfile = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userProfile", verbose_name="User Profile", null=True, blank=True)
    userPhoto = models.ImageField(upload_to='images/profile/', null=True, name="userPhoto",
                                  blank=True, default='images/square6.jpg', verbose_name="User Profile Photo")

    def __str__(self):
        return f'{self.userProfile.username} Profile'

    def save(self, *args, **kwargs):
        super(user_profile, self).save(*args, **kwargs)
        pho = Image.open(self.userPhoto.path)
        if pho.height > 300 or pho.width > 300:
            output_size = (300, 300)
            pho.thumbnail(output_size)
            pho.save(self.userPhoto.path)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


class user_bri_image(models.Model):
    image_name = models.CharField(
        blank=True, null=True, verbose_name="Image Name", name="imageName", max_length=50)
    image_bri = models.ImageField(upload_to='images', null=True, name="briImage",
                                  blank=True, default='images/bri-logo.png', verbose_name="BRI Image")

    def __str__(self):
        return f'{self.imageName}'

    def save(self, *args, **kwargs):
        super(user_bri_image, self).save(*args, **kwargs)
        pho = Image.open(self.briImage.path)
        if pho.height > 300 or pho.width > 300:
            output_size = (300, 300)
            pho.thumbnail(output_size)
            pho.save(self.briImage.path)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Bri Image'
        verbose_name_plural = 'Bri Images'
