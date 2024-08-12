from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SavedExercise, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    # Allow users to upload an avatar
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "avatar"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                UserProfile.objects.create(user=user, avatar=avatar)
            else:
                UserProfile.objects.create(user=user)
        return user


class BMICalculatorForm(forms.Form):
    weight = forms.FloatField(label="Weight (kg)", min_value=0)
    height = forms.FloatField(label="Height (m)", min_value=0)


class ExerciseForm(forms.Form):
    TYPE_CHOICES = [
        ('cardio', 'Cardio'),
        ('olympic_weightlifting', 'Olympic Weightlifting'),
        ('plyometrics', 'Plyometrics'),
        ('powerlifting', 'Powerlifting'),
        ('strength', 'Strength'),
        ('stretching', 'Stretching'),
        ('strongman', 'Strongman'),
    ]

    MUSCLE_CHOICES = [
        ('', 'Select Muscle (Optional)'),  # Allows the field to be blank
        ('abdominals', 'Abdominals'),
        ('abductors', 'Abductors'),
        ('adductors', 'Adductors'),
        ('biceps', 'Biceps'),
        ('calves', 'Calves'),
        ('chest', 'Chest'),
        ('forearms', 'Forearms'),
        ('glutes', 'Glutes'),
        ('hamstrings', 'Hamstrings'),
        ('lats', 'Lats'),
        ('lower_back', 'Lower Back'),
        ('middle_back', 'Middle Back'),
        ('neck', 'Neck'),
        ('quadriceps', 'Quadriceps'),
        ('traps', 'Traps'),
        ('triceps', 'Triceps'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    exercise_type = forms.ChoiceField(
        choices=TYPE_CHOICES, widget=forms.Select)
    muscle_group = forms.ChoiceField(
        choices=MUSCLE_CHOICES, widget=forms.Select, required=False)
    difficulty_level = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES, widget=forms.Select)


class SaveExerciseForm(forms.ModelForm):
    class Meta:
        model = SavedExercise
        fields = []
