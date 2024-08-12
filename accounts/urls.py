from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    # Redirect to login after logout
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("home/", views.home, name="home"),  # Welcome page after login
    path("calculate_bmi/", views.calculate_bmi, name="calculate_bmi"),
    path("profile/", views.profile, name="profile"),
    path("add_workout", views.get_exercises, name="add_workout"),
]
