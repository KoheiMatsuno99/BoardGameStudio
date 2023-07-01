"""
URL configuration for boardGameProject project.

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
from geister.views import move_piece, start_game, get_ready, cpu_move_piece

urlpatterns = [
    path("admin/", admin.site.urls),
    path("start/", start_game, name="start"),
    path("setup/", get_ready, name="setup"),
    path("movement/", move_piece, name="movement"),
    path("cpu-movement/", cpu_move_piece, name="cpu-movement"),
]
