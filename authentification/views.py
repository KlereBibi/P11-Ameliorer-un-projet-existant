"""module returning the different views of the authentication"""
from django.contrib.auth import views as auth_views
from authentification.forms import LoginForm, RegisterForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = "Lien d'activation pour votre enregistrement"
            message = render_to_string('confirmation/confirm_mail.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "confirmation/confirm_mail.html")
    else:
        form = RegisterForm()
    return render(request, 'authentification/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "confirmation/confirm_mail_done.html")
    else:
        return render(request, "confirmation/confirm_mail_invalid.html")


class LoginView(auth_views.LoginView):
    """class returning the form login page
    return a login template"""

    form_class = LoginForm
    template_name = 'authentification/login.html'


# class RegisterView(generic.CreateView):
#
#     """class returning the form register page
#     attach a register template
#     if success return a login template"""
#
#     form_class = RegisterForm
#     template_name = 'authentification/register.html'
#     success_url = reverse_lazy('authentification:login')


class TemplateView(auth_views.TemplateView):
    """class attach the user's account page"""

    template_name = "authentification/account.html"
