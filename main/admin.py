from django.contrib import admin
from django.contrib.auth.models import Group
from .models import scheduletestmodel, feedbackmodel, studentdatamodel, uploadquestionpapermodel, resultmodel
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class scheduletestmodel_Admin(ImportExportModelAdmin):
    list_display = ('course', 'subjects', 'date', 'time', 'duration','questions','marks', )
    list_filter = ('course',)

class feedbackmodel_Admin(ImportExportModelAdmin):
    list_display = ('name','fname','email','feedback', )

class studentdatamodel_Admin(ImportExportModelAdmin):
    exclude = ('user', )
    list_display = ('course', 'branch', 'firstname', 'fname', 'category', 'phone', 'source', 'counsellor', )
    list_filter = ('course', 'branch', 'category',)

class uploadquestionpapermodel_Admin(ImportExportModelAdmin):
    list_display = ('qno', 'answer', 'subject', )

class resultmodel_Admin(ImportExportModelAdmin):
    list_display = ('email', 'name', 'fname', 'mobile', 'subject', 'marks', 'subject', )
    list_filter = ('subject',)

admin.site.site_header = 'GTC Administration'
admin.site.index_title = 'Scholarship Test'
admin.site.unregister(Group)

admin.site.register(scheduletestmodel, scheduletestmodel_Admin)
admin.site.register(feedbackmodel, feedbackmodel_Admin)
admin.site.register(studentdatamodel, studentdatamodel_Admin)
admin.site.register(uploadquestionpapermodel, uploadquestionpapermodel_Admin)
admin.site.register(resultmodel, resultmodel_Admin)