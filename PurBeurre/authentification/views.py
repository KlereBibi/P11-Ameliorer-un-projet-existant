"""module returning the different views of the authentication"""

from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from authentification.forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model


class LoginView(auth_views.LoginView):

    """class returning the form login page
    return a login template"""

    form_class = LoginForm
    template_name = 'authentification/login.html'


class RegisterView(generic.CreateView):

    """class returning the form register page
    attach a register template
    if success return a login template"""

    form_class = RegisterForm
    template_name = 'authentification/register.html'
    success_url = reverse_lazy('authentification:login')


class TemplateView(auth_views.TemplateView):

    """class attach the user's account page"""

    template_name = "authentification/account.html"
