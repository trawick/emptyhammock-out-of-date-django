from django import forms
from django.db import transaction
import yaml

from .models import Package


class DBImportForm(forms.Form):
    db_file = forms.FileField(
        required=True, label='YAML-formatted package db',
        help_text='This db will replace the current package db.')

    def clean_db_file(self):
        db_file = self.cleaned_data['db_file']
        setattr(
            self,
            'packages',
            yaml.load(
                db_file,
                # some version numbers, such as "2.0", look like float; disable
                # auto-conversion so that all version numbers are strings
                Loader=yaml.BaseLoader
            )
        )

    def import_db(self):
        replace_all = True
        with transaction.atomic():
            if replace_all:
                Package.objects.all().delete()
            for k, v in self.packages.items():
                Package.import_from_dict(k, v)
