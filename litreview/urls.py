"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

import authentication.views
import reviews.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", 
            redirect_authenticated_user=True
        ),
        name="login",
        ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup, name='signup'),
    path('home/', reviews.views.home, name='home'),
    path('ticket/create/', reviews.views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/',
         reviews.views.ticket_edit,
         name='ticket_edit',
         ),
    path('reviews/create_without_ticket/',
         reviews.views.review_without_ticket_create,
         name='review_without_ticket_create'),
    path('reviews/create_with_ticket/<int:ticket_id>/',
         reviews.views.review_with_ticket_create,
         name='review_with_ticket_create'),
    path('reviews/<int:review_id>/edit/',
         reviews.views.review_edit,
         name='review_edit'),
    path('follow/followership/',
         reviews.views.follow_user,
         name='follow_user'),
    path('follow/<int:follow_id>/delete/',
         reviews.views.unfollow_user,
         name='unfollow_user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
