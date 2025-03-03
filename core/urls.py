"""
URL configuration for core project.

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
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('auth_app.urls')),
    path('api/users/', include('users_app.urls')),
    path('api/rooms/', include('room_app.urls')),
    path('api/chat/', include('chat_app.urls')),
    path('api/matches/', include('match_app.urls')),
    path('api/blockchain/', include('blockchain_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('spa.urls')),
    path("prometheus/", include("django_prometheus.urls")),
]
