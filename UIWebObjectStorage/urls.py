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
from arvanBucket.views import *

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('home/', View_List, name='home'),
                  path('signup/', SignUp, name='signup'),
                  path('login/', Login, name='login'),
                  path('activate/<uidb64>/<token>/', activate, name='activate'),
                  path('delete/<int:pk>/', delete_row, name='delete_row'),
                  path('authenticate_bucket/', authenticate_bucket, name='create_bucket'),
                  path('create_bucket/', create_bucket, name='create_bucket'),
                  path('delete_bucket/', delete_bucket, name='delete_bucket'),
                  path('check_bucket/', check_bucket_entity, name='check_bucket'),
                  path('get_bucket_list/', check_bucket_list, name='get_bucket_list'),
                  path('get_bucket_policy/', get_bucket_policy, name='get_bucket_policy'),
                  path('upload/', object_upload_in_bucket, name='object_upload_in_bucket'),
                  path('change_bucket_access_policy/', change_bucket_access_policy, name='change_bucket_access_policy'),
                  path('download/', object_download_in_bucket, name='object_download_in_bucket'),
                  path('init/', init_bucket, name='init_bucket'),
                  path('delete/', object_delete_in_bucket, name='object_delete_in_bucket'),
                  path('modal/', uploadModal, name='modal'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
