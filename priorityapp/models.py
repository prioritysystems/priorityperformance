from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

from datetime import date


def upload_location(instance,filename):
       
    # current_date = datetime.date.today().strftime ("%d%m%Y")

    # return '{0}/{1}'.format('nominee_pictures/'+instance.nomination_ref,filename)
    return '{0}/{1}'.format(instance.image_ref,filename)


#Nominations Model
class NominationData(models.Model):

    #Section A
    sec_a_q1 = models.CharField(max_length=50,null=False,blank=False,verbose_name='Nominee-Full Names')
    profile_info = models.TextField(null=True,blank=True,verbose_name='Profile Info')
    timeline = models.CharField(max_length=60,null=True,blank=True,verbose_name='Nomination Timeline')
    sec_a_q2 = models.CharField(max_length=50,null=False,blank=False,verbose_name='Nominee-Country Of Residence')
    sec_a_q3 = models.CharField(max_length=50,null=False,blank=False,verbose_name='Relationship')
    sec_a_q3_other = models.TextField(max_length=100,null=True,blank=True,verbose_name='Relationship-Other')
    sec_a_q4 = models.CharField(max_length=10,null=False,blank=False,verbose_name='Gender')
    sec_a_q5 = models.TextField(max_length=10,null=False,blank=False,verbose_name='Ethnicity')
    sec_a_q6 = models.CharField(max_length=50,null=False,blank=False,verbose_name='City')

    #Section B
    sec_b_q1 = models.TextField(max_length=300,null=False,blank=False,verbose_name='Motivation')
    sec_b_q1_1 = models.CharField(max_length=100,null=False,blank=False,verbose_name='Skill Category')
    sec_b_q1_2 = models.TextField(max_length=100,null=False,blank=False,verbose_name='Clarity')
    sec_b_q2 = models.TextField(max_length=200,null=False,blank=False,verbose_name='Uniqueness')
    sec_b_q3 = models.CharField(max_length=3,null=False,blank=False,verbose_name='Rarity Score')
    sec_b_q3_1 = models.TextField(max_length=100,null=False,blank=False,verbose_name='Rarity Description')
    sec_b_q5 = models.TextField(max_length=200,null=False,blank=False)
    sec_b_q5_1 = models.TextField(max_length=200,null=False,blank=False)
    sec_b_q5_2 = models.TextField(max_length=200,null=False,blank=False)
    sec_b_q6 = models.CharField(max_length= 5,null=False,blank=False)
    sec_b_q6_1 = models.TextField(max_length=200,null=False,blank=False)
    sec_b_q6_2 = models.CharField(max_length= 5,null=False,blank=False)
    sec_b_q6_3 = models.TextField(max_length=200,null=False,blank=False)
    sec_b_q7 = models.TextField(max_length= 200,null=False,blank=False)
    sec_b_q8 = models.TextField(max_length=200,null=False,blank=False)
    nomination_ref = models.CharField(max_length=20,null=True,blank=True)
    modal_ref = models.CharField(max_length=20,null=True,blank=True)
    image_ref = models.CharField(max_length=20,null=True,blank=True)
    nominee_image = models.FileField(upload_to=upload_location,null=True,blank=True)
    
    #Section C: Nominator's details
    #auto_now_add=True adds the current datetime automatically when the instance is created
    sec_c_date_of_nomination = models.DateTimeField(auto_now_add=True)
    #auto_now=True adds the current datetime automatically when the instance is updated
    last_updated = models.DateTimeField(auto_now=True,verbose_name='Last Updated')
    sec_c_first_name = models.CharField(max_length= 50,null=False,blank=True,verbose_name='Nominator-Name')
    sec_c_surname = models.CharField(max_length= 50,null=False,blank=False,verbose_name='Surname')
    sec_c_country_of_residence = models.CharField(max_length= 50,null=False,blank=False,verbose_name='Residence')
    sec_c_citizenship = models.CharField(max_length= 50,null=False,blank=False,verbose_name='Citizenship')
    sec_c_contact_number = models.CharField(max_length= 12,null=False,blank=False,verbose_name='Contact Number')
    sec_c_cell_number = models.CharField(max_length= 12,null=False,blank=False,verbose_name='Cell Number')
    sec_c_email_address = models.CharField(max_length= 50,null=False,blank=False,verbose_name='Email Address')
    nomination_year = models.IntegerField(null=True,blank=True,verbose_name='Nomination Year')
    aga_decision = models.CharField(max_length=20,null=True,blank=True,verbose_name='AGA Decision')
    aga_final_decision = models.CharField(max_length=20,null=True,blank=True,verbose_name='AGA Final Deecision')

    #Sectio D: Disclaimer, see questionnaire
 

    def __str__(self):

        return str(self.sec_a_q1)


    class Meta:
        db_table = "aga_nomination"
        verbose_name_plural = "AGA Nomination Data"



"""
Signals to update db fields
"""
@receiver(pre_save,sender=NominationData)
def save_user(sender, instance,*args,**kwargs):


    """
    Update nomination_year when a nomination is submitted 
    or updated
    This method is more efficient that updating via views since
    both NominationFormView and view_update_nomination_info views 
    use the same NominationDatam model
    """

    get_last_award_year = NominationData.objects.filter(aga_final_decision='winner').last()

    nomination_year = get_last_award_year.nomination_year + 1

    set_nomination_year = nomination_year

    instance.nomination_year =  set_nomination_year

        
class PriorityPerformanceTeam(models.Model):
    full_names =  full_names = models.CharField(max_length=50,null=True,blank=True)
    profile_info = models.CharField(max_length=5000,null=True,blank=True)
    # profile_image

    class Meta:
        db_table = 'priority_team'

class PriorityPerformanceMessages(models.Model):
    full_names = models.CharField(max_length=50,null=True,blank=False)
    email_address = models.EmailField(max_length=100,null=True,blank=False)
    contact_number = models.CharField(max_length=30,null=True,blank=False)
    sent_message = models.TextField()
    message_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'priority_messages'


