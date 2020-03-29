from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (AbstractUser, Group, Permission,
                                        PermissionsMixin, BaseUserManager)


class BasilUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        null=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    readonly = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []