"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""


from django.conf.urls import *
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from accounts.views import ActivationView,RegistrationView,UserUpdateView,ChangePasswordView,UserProfileView,AllExamsView, AllQuestionsView

from numbas import settings



urlpatterns = patterns('',
                       url(r'^password/change/$',
                           auth_views.password_change,
                           name='auth_password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^profile/(?P<pk>\d+)/$',
                           UserProfileView.as_view(),
                           name='view_profile'),
                       url(r'^profile/edit$',
                           login_required(UserUpdateView.as_view()),
                           name='edit_profile'),
                       url(r'^profile/backup/all-exams$',
                           login_required(AllExamsView.as_view()),
                           name='all_exams_download'),
                       url(r'^profile/backup/all-questions$',
                           login_required(AllQuestionsView.as_view()),
                           name='all_questions_download'),
                       )

if settings.CAN_CHANGE_PASSWORD:
    urlpatterns += patterns('',
                           url(r'^profile/change-password$',
                               login_required(ChangePasswordView.as_view()),
                               name='change_password'),
                           )

if settings.ALLOW_REGISTRATION:
    urlpatterns += patterns('',
                           url(r'^activate/complete/$',
                               TemplateView.as_view(template_name='registration/activation_complete.html'),
                               name='registration_activation_complete'),

                           # Activation keys get matched by \w+ instead of the more specific
                           # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                           # that way it can return a sensible "invalid key" message instead of a
                           # confusing 404.
                           url(r'^activate/(?P<activation_key>\w+)/$',
                               ActivationView.as_view(),
                               name='registration_activate'),
                           url(r'^register/$',
                               RegistrationView.as_view(),
                               {'backend': 'accounts.backend.Backend'},
                               name='registration_register'),
                           url(r'^register/complete/$',
                               TemplateView.as_view(template_name='registration/registration_complete.html'),
                               name='registration_complete'),
                           url(r'^register/closed/$',
                               TemplateView.as_view(template_name='registration/registration_closed.html'),
                               name='registration_disallowed'),
                           url(r'^register/after-first-login/$',
                               TemplateView.as_view(template_name='registration/after_first_login.html'),
                               name='after_first_login'),
                           )


