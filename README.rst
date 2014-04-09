==================
 django-admin-csv 
==================

Adds a "download csv" option to your ModelAdmin. Simply add "admin_csv" to your
INSTALLED_APPS, and have your ModelAdmin extend CSVMixin like so:

.. code:: python

    from admin_csv import CSVMixin

    class MyModelAdmin(CSVMixin, admin.ModelAdmin):
        list_display = ['foo', 'bar', 'baz']
        csv_fields = list_display + ['qux']
