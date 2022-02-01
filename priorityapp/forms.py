from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field
from django.core.exceptions import ValidationError
from priorityapp.models import *
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
import random, string,datetime
from datetime import date


"""
Valid selection choices for countries
If the API choice doesn't match any of these, an error will be displayed for the user
"""
COUNTRY_CHOICES = [('','Select'),('Afghanistan','Afghanistan'),('Albania','Albania'),('Algeria','Algeria'),('Andorra','Andorra'),('Angola','Angola'),
('Antigua and Barbuda','Antigua and Barbuda'),('Argentina','Argentina'),('Armenia','Armenia'),('Australia','Australia'),
('Austria','Austria'),('Azerbaijan','Azerbaijan'),('Bahamas','Bahamas'),('Bahrain','Bahrain'),
('Bangladesh','Bangladesh'),('Barbados','Barbados'),('Belarus','Belarus'),('Belgium','Belgium'),
('Belize','Belize'),('Benin','Benin'),('Bhutan','Bhutan'),('Bolivia','Bolivia'),
('Bosnia and Herzegovina','Bosnia and Herzegovina'),('Botswana','Botswana'),('Brazil','Brazil'),('Brunei','Brunei'),
('Bulgaria','Bulgaria'),('Burkina Faso','Burkina Faso'),('Burundi','Burundi'),("Côte d'Ivoire","Côte d'Ivoire"),
('Cabo Verde','Cabo Verde'),('Cambodia','Cambodia'),('Cameroon','Cameroon'),('Canada','Canada'),
('Central African Republic','Central African Republic'),
('Chad','Chad'),('Chile','Chile'),('China','China'),('Colombia','Colombia'),('Comoros','Comoros'),
('Congo(Congo-Brazzaville)','Congo(Congo-Brazzaville)'),('Costa Rica','Costa Rica'),
('Croatia','Croatia'),('Cuba','Cuba'),('Cyprus','Cyprus'),('Czechia(Czech Republic)','Czechia(Czech Republic)'),
('Democratic Republic of the Congo','Democratic Republic of the Congo'),('Denmark','Denmark'),
('Djibouti','Djibouti'),('Dominica','Dominica'),('Dominican Republic','Dominican Republic'),('Ecuador','Ecuador'),
('Egypt','Egypt'),('El Salvador','El Salvador'),('Equatorial Guinea','Equatorial Guinea'),
('Eritrea','Eritrea'),('Estonia','Estonia'),('Eswatini','Eswatini'),('Ethiopia','Ethiopia'),('Fiji','Fiji'),
('Finland','Finland'),('France','France'),('Gabon','Gabon'),('Gambia','Gambia'),('Georgia','Georgia'),
('Germany','Germany'),('Ghana','Ghana'),('Greece','Greece'),('Grenada','Greece'),('Guatemala','Guatemala'),
('Guinea','Guatemala'),('Guinea-Bissau','Guinea-Bissau'),('Guyana','Guyana'),('Haiti','Haiti'),
('Holy See','Holy See'),('Honduras','Honduras'),('Hungary','Hungary'),('Iceland','Iceland'),('India','India'),
('Indonesia','Indonesia'),('Iran','Iran'),('Iraq','Iraq'),('Ireland','Ireland'),('Israel','Israel'),
('Italy','Italy'),('Jamaica','Jamaica'),('Japan','Japan'),('Jordan','Jordan'),('Kazakhstan','Kazakhstan'),
('Kenya','Kenya'),('Kiribati','Kiribati'),('Kuwait','Kuwait'),('Kyrgyzstan','Kyrgyzstan'),
('Laos','Laos'),('Latvia','Latvia'),('Lebanon','Lebanon'),('Lesotho','Lesotho'),('Liberia','Liberia'),
('Libya','Libya'),('Liechtenstein','Liechtenstein'),('Lithuania','Lithuania'),('Luxembourg','Luxembourg'),
('Madagascar','Madagascar'),('Malawi','Malawi'),('Libya','Libya'),('Malaysia','Malaysia'),('Maldives','Maldives'),('Mali','Mali'),('Malta','Malta'),
('Marshall Islands','Marshall Islands'),('Mauritania','Mauritania'),('Mauritius','Mauritius'),
('Mexico','Mexico'),('Micronesia','Micronesia'),('Moldova','Moldova'),('Monaco','Monaco'),('Mongolia','Mongolia'),
('Montenegro','Montenegro'),('Morocco','Morocco'),('Mozambique','Mozambique'),('Myanmar (formerly Burma)','Myanmar (formerly Burma)'),
('Namibia','Namibia'),('Nauru','Nauru'),('Nepal','Nepal'),('Netherlands','Netherlands'),('New Zealand','New Zealand'),
('Nicaragua','Nicaragua'),('Niger','Niger'),('Nigeria','Nigeria'),('North Korea','North Korea'),('North Macedonia','North Macedonia'),
('Norway','Norway'),('Oman','Oman'),('Pakistan','Pakistan'),('Palau','Palau'),('Palestine State','Palestine State'),
('Panama','Panama'),('Papua New Guinea','Papua New Guinea'),('Paraguay','Paraguay'),('Peru','Peru'),('Philippines','Philippines'),
('Poland','Poland'),('Portugal','Portugal'),('Qatar','Qatar'),('Romania','Romania'),('Russia','Russia'),('Rwanda','Rwanda'),
('Saint Kitts and Nevis','Saint Kitts and Nevis'),('Saint Lucia','Saint Lucia'),('Saint Vincent and the Grenadines','Saint Vincent and the Grenadines'),
('Samoa','Samoa'),('San Marino','San Marino'),('Sao Tome and Principe','Sao Tome and Principe'),('Saudi Arabia','Saudi Arabia'),
('Senegal','Senegal'),('Serbia','Serbia'),('Seychelles','Seychelles'),('Sierra Leone','Sierra Leone'),('Singapore','Singapore'),
('Slovakia','Slovakia'),('Slovenia','Slovenia'),('Solomon Islands','Solomon Islands'),('Somalia','Somalia'),('South Africa','South Africa'),
('South Korea','South Korea'),('South Sudan','South Sudan'),('Spain','Spain'),('Sri Lanka','Sri Lanka'),('Sudan','Sudan'),
('Suriname','Suriname'),('Sweden','Sweden'),('Switzerland','Switzerland'),('Syria','Syria'),('Tajikistan','Tajikistan'),
('Tanzania','Tanzania'),('Thailand','Thailand'),('Timor-Leste','Timor-Leste'),('Togo','Togo'),('Tonga','Tonga'),('Trinidad and Tobago','Trinidad and Tobago'),
('Tunisia','Tunisia'),('Turkey','Turkey'),('Turkmenistan','Turkmenistan'),('Tuvalu','Tuvalu'),('Uganda','Uganda'),('Ukraine','Ukraine'),
('United Arab Emirates','United Arab Emirates'),('United Kingdom','United Kingdom'),('United States of America','United States of America'),
('Uruguay','Uruguay'),('Uzbekistan','Uzbekistan'),('Vanuatu','Vanuatu'),('Venezuela','Venezuela'),('Vietnam','Vietnam'),('Yemen','Yemen'),
('Zambia','Zambia'),('Zimbabwe','Zimbabwe')]

NOMINEE_RELATIONSHIP_CHOICES = [('','Select'),('Family Member','Family Member'),('Friend','Friend'),('Co-worker','Co-worker'),
                        ('Business Associate','Business Associate'),('Mentor','Mentor'),('Nominating Myself','Nominating Myself'),('Other','Other')]

ETHNICITY_CHOICES = [('','Select'),('African','African'),('Coloured','Coloured'),('Indian/Asian','Indian/Asian'),('White','White'),('Other','Other')]

PROVINCE_CHOICES = [('','Select'),('Gauteng','Gauteng'),('Western Cape','Western Cape'),('Kwa-Zulu Natal','Kwa-Zulu Natal'),('Eastern Cape','Eastern Cape'),
                ('North West','North West'),('Limpopo','Limpopo'),('Mpumalanga','Mpumalanga'),('Free State','Free State'),
                ('Northern Cape','Northern Cape'),('Outside South Africa','Outside South Africa'),('Is late','Is late')]

#This included nominees that are late
TIME_PERIOD_CHOICES_OLD = [('','Select'),('1900 to 1950','1900 to 1950'),('1951 to 2000','1951 to 2000'),
                       ('2001 to 2010','2001 to 2010'),('Present day,after 2010','Present day,after 2010'),('1900 to 1950,Nominee is late','1900 to 1950,Nominee is late'),('1951 to 2000,Nominee is late','1951 to 2000,Nominee is late'),
                       ('2001 to 2010,Nominee is late','2001 to 2010,Nominee is late'),('Present day,after 2010,Nominee is late','Present day,after 2010,Nominee is late')]


TIME_PERIOD_CHOICES = [('','Select'),('1900 to 1950','1900 to 1950'),('1951 to 2000','1951 to 2000'),
                        ('2001 to Present','2001 to Present')]

#Create div for display errors
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return mark_safe('<div class="invalid-feedback">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self]))


class NominationForm(forms.ModelForm):
   
    sec_a_q1 = forms.CharField(label="Please provide the nominee’s full name")
    sec_a_q2 = forms.ChoiceField(choices=COUNTRY_CHOICES,label="Please state the nominee's Country of residence")
    sec_a_q3 = forms.ChoiceField(choices=NOMINEE_RELATIONSHIP_CHOICES,label="What is your relationship to the Nominee?")
    sec_a_q3_other = forms.CharField(widget=forms.Textarea,label="Please elaborate if other",required=False)
    sec_a_q4 = forms.ChoiceField(choices=[('','Select'),('Male','Male'),('Female','Female'),('Gender-neutral','Gender-neutral')],label="What is the gender of the nominee?")
    sec_a_q5 = forms.ChoiceField(choices=ETHNICITY_CHOICES,label="For statistical purposes please confirm the ethnic group of the nominee?")
    sec_a_q6 = forms.CharField(label="In which city is/was the nominee based?")

    """
    Fields sec_a_q7 sec_a_q7_1 were removed, no longer necessary
    Keep empty <divs> on the template in order to maintain the form's logic for sec_b_q6 selection
    """
    sec_b_q1 = forms.CharField(widget=forms.Textarea,label="Please state the main motivation behind your nomination?")
    sec_b_q1_1 = forms.CharField(widget=forms.Textarea,label="Advise on the skill category or type of skill that your nomination is based on?")
    sec_b_q1_2 = forms.CharField(widget=forms.Textarea,label="Please provide clarity and a definition of the unique skill recognised above?")
    sec_b_q2 = forms.CharField(widget=forms.Textarea,label="How easy is it for this unique skill to be recognised or appreciated by others and why?")
    sec_b_q3 = forms.IntegerField(label="If you were to score the rarity of this skill in the world out of 100 how would you score it’s rarity where 100 is extremely rare.",min_value=0,max_value=100)
    sec_b_q3_1 = forms.CharField(widget=forms.Textarea,label="If you were to describe the rarity of this skill in words,what would you say?")
    
    sec_b_q5 = forms.CharField(widget=forms.Textarea,label="Which important problem(s) within our society in Africa does this skill address?")
    sec_b_q5_1 = forms.CharField(widget=forms.Textarea,label="What is the importance of solving these types of problems within society compared to other problems?")
    sec_b_q5_2 = forms.CharField(widget=forms.Textarea,label="Please explain how the nominee has been able to apply this skill or unique talent to resolve problems?")
    
    sec_b_q6 = forms.ChoiceField(choices=[('','Select'),('Yes','Yes'),('No','No')],label="To your knowledge has the nominee influenced others to desire, possess and express the same skill or other skills?",required=False)
    sec_b_q6_1 = forms.CharField(widget=forms.Textarea,label="Please describe how the nominee has influenced others to desire, \
                                        possess and express the same or other skills they possess?",required=False)
    sec_b_q6_2 = forms.ChoiceField(choices=[('','Select'),('Yes','Yes'),('No','No')],
                                            label="Has the nominee trained and developed \
                                                protégés with the same skill or other skills?",required=False)
    sec_b_q6_3 = forms.CharField(widget=forms.Textarea,label="Please provide any information that explains how the nominee \
                                        has specifically trained and developed the skills and development of others?",required=False)
    sec_b_q7 = forms.CharField(widget=forms.Textarea,label="Please provide information on any professional or official recognition, \
                                        awards, and endorsements that the nominee has received that you are aware of?\
                                        STATE BODY AND YEAR OF RECOGNITION")
    sec_b_q8 = forms.CharField(widget=forms.Textarea,label="Please provide any other information that you feel might be important to support your nomination")
    nominee_image =  forms.FileField(required=False)
    sec_c_first_name = forms.CharField()
    sec_c_surname = forms.CharField()
    sec_c_country_of_residence = forms.ChoiceField(choices=COUNTRY_CHOICES)
    sec_c_citizenship = forms.CharField()
    sec_c_contact_number = forms.CharField()
    sec_c_cell_number = forms.CharField()
    sec_c_email_address = forms.EmailField()
    nomination_year = forms.IntegerField(required=False)


    def __init__(self, *args, **kwargs):
        super(NominationForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # self.fields['nomination_year'].label = ''
        
        #Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-group textinput textInputt form-control',}
            self.label_suffix = ""

    def clean_sec_a_q1(self):

        """
        The 'clean' method name should contain the field name as per models
        ie clean_sec_a_q1 or clean_sec_c_email_address etc
        """

        nominee_full_names = self.cleaned_data['sec_a_q1']

        # nominee_full_names_sorted = ' '.join(sorted(nominee_full_names.lower().split()))

        # print("nominee_full_names_sorted",nominee_full_names_sorted)

        #__icontains ~ like '%string%' case-insensitive
        # nominations_data = NominationData.objects.filter(sec_a_q1__icontains=nominee_full_names)

        # print('nominations_data',nominations_data)

        # for i in nominations_data:
        #     print("nominations_data",i.sec_a_q1,i.sec_a_q2)


        """
        Convert names to lowercase and append to list
        In case user enters name in with uppercases 
        """
        # names_list = [name.sec_a_q1.lower() for name in nominations_data]
        
        # print("names_list",names_list)

        # sorted_names_list = []
        # for name in names_list:
        #     sorted_names_list.append(' '.join(sorted(name.split())))

        # print("sorted_names_list",sorted_names_list)
        
        if NominationData.objects.filter(sec_a_q1__icontains=nominee_full_names):
            raise ValidationError(nominee_full_names + " has already been nominated.Only one nomination per nonimee is allowed.")

        return self.cleaned_data['sec_a_q1']

    class Meta:
        model = NominationData
        fields = '__all__'



class NominationUpdateForm(forms.ModelForm):
       
    sec_a_q1 = forms.CharField(label="Please provide the nominee’s full name")
    sec_a_q2 = forms.ChoiceField(choices=COUNTRY_CHOICES,label="Please state the nominee's Country of residence")
    sec_a_q3 = forms.ChoiceField(choices=NOMINEE_RELATIONSHIP_CHOICES,label="What is your relationship to the Nominee?")
    sec_a_q3_other = forms.CharField(widget=forms.Textarea,label="Please elaborate if other",required=False)
    sec_a_q4 = forms.ChoiceField(choices=[('','Select'),('Male','Male'),('Female','Female'),('Gender-neutral','Gender-neutral')],label="What is the gender of the nominee?")
    sec_a_q5 = forms.ChoiceField(choices=ETHNICITY_CHOICES,label="For statistical purposes please confirm the ethnic group of the nominee?")
    sec_a_q6 = forms.CharField(label="In which city is/was the nominee based?")
    
    #Remove time periods, no longer applicable
    # sec_a_q7 = forms.ChoiceField(choices=TIME_PERIOD_CHOICES,label="In which time period was the genius demonstrated?")
    # sec_a_q7_1 = forms.ChoiceField(choices=TIME_PERIOD_CHOICES,label="Besides the time period selected above, if applicable,\
                                                                        # please select another time period where the nominee demonstrated ingenuity.",required=False)
    sec_b_q1 = forms.CharField(widget=forms.Textarea,label="Please state the main motivation behind your nomination?")
    sec_b_q1_1 = forms.CharField(widget=forms.Textarea,label="Advise on the skill category or type of skill that your nomination is based on?")
    sec_b_q1_2 = forms.CharField(widget=forms.Textarea,label="Please provide clarity and a definition of the unique skill recognised above?")
    sec_b_q2 = forms.CharField(widget=forms.Textarea,label="How easy is it for this unique skill to be recognised or appreciated by others and why?")
    sec_b_q3 = forms.IntegerField(label="If you were to score the rarity of this skill in the world out of 100 how would you score it’s rarity where 100 is extremely rare.",min_value=0,max_value=100)
    sec_b_q3_1 = forms.CharField(widget=forms.Textarea,label="If you were to describe the rarity of this skill in words,what would you say?")
    
    sec_b_q5 = forms.CharField(widget=forms.Textarea,label="Which important problem(s) within our society in Africa does this skill address?")
    sec_b_q5_1 = forms.CharField(widget=forms.Textarea,label="What is the importance of solving these types of problems within society compared to other problems?")
    sec_b_q5_2 = forms.CharField(widget=forms.Textarea,label="Please explain how the nominee has been able to apply this skill or unique talent to resolve problems?")

    sec_b_q6 = forms.ChoiceField(choices=[('','Select'),('Yes','Yes'),('No','No')],label="To your knowledge has the nominee influenced others to desire, possess and express the same skill or other skills?",required=False)
    sec_b_q6_1 = forms.CharField(widget=forms.Textarea,label="Please describe how the nominee has influenced others to desire, \
                                        possess and express the same or other skills they possess?",required=False)
    sec_b_q6_2 = forms.ChoiceField(choices=[('','Select'),('Yes','Yes'),('No','No')],
                                            label="Has the nominee trained and developed \
                                                protégés with the same skill or other skills?",required=False)
    sec_b_q6_3 = forms.CharField(widget=forms.Textarea,label="Please provide any information that explains how the nominee \
                                        has specifically trained and developed the skills and development of others?",required=False)
    
    sec_b_q7 = forms.CharField(widget=forms.Textarea,label="Please provide information on any professional or official recognition, \
                                        awards, and endorsements that the nominee has received that you are aware of?\
                                        STATE BODY AND YEAR OF RECOGNITION")
    sec_b_q8 = forms.CharField(widget=forms.Textarea,label="Please provide any other information that you feel might be important to support your nomination")
    nominee_image =  forms.FileField(required=False)
    sec_c_first_name = forms.CharField()
    sec_c_surname = forms.CharField()
    sec_c_country_of_residence = forms.ChoiceField(choices=COUNTRY_CHOICES)
    sec_c_citizenship = forms.CharField()
    sec_c_contact_number = forms.CharField()
    sec_c_cell_number = forms.CharField()
    sec_c_email_address = forms.EmailField()
  

    def __init__(self, *args, **kwargs):
        super(NominationUpdateForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList
        
        #Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-group textinput textInputt form-control',}

    class Meta:
        model = NominationData
        exclude = ('nomination_ref',)


class ContactUsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.error_class = DivErrorList
        self.label_suffix = ""
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-group textinput textInput form-control',}
            self.fields[field].label = ''
        
        self.fields['full_names'].widget.attrs['placeholder'] = "Full Names*"
        self.fields['email_address'].widget.attrs['placeholder'] = "Email Address*"
        self.fields['contact_number'].widget.attrs['placeholder'] = "Contact Number*"
        self.fields['sent_message'].widget.attrs['placeholder'] = "Message*"
    class Meta:
        model = PriorityPerformanceMessages
        fields = '__all__'