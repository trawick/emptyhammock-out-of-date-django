from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html

from .models import Package, PackageVersion, PackageDBAccess
from .utils import staff_required
from .views import AdminExportDBView, ExportDBView, ImportDBView


class PackageVersionInline(admin.TabularInline):
    model = PackageVersion
    fields = ('version', 'type', )


class PackageAdmin(admin.ModelAdmin):
    change_list_template = 'e_ood_django/admin/package_change_list.html'
    inlines = (PackageVersionInline, )
    list_display = ('name', '_changelog_url', )
    readonly_fields = ('name_lower', )
    search_fields = ('name', )

    @staticmethod
    def _changelog_url(obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.changelog_url, obj.changelog_url
        )

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
            url(
                r'^admin_export_db/$',
                staff_required(AdminExportDBView.as_view()),
                name='{}_{}_admin_export_db'.format(
                    self.model._meta.app_label, self.model._meta.model_name
                )
            ),
        ] + urls


class PackageDBAccessAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'notes', )
    readonly_fields = ('uuid', '_url')
    fields = ('_url', 'uuid', 'notes')

    def get_queryset(self, request):
        setattr(self, 'saved_request', request)
        return super().get_queryset(request)

    def _url(self, obj):
        return self.saved_request.build_absolute_uri(
            reverse(
                'admin:e_ood_django_package_export_db',
                args=[obj.uuid]
            )
        )


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageDBAccess, PackageDBAccessAdmin)
