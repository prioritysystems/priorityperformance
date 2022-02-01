from django.contrib import admin
from priorityapp.models import *

# Register your models here.

class PriorityPerformanceTeamAdmin(admin.ModelAdmin):
    list_display = ['full_names','profile_info']
    



class NominationDataAdmin(admin.ModelAdmin):
    list_display = ['sec_a_q1','sec_a_q2','sec_c_first_name','sec_c_surname',
    				'sec_c_cell_number','sec_c_email_address','nomination_year','last_updated']

    list_filter = ('nomination_year','sec_a_q2',) 

    model = NominationData

    exclude = ['aga_decision','aga_final_decision','nomination_ref','modal_ref',
    			'image_ref','nominee_image','timeline','sec_b_q1_1','sec_b_q1_2','sec_b_q3','sec_b_q5','sec_b_q5_1','sec_b_q5_2','sec_b_q6',
    			'sec_b_q6_1','sec_b_q6_2','sec_b_q6_3','sec_b_q7','sec_b_q8']

    #To include all fields
    # list_display = [field.name for field in NominationData._meta.get_fields()]



admin.site.register(NominationData,NominationDataAdmin)
admin.site.register(PriorityPerformanceTeam,PriorityPerformanceTeamAdmin)