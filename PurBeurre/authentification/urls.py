from django.urls import path
from django.contrib.auth.views import LogoutView
from authentification.views import LoginView, RegisterView, TemplateView
from purbeurre import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "authentification"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(template_name='products/home.html', next_page=None), name='logout'),
    path('account/', TemplateView.as_view(), name='account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(#1er page
        template_name="password/password_reset.html", #utilisateur
        email_template_name='password/password_reset_content.txt', #contenue du mail
        success_url=reverse_lazy('authentification:password_reset_done'),#a redéfinir
        subject_template_name='password/password_reset_subject.txt'),#sujet dans l'email
         name='reset_password'),#name
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(#just un template name - s'affiche "m'envoyer le mail"
        template_name="password/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(#reset mot de pass lui même
        template_name="password/password_reset_confirm.html",
        success_url=reverse_lazy('authentification:password_reset_complete')), #redirection url après
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(#pour dire bravo on a changé votre mot de passe.
        template_name="password/password_reset_complete.html"),
         name='password_reset_complete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
