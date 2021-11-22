"""contactlist URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from list import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginuser, name='loginuser'),#done
    path('logout/', views.logoutuser, name='logoutuser'),#na
    path('', views.home, name='home'),#na
    path('profile', views.userpage, name='profile'),
    path('<str:Event_id>/', views.eventpage, name='event'),#done
    path('<str:Event_id>/new/', views.new, name='new'),#done
    path('email', views.sendemail, name='email'),#done
    path('contact/<int:Contact_id>/', views.contact, name='contact'),#done
    path('contact/<int:Contact_id>/delete/', views.delete, name='delete'),#na
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)