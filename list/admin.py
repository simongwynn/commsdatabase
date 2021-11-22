from django.contrib import admin
from .models import Contact, Event, Profile
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class export1(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('user','Event' )
    list_display = ['user']

class export2(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('event_name','')
    list_display = ('event_id', 'event_name')

class export3(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('contact_name', 'contact_organisation', 'contact_email', 'contact_mobile' )
    list_display = ('id', 'contact_name', 'contact_organisation', 'contact_email', 'contact_mobile',
                    'startlist','results','communiques','event')

admin.site.register(Profile, export1)
admin.site.register(Event, export2)
admin.site.register(Contact, export3)