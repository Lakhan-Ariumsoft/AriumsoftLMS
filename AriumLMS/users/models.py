from django.contrib.auth.models import AbstractUser, Group, Permission,BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    # Custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Override the groups and user_permissions fields to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Avoid conflict with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Avoid conflict with auth.User.user_permissions
        blank=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Role Model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# UserRole Mapping
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')


# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.email}"

# JWT Token Model
class JWTToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jwt_tokens')
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"JWT Token for {self.user.email}"


# # Redis Cache Example (utility to invalidate cache)
# from django.core.cache import cache

# def invalidate_model_cache(instance, **kwargs):
#     model_name = instance.__class__.__name__.lower()
#     cache_key = f"{model_name}_{instance.pk}"
#     cache.delete(cache_key)

# # Signals for caching
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

# @receiver(post_save)
# @receiver(post_delete)
# def invalidate_cache_on_change(sender, instance, **kwargs):
#     invalidate_model_cache(instance)
