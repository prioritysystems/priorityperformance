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

""""
Global dates
Used for opening and closing date counter
"""

current_year = date.today().year
todays_date = date.today()

#yyyy/mm/dd 
nominations_closing_date = datetime.datetime(current_year,1,31).date()
nominations_opening_date = datetime.datetime(current_year,8,1).date()

nominations_open = (todays_date <= nominations_closing_date ) or (todays_date  >= nominations_opening_date )

nominations_open_jan =  todays_date  <= nominations_closing_date
nominations_open_aug =  todays_date  >= nominations_opening_date

if nominations_open_jan:
    current_year = current_year
if nominations_open_aug:
    current_year = current_year  + 1
    
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

#Priority Performance Projects 
def priority_home(request):

    todays_date = date.today()

    current_year = date.today().year
    
    previous_year = current_year-1
    
    previous_opening_date = datetime.datetime(previous_year,8,1).date()
    
    current_opening_date = datetime.datetime(current_year,8,1).date()
    
    current_closing_date = datetime.datetime(current_year,1,31).date()

    # nominations_open = todays_date >= nominations_opening_date
    
    nominations_open = todays_date <= previous_opening_date and todays_date <= current_closing_date
    

    template = "priority-templates/home_priority_performance.html"

    context = {"nominations_open":nominations_open}

    return render(request,template,context)



#AGA: African Genius Award
def aga_home(request):
    
    template = "aga-templates/aga_home.html" 
    
    context = {"current_year":current_year,"todays_date":todays_date,"nominations_open":nominations_open}

    return render(request,template,context)



#AGA Nominations List
def aga_nominations_list(request):

    
    template = "aga-templates/nominations_list.html"

    current_year = date.today().year

    count_aga_winners =  NominationData.objects.filter(nomination_year=current_year).count()
    
    nominations_data = NominationData.objects.values('id','sec_a_q1','sec_a_q2','sec_b_q1',
                        'sec_c_date_of_nomination','image_ref','nominee_image',"modal_ref","nomination_year")
    
    """
    Always generate a unique modal ref number and update the modal to prevent from locking
    Fixed modal reference numbers were causing loading issues
    """
    for n in nominations_data:
        new_modal_ref = get_string(20,0)
        NominationData.objects.filter(id=n['id']).update(modal_ref=new_modal_ref)


    #Set the files path depending on the environment
    if settings.IS_DEV_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "priorityapp/static/bootstrap/assets/img/nominee_images/"))
    if settings.IS_PROD_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "static/bootstrap/assets/img/nominee_images/"))


    #Dynamic filtering by year, request.GET fetches the year from the URL and the the filtering form
    nomination_date_filter = WinnersFilter(request.GET, queryset=nominations_data)

    context = {"nominations_data":nominations_data,"count_aga_winners":count_aga_winners,
                "files":files,'nomination_date_filter': nomination_date_filter}


    return render(request,template,context)



#AGA Winners
def aga_honours(request):

    
    template = "aga-templates/aga_honours.html"

    current_year = date.today().year

    
    nominations_data = NominationData.objects.filter(aga_final_decision='winner')\
                        .values('id','sec_a_q1','sec_a_q2','sec_b_q1','timeline','profile_info','sec_c_date_of_nomination',
                            'image_ref','nominee_image',"modal_ref","nomination_year")
    
    """
    Always generate a unique modal ref number and update the modal to prevent from locking
    Fixed modal reference numbers were causing loading issues
    """
    for n in nominations_data:
        new_modal_ref = get_string(20,0)
        NominationData.objects.filter(id=n['id']).update(modal_ref=new_modal_ref)


    #Set the files path depending on the environment
    if settings.IS_DEV_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "priorityapp/static/bootstrap/assets/img/nominee_images/"))
    if settings.IS_PROD_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "static/bootstrap/assets/img/nominee_images/"))


    #Dynamic filtering by year, request.GET fetches the year from the URL and the the filtering form
    nomination_date_filter = WinnersFilter(request.GET, queryset=nominations_data)

    #Count winner for the selected year
    count_aga_winners = 0
    get_nomination_year = None
    for nomination in nomination_date_filter.qs:
        get_nomination_year  = nomination['nomination_year']

    count_aga_winners =  NominationData.objects.filter(nomination_year=get_nomination_year,aga_final_decision='winner').count()
    
    context = {"nominations_data":nominations_data,"count_aga_winners":count_aga_winners,
                "files":files,'nomination_date_filter': nomination_date_filter}


    return render(request,template,context)




#AGA Finalists
def aga_african_achievers(request):

    
    template = "aga-templates/aga_african_achievers.html"


    current_year = date.today().year

    get_year = request.GET.get('nomination_year')

    request.session['nomination_year'] = get_year

    
    nominations_data = NominationData.objects.filter(aga_decision='finalist')\
                        .values('id','sec_a_q1','sec_a_q2','timeline','profile_info','sec_b_q1','sec_c_date_of_nomination',
                            'image_ref','nominee_image',"modal_ref","nomination_year")
    

    """
    Always generate a unique modal ref number and update the modal to prevent from locking
    Fixed modal reference numbers were causing loading issues
    """
    for n in nominations_data:
        new_modal_ref = get_string(20,0)
        NominationData.objects.filter(id=n['id']).update(modal_ref=new_modal_ref)

    #Set the files path depending on the environment
    if settings.IS_DEV_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "priorityapp/static/bootstrap/assets/img/nominee_images/"))
    if settings.IS_PROD_ENVIRONMENT:
        files = os.listdir(os.path.join(settings.BASE_DIR, "static/bootstrap/assets/img/nominee_images/"))

    nomination_date_filter = WinnersFilter(request.GET, queryset=nominations_data)

    count_aga_finalists = 0
    get_nomination_year = None
    for nomination in nomination_date_filter.qs:
        get_nomination_year  = nomination['nomination_year']
    
    count_aga_finalists =  NominationData.objects.filter(nomination_year=get_nomination_year,aga_decision='finalist').count()
        
    context = {"nominations_data":nominations_data,"count_aga_finalists":count_aga_finalists,
                "files":files,"get_year":get_year,'nomination_date_filter': nomination_date_filter}

    
    
    return render(request,template,context)










class NominationFormView(FormView):

    """
    Using CBV to override POST method
    """
    form_class = NominationForm
    # success_url = reverse_lazy('viewNominations')

    template_name='aga-templates/aga_nomination_submission.html'
    
    if not nominations_open:
        template_name = "aga-templates/nominations_closed_error.html"
   

    def post(self, request):

        form = NominationForm(request.POST,request.FILES)

        context = {'form':form}


        if settings.IS_DEV_ENVIRONMENT:
            url_ = "http://127.0.0.1:8000/geniusinfo/"

        if settings.IS_PROD_ENVIRONMENT:
            url_ = "https://priorityperformance.co.za/geniusinfo/"

        """
        Nomination submission
        Send an email notication to the user and a vetting notification to the AGA administrator 
        """

        if form.is_valid():

            #Save form before committing it to the db and add the nomination year
        
            # form_instance = form.save(commit=False)
            # form_instance.nomination_year = set_nomination_year
            # form_instance.save()

            form.save()

            messages.success(request,".")

            full_names = form.cleaned_data.get('sec_c_first_name')
            nominee_full_names = form.cleaned_data.get('sec_a_q1')
            nominator_email_address = form.cleaned_data.get('sec_c_email_address')
            nomination_ref = form.cleaned_data.get('nomination_ref')

            subject = 'African Genius Awards'
            html_message = (
                f"Dear " + str(full_names) +","+ "\n \n"
                f"Thank you for submitting a nomination for "+ str(nominee_full_names) + "."
                f"Your nomination reference number is: "+ str(nomination_ref) + "\n \n"
                f"The nomination reference number SHOULD NOT be shared with anyone." + "\n \n"
                f"To view,change or upload a picture for the submitted nomination, please go to "+str(url_)+str(nomination_ref)+"/"+" "
                f"before " + str(nominations_closing_date) + "\n \n"
                f"Regards, \n"
                f"The A.G.A Team")

            html_message_vetting = (
                f"Good day ,"+ "\n \n"
                f"A nomination has been submitted for "+ str(nominee_full_names) + "."+ "\n \n"
                f"Please notify jasonm@plus94.co.za to provide the nomination details for vetting purposes." + "\n \n"
                f"Regards, \n"
                f"The A.G.A Team")

            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['aganominations@priorityperformance.co.za',nominator_email_address]
            recipient_list_vetting = ['noloyiso@plus94.co.za']
            recipient_list_vetting_2 = ['jasonm@plus94.co.za']

            send_mail(subject, html_message, from_email,recipient_list, fail_silently=True)
            # send_mail(subject, html_message_vetting, from_email,recipient_list_vetting, fail_silently=True)
            send_mail(subject, html_message_vetting, from_email,recipient_list_vetting_2, fail_silently=True)
       
            return redirect('viewNominations')
        
        else:

            for field in form.errors:
                
                form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
            
            print(" form.errors:", form.errors)
            messages.error(request,"There was a submission error, please check the form and resubmit.")
            

        # return render(request,template_name,context)


    def get_context_data(self,**kwargs):
    
        current_year = 2021

        next_year = current_year + 1

        #Parse form into context data to prevent error
        form = NominationForm(self.request.POST or None)

        #yyyy/mm/dd 
        nominations_closing_date = datetime.datetime(next_year,1,31).date()

        todays_date = date.today()

        nominations_open = todays_date <= nominations_closing_date

        context = {"nominations_open":nominations_open,"form":form,"next_year":next_year,"current_year":current_year}

        return context






#Priority Message Sent
def priority_message_sent(request):


    template = "priority-templates/priority_message_sent.html"

    
    context = {}

    return render(request,template,context)


#Nomination info can be viewed anytime
def view_update_nomination_info(request,get_nomination_ref):

    is_date_valid_for_update = nominations_open

    nominee = get_object_or_404(NominationData,nomination_ref=get_nomination_ref)

    form = NominationUpdateForm(request.POST or None,instance=nominee)

    if settings.IS_DEV_ENVIRONMENT:
        url_ = "http://127.0.0.1:8000/geniusinfo/"
    
    if settings.IS_PROD_ENVIRONMENT:
        url_ = "https://priorityperformance.co.za/geniusinfo/"

    """
    Only allow users to edit the form before the nominaton closing date
    """
    if is_date_valid_for_update:

        if request.method == 'POST':

            form = NominationUpdateForm(request.POST or None, request.FILES or None, instance=nominee)
            
            if form.is_valid():
                form.save()

                #Send confirm email
                full_names = form.cleaned_data.get('sec_c_first_name')
                nominee_full_names = form.cleaned_data.get('sec_a_q1')
                nominator_email_address = form.cleaned_data.get('sec_c_email_address')
                subject = 'African Genius Awards'
                html_message = (
                    f"Dear " + str(full_names) +","+ "\n \n"
                    f"Your nomination details for "+ str(nominee_full_names)+" "
                    f"have been updated, the nomination reference number is still: "+ str(get_nomination_ref) + "\n \n"
                    f"The nomination reference number SHOULD NOT be shared with anyone." + "\n \n"
                    f"To view,change or upload a picture for the submitted nomination, please go to "+str(url_)+str(get_nomination_ref)+"/"+" "
                    f"before " + str(nominations_closing_date) + "\n \n"
                    f"Regards, \n"  
                    f"The A.G.A Team")
                from_email = settings.EMAIL_HOST_USER
                recipient_list = ['aganominations@priorityperformance.co.za',nominator_email_address]
                send_mail(subject, html_message, from_email,recipient_list, fail_silently=True)
                return redirect ('viewNominations')

            else:

                for field in form.errors:
                    form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
                    print("Form Errors:",form.errors)
                    messages.error(request,"Error: One or more questions were not answered.\
                        Please make sure that all questions are answered and resubmit.")

    else:

        return redirect('nominationsClosedError')
        

    template = "aga-templates/nomination_view_update_info.html"

    if not nominations_open:
        template = "aga-templates/nominations_closed_error.html"
        
        

    nomination_data = NominationData.objects.filter(nomination_ref=get_nomination_ref)
    
    context ={"nomination_data":nomination_data,"form":form,"is_date_valid_for_update":is_date_valid_for_update,"nominee":nominee,"nominations_closing_date":nominations_closing_date} 

    return render(request,template,context)



#Not used in production
#Nomination vetting info can be viewed anytime
# def vetting_nomination(request,get_nomination_id):

#     current_year = date.today().year
#     todays_date = date.today()

#     nominations_closing_date = datetime.datetime(current_year,4,30).date()
   
#     is_date_valid_for_update = todays_date < nominations_closing_date

#     nominee = get_object_or_404(NominationData,nomination_ref=get_nomination_ref)

#     form = NominationUpdateForm(request.POST or None,instance=nominee)

#     if settings.IS_DEV_ENVIRONMENT:
#         url_ = "http://127.0.0.1:8000/geniusinfo/"
    
#     if settings.IS_PROD_ENVIRONMENT:
#         url_ = "https://priorityperformance.co.za/geniusinfo/"

#     if is_date_valid_for_update:
#         if request.method == 'POST':
#             form = NominationUpdateForm(request.POST or None, request.FILES or None, instance=nominee)
#             if form.is_valid():
#                 form.save()

#                 #Send confirm emails
#                 full_names = form.cleaned_data.get('sec_c_first_name')
#                 nominee_full_names = form.cleaned_data.get('sec_a_q1')
#                 nominator_email_address = form.cleaned_data.get('sec_c_email_address')
#                 nomination_ref = form.cleaned_data.get('nomination_ref')
#                 subject = 'African Genius Awards'
#                 html_message = (
#                     f"Dear " + str(full_names) +","+ "\n \n"
#                     f"Your nomination details for "+ str(nominee_full_names)+" "
#                     f"have been updated, the nomination reference number is still: "+ str(get_nomination_ref) + "\n \n"
#                     f"The nomination reference number SHOULD NOT be shared with anyone." + "\n \n"
#                     f"To view,change or upload a picture for the submitted nomination, please go to " + str(url_) + str(get_nomination_ref)+"/" + "\n "
#                     f"\n \n"
#                     f"Regards, \n"  
#                     f"The A.G.A Team")
#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = ['aganominations@priorityperformance.co.za',nominator_email_address]
#                 send_mail(subject, html_message, from_email,recipient_list, fail_silently=True)
#                 return redirect ('viewNominations')

#             else:
#                 for field in form.errors:
#                     form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
#                     print("Form Errors:",form.errors)
#                     messages.error(request,"Error: One or more questions were not answered.\
#                         Please make sure that all questions are answered and resubmit.")

#     template = "aga-templates/nomination_view_update_info.html"

#     nomination_data = NominationData.objects.filter(nomination_ref=get_nomination_ref)
    
#     context ={"nomination_data":nomination_data,"form":form,"is_date_valid_for_update":is_date_valid_for_update,"nominee":nominee,"nominations_closing_date":nominations_closing_date} 

#     return render(request,template,context)



"""
Countries API
safe parameter is set to 'False' to prevent serialzation error since 
JsonResponse only serializes dictionary objects 
and all_countries_list is a 'list' data type
"""
def countries_API(request):


    all_countries_list = ['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda',
                    'Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain',
                    'Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia',
                    'Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso',
                    'Burundi',"Côte d'Ivoire",'Cabo Verde','Cambodia','Cameroon','Canada','Central African Republic',
                    'Chad','Chile','China','Colombia','Comoros','Congo(Congo-Brazzaville)','Costa Rica','Croatia',
                    'Cuba','Cyprus','Czechia(Czech Republic)','Democratic Republic of the Congo','Denmark',
                    'Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea',
                    'Eritrea','Estonia','Eswatini','Ethiopia','Fiji','Finland','France','Gabon','Gambia','Georgia',
                    'Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti',
                    'Holy See','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel',
                    'Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kiribati','Kuwait','Kyrgyzstan','Laos',
                    'Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Madagascar',
                    'Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Mauritania','Mauritius','Mexico',
                    'Micronesia','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Myanmar (formerly Burma)',
                    'Namibia','Nauru','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria',
                    'North Korea','North Macedonia','Norway','Oman','Pakistan','Palau','Palestine State',
                    'Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Qatar',
                    'Romania','Russia','Rwanda','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines',
                    'Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Seychelles',
                    'Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa',
                    'South Korea','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland',
                    'Syria','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago',
                    'Tunisia','Turkey','Turkmenistan','Tuvalu','Uganda','Ukraine','United Arab Emirates','United Kingdom',
                    'United States of America','Uruguay','Uzbekistan','Vanuatu','Venezuela','Vietnam','Yemen','Zambia','Zimbabwe']

    return JsonResponse(list(all_countries_list),safe=False)


def error_404_view(request,exception):

    template = "priority-templates/404_error.html"

    context = {}

    return render(request,template,context)

def error_500_view(request):
    
    template = "priority-templates/500_error.html"

    context = {}

    return render(request,template,context)


def error_closed_nominations(request):
    
    template = 'aga-templates/nominations_closed_error.html'

    context = {}

    return render(request,template,context)