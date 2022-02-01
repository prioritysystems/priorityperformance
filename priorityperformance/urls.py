"""priorityperformance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from priorityapp.views import *
from priorityapp import views
from django.views.generic import RedirectView

urlpatterns = [
    path('priority/admin/', admin.site.urls),
    path('',priority_home,name="priorityHome"),
    path('africangenius/',aga_home,name='agraHome'),
    path('countries/',countries_API,name='countriesAPI'),
    path('aga/nominate/',views.NominationFormView.as_view(), name='agraNomination'),
    path('aga/nominations/',aga_nominations_list,name="viewNominations"),
    path('aga/outstanding-african-achievers/',aga_african_achievers,name="viewAGAFinalists"),
    path('aga/honours/',aga_honours,name="viewAGAHonours"),
    path('geniusinfo/<str:get_nomination_ref>/',view_update_nomination_info),
    path('message-sent/',priority_message_sent,name="messageSent"),
    path('aga/nominations-closed/',error_closed_nominations,name="nominationsClosedError"),
]

handler404 = 'priorityapp.views.error_404_view'
handler500 = 'priorityapp.views.error_500_view'