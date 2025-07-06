from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    USER_TYPE_CHOICES = (
        
        ('shop', 'Shop'),
        ('individual', 'Individual'),
    )
    Name = models.CharField(max_length=255, blank=True, null=True)
    Wname = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    I_am_a = models.CharField(max_length=255, blank=True, null=True)
    experience_in_years = models.IntegerField(blank=True, null=True)
    
    
    def __str__(self):
        return self.username

    # Fixing the reverse accessor clash
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )


# Worker Model
class WorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    Name = models.CharField(max_length=255, blank=True, null=True)
    I_am_a = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    Other_skills = models.CharField(max_length=255, blank=True, null=True)
    experience_in_years = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

# Shop/Individual Model
class ShopOrIndividualProfile(models.Model):
    USER_TYPE_CHOICES = (
        
        ('shop', 'Shop'),
        ('individual', 'Individual'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='shop')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    Name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
