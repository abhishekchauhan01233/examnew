from django.contrib import admin
from .models import scheduletestmodel, feedbackmodel, studentdatamodel, uploadquestionpapermodel, resultmodel
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(scheduletestmodel, feedbackmodel, studentdatamodel, uploadquestionpapermodel, resultmodel)

class ViewAdmin(ImportExportModelAdmin):
    pass

admin.site.site_header = 'GTC Administration'