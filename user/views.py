from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistration
from .forms import LoginForm


def home(request):
    return render(request, "home.html")


def register(request):

    if request.method == "POST":

        form = UserRegistration(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Account Created Successfully"
            )

            login(request, user)

            if user.role == "teacher":
                return redirect("teacher_dashboard")

            elif user.role == "parent":
                return redirect("parent_dashboard")

    else:

        form = UserRegistration()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )





def user_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                # DJANGO ADMIN
                if user.is_superuser:

                    return redirect("/admin/")


                # MANAGER LOGIN
                elif user.role == "manager":

                    return redirect("manager_dashboard")


                # TEACHER LOGIN
                elif user.role == "teacher":

                    return redirect("teacher_dashboard")


                # PARENT LOGIN
                elif user.role == "parent":

                    return redirect("parent_dashboard")


            else:

                messages.error(
                    request,
                    "Invalid Username or Password"
                )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


def user_logout(request):

    logout(request)

    return redirect("home")