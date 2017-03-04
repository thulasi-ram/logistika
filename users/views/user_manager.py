from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        username = self.generate_unique_username(email, **extra_fields)

        return self._create_user(username, email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        username = self.generate_unique_username(email, **extra_fields)
        return self._create_user(username, email, password, **extra_fields)

    def generate_unique_username(self, email, extra_fields):
        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')
        if first_name and last_name:
            base_username = '{first_name}{last_name}'.format(first_name=first_name, last_name=last_name)
        else:
            base_username = email.split('@')[0]
        i = 0
        while get_user_model().objects.filter(username=base_username).exists():
            if i:
                base_username = '{usrname}{i}'.format(usrname=base_username, i=i)
            i += 1
        return base_username

    def filter(self, **kwargs):
        if 'username' in kwargs:
            kwargs['username__iexact'] = kwargs['username']
            del kwargs['username']
        return super(CustomUserManager, self).filter(**kwargs)

    def get(self, **kwargs):
        if 'username' in kwargs:
            kwargs['username__iexact'] = kwargs['username']
            del kwargs['username']
        return super(CustomUserManager, self).get(**kwargs)
