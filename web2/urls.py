"""web2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import statistics
from django.contrib import admin
from django.urls import path,include
from . import settings
from . import views

app_name = 'web2'

urlpatterns = [
    path('members/', include('members.urls')),
    path('ascii/', include('ascii.urls')),
    path("admin/", admin.site.urls),
    path('',views.home,name="home"),
    #path('', include('pwa.urls'))
    
] 
#+ statistics(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


'''# only in development
if settings.DEBUG:
    urlpatterns += statistics(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
'''