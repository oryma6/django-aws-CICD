from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Task, Project
from .forms import SignupForm

# Create your views here.

INDEX_PAGE : str = "app/index.html"
SIGNUP_PAGE : str = "app/signup.html"
LOGIN_PAGE : str = "app/login.html"
HOME_PAGE : str = "app/home.html"

def index(request):
    return render(request, INDEX_PAGE)

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # Hash the password
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()

    return render(request, SIGNUP_PAGE, {
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # this method automatically saves the user's ID into the session
            return redirect("home")
        else:
            return render(request, LOGIN_PAGE, {
                "message": "Invalid credentials."
        })
    try:
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, LOGIN_PAGE)
    except:
        return render(request, LOGIN_PAGE, {
            "message": "Session Stopped"
        })
    
def logout_view(request):
    logout(request)
    return render(request, LOGIN_PAGE, {
        "message": "Logged out"
    })

@login_required
def home(request):
    if not request.user.is_authenticated: # works because Django attaches the logged-in user to request.user using the session cookie.
        return redirect("login")
    
    tasks = Task.objects.filter(user=request.user).select_related("project").order_by("due_date")
    return render(request, HOME_PAGE, {
        "tasks": tasks
    })