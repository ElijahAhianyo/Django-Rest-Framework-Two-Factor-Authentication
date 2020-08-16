from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password=None, **extra_fields):

        if not mobile:
            raise ValueError('mobile number must be provided')

        if not password:
            raise ValueError('Password must be provided')
        if 'email' in extra_fields:
            new_email = extra_fields.pop('email')
            email = self.normalize_email(new_email)
            print('second: ',extra_fields)
            extra_fields['email'] = email
            user = self.model(mobile=mobile, **extra_fields)
        else:
            user = self.model(mobile=mobile,**extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_active'] = True
        return self._create_user(mobile, password, **extra_fields)



class User(AbstractBaseUser):

    USERNAME_FIELD = 'mobile'
    email = models.EmailField('email', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(unique=True,validators=[phone_regex], max_length=17)
    title = models.CharField('title', blank=True, null=True, max_length=400)
    first_name = models.CharField('First Name', blank=True, null=True, max_length=400)
    last_name = models.CharField('Last Name', blank=True, null=True, max_length=400)
    other_name = models.CharField('Other Names', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    otp_token_uuid = models.CharField(max_length=70,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
