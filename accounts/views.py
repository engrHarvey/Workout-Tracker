from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, BMICalculatorForm, ExerciseForm, SaveExerciseForm
from django.contrib.auth.decorators import login_required
import requests
from .models import BMIRecord, SavedExercise, UserProfile
from django.contrib import messages
import os
from dotenv import load_dotenv

load_dotenv()


# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for the user
            login(request, user)
            # redirect to the home page or any other page
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to the home page or any other page
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def home(request):
    return render(request, "accounts/home.html")


@login_required
def profile(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Create a UserProfile if it does not exist
            user_profile = UserProfile.objects.create(user=request.user)

        saved_exercises = SavedExercise.objects.filter(
            user=request.user).order_by('-date_executed')
        bmi_records = BMIRecord.objects.filter(
            user=request.user).order_by('-date_recorded')

        return render(request, 'accounts/profile.html', {
            'user_profile': user_profile,
            'bmi_records': bmi_records,
            'saved_exercises': saved_exercises
        })
    else:
        return redirect('login')


@login_required
def calculate_bmi(request):
    bmi = None
    weight_category = None

    if request.method == "POST":
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']

            # Calculate BMI
            bmi = weight / (height ** 2)

            # Fetch weight category from API
            url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/weight-category"
            querystring = {"bmi": str(bmi)}

            headers = {
                "x-rapidapi-key": os.getenv('x-rapidapi-key'),
                "x-rapidapi-host": "body-mass-index-bmi-calculator.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            weight_category = response.json().get("weightCategory")

            # Save the record to the database
            if request.user.is_authenticated:
                BMIRecord.objects.create(
                    user=request.user,
                    bmi=bmi,
                    weight_category=weight_category
                )

    else:
        form = BMICalculatorForm()

    return render(request, 'accounts/calculate_bmi.html', {'form': form, 'bmi': bmi, 'weight_category': weight_category})


def fetch_image_from_google(exercise_name):
    api_key = os.getenv('YOUR_GOOGLE_CUSTOM_SEARCH_API_KEY')
    cse_id = os.getenv('YOUR_CUSTOM_SEARCH_ENGINE_ID')

    url = f"https://www.googleapis.com/customsearch/v1?q={
        exercise_name}&searchType=image&key={api_key}&cx={cse_id}&num=1"

    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        return data['items'][0]['link']  # Return the URL of the first image
    else:
        return None  # Or return a default image URL


@login_required
def get_exercises(request):
    exercises = []
    save_form = None
    form = ExerciseForm()  # Initialize the form here to ensure it's always available

    if request.method == 'POST':
        if 'search' in request.POST:
            form = ExerciseForm(request.POST)
            if form.is_valid():
                exercise_type = form.cleaned_data['exercise_type']
                muscle_group = form.cleaned_data.get('muscle_group', '')
                difficulty_level = form.cleaned_data['difficulty_level']

                url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"
                querystring = {"type": exercise_type,
                               "difficulty": difficulty_level}

                if muscle_group:
                    querystring["muscle"] = muscle_group

                headers = {
                    "x-rapidapi-key": os.getenv('x-rapidapi-key'),
                    "x-rapidapi-host": "exercises-by-api-ninjas.p.rapidapi.com"
                }

                response = requests.get(
                    url, headers=headers, params=querystring)
                # Ensure response content is decoded as UTF-8
                response.encoding = 'UTF-8'

                exercises = response.json()
                # Fetch image URLs for each exercise
                for exercise in exercises:
                    image_url = fetch_image_from_google(exercise['name'])
                    exercise['image_url'] = image_url if image_url else "URL_TO_DEFAULT_IMAGE"

                save_form = SaveExerciseForm()
        elif 'save' in request.POST:
            save_form = SaveExerciseForm(request.POST)
            if save_form.is_valid():
                exercise_name = request.POST.get('exercise_name')
                exercise_type = request.POST.get('exercise_type')
                muscle_group = request.POST.get('muscle_group')
                difficulty_level = request.POST.get('difficulty_level')

                saved_exercise = SavedExercise(
                    user=request.user,
                    name=exercise_name,
                    exercise_type=exercise_type,
                    muscle_group=muscle_group,
                    difficulty_level=difficulty_level
                )
                saved_exercise.save()

                messages.success(request, f"Exercise '{
                                 exercise_name}' saved successfully!")

    return render(request, 'accounts/exercise_list.html', {
        'form': form,  # This ensures 'form' is passed to the template even if the POST request wasn't valid
        'exercises': exercises,
        'save_form': save_form
    })
