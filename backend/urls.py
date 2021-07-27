"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ots.views import UserView, SessionView, ParticipationView, MessageView
from rest_framework.authtoken import views
from ots import urls
router = DefaultRouter()
router.register('ots/users', UserView, basename="User")
router.register('ots/sessions', SessionView, basename="Session")
router.register('ots/participation', ParticipationView, basename="Participation")
router.register('ots/messages', MessageView, basename="Message")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('user/', include(urls))
]
