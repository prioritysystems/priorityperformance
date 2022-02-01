import django_filters
from django_filters import DateFilter,ChoiceFilter
from django import forms

from priorityapp.models import NominationData



class WinnersFilter(django_filters.FilterSet):

    """
    Filter AGA Winners by Year
    ChoiceFilter is a built-in class from the django_filters library
    it performs all the filtering
    django-filters has many types of filters
    """

    NOMINATION_YEAR_CHOICES = []

    nomination_years_list = NominationData.objects.values_list('nomination_year', flat=True)\
                            .order_by('id').distinct()

    for year_ in nomination_years_list:
        
        if year_ is not None:
            NOMINATION_YEAR_CHOICES.append((str(year_),str(year_)))

    #'Set' automatically removes duplicates from a list
    nomination_year = ChoiceFilter(choices=set(NOMINATION_YEAR_CHOICES),label='')
       
    class Meta:
        model = NominationData
        fields = ['nomination_year']




class NominationsFilter(django_filters.FilterSet):

    """
    Filter AGA Nominations by Year
    ChoiceFilter is a built-in class from the django_filters library
    it performs all the filtering
    django-filters has many types of filters
    """

    NOMINATION_YEAR_CHOICES = []

    nomination_years_list = NominationData.objects.values_list('nomination_year', flat=True)\
                            .order_by('nomination_year').distinct()

    for year_ in nomination_years_list:
        
        if year_ is not None:

            NOMINATION_YEAR_CHOICES.append((str(year_),str(year_)))
    
    
    #'Set' automatically removes duplicates from a list
    nomination_year = ChoiceFilter(choices=set(NOMINATION_YEAR_CHOICES),label='')
       
    class Meta:
        model = NominationData
        fields = ['nomination_year']


