from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic.edit import FormView, View

from .forms import DBImportForm
from .models import Package, PackageDBAccess


class AnyExportDBView(View):

    @staticmethod
    def format_value(value):
        if isinstance(value, list):
            return '[' + ', '.join(value) + ']'
        else:
            return "'{}'".format(value)

    def get_yaml(self):
        d = Package.export()
        # This sucks, but I don't see a clean way to output this as desired
        # in a clean manner.  The best I found was
        #   https://gist.github.com/miracle2k/3184458
        # but it mutates yaml, potentially affecting other code.
        y = []
        for name in d.keys():
            y.append(name + ':')
            for k, value in d[name].items():
                y.append('  ' + k + ': ' + self.format_value(value))
        y = '\n'.join(y) + '\n'
        return y


class ExportDBView(AnyExportDBView):
    """
    Random clients can use this view as long as they have the magic
    UUID.
    """

    def get(self, request, uuid):
        get_object_or_404(PackageDBAccess, uuid=uuid)  # authorize client
        y = self.get_yaml()
        return HttpResponse(y)


class AdminExportDBView(AnyExportDBView):
    """
    Admin users can use this view from the button in admin.  The URL
    spec wraps this with a staff-user requirement.
    """

    def get(self, request):
        y = self.get_yaml()
        # no registered MIME type for YAML as of early 2018 AFAICT
        response = HttpResponse(content=y, content_type='text/x-yaml')
        suggested_filename = now().strftime('db-%Y-%m-%d.yaml')
        response['Content-Disposition'] = 'attachment; filename=%s' % suggested_filename
        return response


class ImportDBView(FormView):
    template_name = 'e_ood_django/admin/import_db.html'
    form_class = DBImportForm

    def get_success_url(self):
        app_label, object_name = 'e_ood_django', 'package'
        return reverse('admin:%s_%s_changelist' % (app_label, object_name))

    def form_valid(self, form):
        form.import_db()
        return super().form_valid(form)
