from django.contrib import admin
from django.apps import apps

from .models import Profile,Question,Language,AnswerOptions,Stage,StudyMaterial
# Register your models here.

class StageAdmin(admin.StackedInline):
    model = Stage
    extra = 1

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    #fields = ['name',]
    inlines = [StageAdmin, ]
    model = Language
    list_display = ['name',]
    list_filter = ['name',]

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    #fields = ['stage','topic','text','audio',]
    model = StudyMaterial
    list_display = ['language','stage','topic','text','audio',]
    readonly_fields = ['date_created',]
    list_filter = ['topic','language','stage']
    

class AnswerOptionsAdmin(admin.StackedInline):
    model = AnswerOptions
    extra = 4
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['study_material','text',]
    model = Question
    inlines = [AnswerOptionsAdmin]
    list_display = ['study_material','text',]
    list_filter = ['study_material',]

admin.register(Stage, StageAdmin)
admin.register(StudyMaterial, StudyMaterialAdmin)
#admin.site.register(Language, LanguageAdmin)
admin.register(AnswerOptions, AnswerOptionsAdmin)
admin.register(Question, QuestionAdmin)
admin.register(Profile)

"""class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListAdminMixin,self).__init__(model,admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass',(ListAdminMixin, admin.ModelAdmin),{})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass"""