from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a regular user with email, username and password.
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a superuser with email, username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    # UUID as primary key (more secure than auto-incrementing integers)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Email is unique and used for authentication
    email = models.EmailField(unique=True)
    
    # Additional fields
    phone_number = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Email is the login field, not username
    USERNAME_FIELD = 'email'
    
    # Required fields when creating a user via createsuperuser
    REQUIRED_FIELDS = ['username']

    # Use our custom manager
    objects = UserManager()

    def __str__(self):
        return self.email
    

class Profile(models.Model):

    GENDER_CHOICES = [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ]

    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general_fitness', 'General Fitness'),
        ('strength_training', 'Strength Training'),
    ]
    FITNESS_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('elite', 'Elite')
    ]

    user = models.OneToOneField(
        User ,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True)

    # Fitness Info
    fitness_goal = models.CharField(max_length=50, choices=FITNESS_GOALS, blank=True)
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVELS, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Emergency Info
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

    # Preferences
    preferred_workout_time = models.CharField(max_length=50, blank=True)
    notification_preferences = models.JSONField(default=dict)  # Stores settings as JSON

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"