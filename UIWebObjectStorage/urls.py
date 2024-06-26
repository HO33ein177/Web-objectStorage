"""
URL configuration for UIWebObjectStorage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from objectStorage.views import *
from django.conf.urls.static import static
from UIWebObjectStorage import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('signup/', SignUp, name='signup'),
                  path('login/', Login, name='login'),
                  path('activate/<uidb64>/<token>/', activate, name='activate'),
                  path('delete/<int:pk>/', delete_row, name='delete_row'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
