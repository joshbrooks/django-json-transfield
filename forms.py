from django import forms
from django.conf import settings

from . import models


def enlangished_class(base_form: forms.ModelForm) -> forms.ModelForm:
    """
    Enhances a 'Form' with additional fields based on settings languages
    """
    fields = base_form.Meta.translation_fields

    label = "json_languages_{prefix}".format(prefix="_".join(fields))
    language_fields = {}
    for field in fields:
        for langcode, langname in settings.LANGUAGES:
            fieldname = "%s_%s" % (field, langcode)
            language_fields[fieldname] = forms.CharField()

    return type(label, (base_form,), language_fields)


class TransModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for translated_field in self.Meta.translation_fields:

            # Find the initial value of the translated fields
            if kwargs.get("instance"):
                values = getattr(kwargs["instance"], translated_field) or {}
            else:
                values = {}

            for (langcode, langname) in settings.LANGUAGES:
                # Field names should be compatible with
                # JSON format ie {field}_{languuge}
                fieldname = "%s_%s" % (translated_field, langcode)
                self.fields[fieldname] = forms.CharField(
                    label="%s in %s" % (translated_field, langname),
                    required=False,
                    initial=values.get(langcode, ""),
                )

    def save(self, commit=True):
        for translated_field in self.Meta.translation_fields:
            translated = {}
            for (langcode, langname) in settings.LANGUAGES:
                fieldname = "%s_%s" % (translated_field, langcode)
                value = self.cleaned_data[fieldname]
                if value:
                    translated[langcode] = value
            setattr(self.instance, translated_field, translated)
        self.instance = super().save(commit=False)
        if commit:
            self.instance.save()
        return self.instance


class TranslatedFieldsTestModelForm(TransModelForm):
    class Meta:
        model = models.TranslatedFieldsTestModel
        fields = ("id",)
        translation_fields = "titles description".split()


TranslatedFieldsTestModelFormInstance = enlangished_class(TranslatedFieldsTestModelForm)
