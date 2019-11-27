from django.contrib.postgres.fields import JSONField


class TranslatedFieldsTestModel(models.Model):
    titles = JSONField(null=True, blank=True)
    description = JSONField(null=True, blank=True)
