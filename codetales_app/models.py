from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserRegistration(models.Model):
    Email=models.EmailField()
    Password=models.CharField(max_length=20)

class Profile(models.Model):
    user_registration = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)
    Email = models.EmailField()
    UserName = models.CharField(max_length=25, blank=True)
    DoB = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    Bio = models.TextField(blank=True)


@receiver(post_save, sender=UserRegistration)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Get the initial UserName from the UserRegistration instance
        initial_username = instance.Email.split('@')[0]  # Using part of the email as initial username
        Profile.objects.create(user_registration=instance, Email=instance.Email, UserName=initial_username)

class AdminRegistration(models.Model):
    UserName=models.CharField(max_length=25)
    Password=models.CharField(max_length=20)

class Feedback(models.Model):
    Name=models.CharField(max_length=25)
    Email=models.EmailField()
    Phone=models.CharField(max_length=10)
    Message=models.CharField(max_length=300)

class CStory(models.Model):
    Level=models.IntegerField()
    Page=models.IntegerField()
    Title=models.CharField(max_length=35,blank=True)
    Content=models.TextField()
    hasPuzzle=models.BooleanField(null=True,blank=True)
    PuzzleID=models.IntegerField(null=True,blank=True)

class PyStory(models.Model):
    Level=models.IntegerField()
    Page=models.IntegerField()
    Title=models.CharField(max_length=35,blank=True)
    hasPuzzle=models.BooleanField(null=True,blank=True)
    PuzzleID=models.IntegerField(null=True,blank=True)
    Content=models.TextField()

class Puzzle(models.Model):
    puzzleLanguage=models.CharField(max_length=10)
    puzzleID=models.IntegerField()
    puzzleDescription=models.TextField(null=True,blank=True)
    puzzleQuestion=models.TextField(null=True,blank=True)
    bookPageUrl=models.CharField(max_length=20)
    codeSnippet=models.TextField(null=True,blank=True)
    needsIP=models.BooleanField(null=True,blank=True)