from django.contrib import admin

from data_aggregator.models import File, DataRow


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("id",)


@admin.register(DataRow)
class DataRowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "advertiser",
        "brand",
        "start_date",
        "end_date",
        "platform",
        "impr",
    )
    search_fields = ("advertiser", "brand", "platform")
    list_filter = ("start_date", "end_date", "platform")
    date_hierarchy = "start_date"
