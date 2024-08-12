from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bmi = models.FloatField()
    weight_category = models.CharField(max_length=100)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bmi} ({self.weight_category})"


class SavedExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    exercise_type = models.CharField(max_length=50)
    muscle_group = models.CharField(max_length=50, blank=True)
    difficulty_level = models.CharField(max_length=50)
    date_executed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.exercise_type}) - {self.difficulty_level} on {self.date_executed}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.jpg', blank=True)

    def __str__(self):
        return self.user.username
