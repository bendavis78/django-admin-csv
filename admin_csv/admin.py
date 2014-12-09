from functools import update_wrapper

from django.contrib.admin.utils import label_for_field
from django.utils.six import text_type


class CSVMixin(object):
    """
    Adds a CSV export action to an admin view.
    """

    change_list_template = "admin/change_list_csv.html"

    # This is the maximum number of records that will be written.
    # Exporting massive numbers of records should be done asynchronously.
    csv_record_limit = None
    csv_fields = []
    csv_headers = {}

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

    def get_csv_filename(self, request):
        return text_type(self.model._meta.verbose_name_plural)

    def changelist_view(self, request, extra_context=None):
        context = {
            'querystring': request.GET.urlencode()
        }
        context.update(extra_context or {})
        return super(CSVMixin, self).changelist_view(request, context)

    def csv_header_for_field(self, field_name):
        if self.csv_headers.get(field_name):
            return self.csv_headers[field_name]
        return label_for_field(field_name, self.model, self)

    def csv_export(self, request, *args, **kwargs):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={0}.csv'.format(
                self.get_csv_filename(request)))
        fields = list(self.get_csv_fields(request))
        writer = csv.DictWriter(response, fields)

        # Write header row.
        headers = dict((f, self.csv_header_for_field(f)) for f in fields)
        writer.writerow(headers)

        # Get the queryset using the changelist
        cl_response = self.changelist_view(request)
        cl = cl_response.context_data.get('cl')
        queryset = cl.get_queryset(request)

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
