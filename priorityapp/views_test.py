from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from priorityapp.filters import WinnersFilter, NominationsFilter

from rest_framework.decorators import api_view

from .forms import NominationForm
from priorityapp.forms import *
from priorityapp.models import *
from datetime import date
import datetime,random,string
import os


#Generate a modal ref string
def get_string(letters_count, digits_count):
    
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = ''.join(sample_list)

    return final_string


def aga_social_media(request):
    
    template = "aga-templates/aga_social_media.html"

    current_year = date.today().year

    #yyyy/mm/dd 
    nominations_closing_date = datetime.datetime(current_year,3,31).date()

    nominations_opening_date = datetime.datetime(current_year,8,1).date()

    todays_date = date.today()

    nominations_open = todays_date >= nominations_opening_date

    context = {"curent_year":current_year,"nominations_open":nominations_open}

    return render(request,template,context)