from django.conf.urls import url
from django.contrib import admin

from .models import Package, PackageVersion, PackageDBAccess
from .utils import staff_required
from .views import ExportDBView, ImportDBView


class PackageVersionInline(admin.TabularInline):
    model = PackageVersion


class PackageAdmin(admin.ModelAdmin):
    change_list_template = 'e_ood_django/admin/package_change_list.html'
    inlines = (PackageVersionInline, )
    readonly_fields = ('name_lower', )
    search_fields = ('name', )

    def get_urls(self):
        urls = super().get_urls()
        return [
            url(
                r'^import_db/$',
                staff_required(ImportDBView.as_view()),
                name='{}_{}_import_db'.format(
                    self.model._meta.app_label, self.model._meta.model_name
                )
            ),
            url(
                r'^export_db/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
                ExportDBView.as_view(),
                name='{}_{}_export_db'.format(
                    self.model._meta.app_label, self.model._meta.model_name
                )
            ),
        ] + urls


class PackageDBAccessAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'notes', )
    readonly_fields = ('uuid', )


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageDBAccess, PackageDBAccessAdmin)
