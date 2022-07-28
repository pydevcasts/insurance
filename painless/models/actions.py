from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
import csv

# Register your actions here.

class ExportMixin:
    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type = "application/json")
        serializers.serialize("json", queryset, stream=response)
        return response
    
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_pdf(self, request, queryset):
        pass

    export_as_json.short_description = "Export selected posts as JSON"
    export_as_csv.short_description = "Export selected posts as CSV"


class PostableMixin:
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status = 1)

        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = "{} posts were".format(rows_updated)
        
        self.message_user(request, "{} successfuly marked as published.".format(message_bit))



    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status = 0)

        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = "{} stories were".format(rows_updated)
        
        self.message_user(request, "{} successfuly marked as draft.".format(message_bit))

    make_published.short_description = "Update selected posts as published"
    make_draft.short_description = "Update selected posts as draft"