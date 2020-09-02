from django.contrib import admin
from .models import Question, Language, AnswerOptions, Stage, StudyMaterial, Result, SearchQuery

admin.site.register(Result)
admin.site.register(SearchQuery)


class StageAdmin(admin.StackedInline):
    model = Stage
    extra = 1


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    # fields = ['name',]
    inlines = [StageAdmin, ]
    model = Language
    list_display = ['name', ]
    list_filter = ['name', ]


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    # fields = ['stage','topic','text','audio',]
    model = StudyMaterial
    list_display = ['stage', 'topic', 'text', 'audio', ]
    readonly_fields = ['date_created', ]
    list_filter = ['topic', ]


class AnswerOptionsAdmin(admin.StackedInline):
    model = AnswerOptions
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['study_material','text',]
    model = Question
    inlines = [AnswerOptionsAdmin]
    list_display = ['study_material', 'text', 'audio']
    list_filter = ['study_material', ]


admin.register(Stage, StageAdmin)
admin.register(StudyMaterial, StudyMaterialAdmin)
admin.register(AnswerOptions, AnswerOptionsAdmin)
admin.register(Question, QuestionAdmin)

