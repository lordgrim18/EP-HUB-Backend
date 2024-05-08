from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_('Enter a valid email address.'))
        
    def create_user(self, first_name, last_name, email, phone_number, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("an email address is required"))
        if not first_name:
            raise ValueError(_("first name is required"))
        if not last_name:
            raise ValueError(_("last name is required"))
        user = self.model(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone_number, first_name, last_name, password, **extra_fields):
        ## change superuser to admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        user = self.create_user(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, password=password, **extra_fields)
        user.save(using=self._db)
        return user