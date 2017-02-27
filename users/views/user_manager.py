from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, is_active=is_active, **extra_fields)
        user.set_password(password)
        user.set_confirmation_key(email)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        return self.create_user(email=email, password=password, is_staff=True, is_superuser=True, is_active=True, **kwargs)

    def create_user(self, email, password, is_staff=False, is_superuser=False, is_active=True, **kwargs):
        return self._create_user(email, password, is_staff, is_superuser, is_active, **kwargs)

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


