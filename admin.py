from django.contrib import admin

from . import forms, models


@admin.register(models.TranslatedFieldsTestModel)
class TranslatedFormTest(admin.ModelAdmin):
    form = forms.TranslatedFieldsTestModelFormInstance
