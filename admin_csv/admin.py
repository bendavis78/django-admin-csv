from functools import update_wrapper

from django.contrib.admin.utils import label_for_field
from django.contrib.admin.views.main import SEARCH_VAR


class CSVMixin(object):
    """
    Adds a CSV export action to an admin view.
    """

    change_list_template = "admin/change_list_csv.html"

    # This is the maximum number of records that will be written.
    # Exporting massive numbers of records should be done asynchronously.
    csv_record_limit = None
    csv_fields = []

    def get_csv_fields(self, request):
        return self.csv_fields or self.list_display

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        opts = self.model._meta
        urlname = '{0.app_label}_{0.model_name}_csvdownload'.format(opts)
        urlpatterns = [
            url('^csv/$', wrap(self.csv_export), name=urlname)
        ]
        return urlpatterns + super(CSVMixin, self).get_urls()

    def csv_export(self, request, *args, **kwargs):
        import csv
        from django.http import HttpResponse
        from django.template.defaultfilters import slugify

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' \
            % slugify(self.model.__name__)
        fields = list(self.get_csv_fields(request))
        writer = csv.DictWriter(response, fields)

        # Write header row.
        headers = dict((f, label_for_field(f, self.model, self))
                       for f in fields)
        writer.writerow(headers)

        # Get the queryset
        queryset = self.get_queryset(request)
        search_term = request.GET.get(SEARCH_VAR, '')
        queryset, _ = self.get_search_results(request, queryset, search_term)

        # Write records.
        if self.csv_record_limit:
            queryset = queryset[:self.csv_record_limit]
        for r in queryset:
            data = {}
            for name in fields:
                if hasattr(r, name):
                    data[name] = getattr(r, name)
                elif hasattr(self, name):
                    data[name] = getattr(self, name)(r)
                else:
                    raise ValueError('Unknown field: {}'.format(name))

                if callable(data[name]):
                    data[name] = data[name]()
            writer.writerow(data)
        return response

    csv_export.short_description = \
        'Exported selected %(verbose_name_plural)s as CSV'
