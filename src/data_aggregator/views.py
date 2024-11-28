import datetime

import pandas as pd
from django.shortcuts import render
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from data_aggregator.models import File, DataRow
from data_aggregator.forms import UploadFileForm
import warnings


@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            uploaded_file = File.objects.create(
                upload_by=request.user, file_name=file.name, status=True
            )
            warnings.simplefilter(action="ignore", category=UserWarning)
            try:
                df = (
                    pd.read_csv(file, parse_dates=["Start", "End"])
                    if file.name.endswith(".csv")
                    else pd.read_excel(file, parse_dates=["Start", "End"])
                )

                required_columns = {
                    "Advertiser",
                    "Brand",
                    "Start",
                    "End",
                    "Format",
                    "Platform",
                    "Impr",
                }
                if not required_columns.issubset(df.columns):
                    uploaded_file.status = False
                    uploaded_file.error = (
                        "Invalid file format, some column does not exist"
                    )
                    uploaded_file.save()
                    return render(
                        request,
                        "data_aggregator/upload.html",
                        {"form": form, "message": uploaded_file.error},
                    )

                num_rows = df.shape[0]

                df["Start"] = pd.to_datetime(df["Start"], format=None, errors="coerce")
                df["End"] = pd.to_datetime(df["End"], format=None, errors="coerce")
                df = df.dropna(subset=["Start", "End"])

                objects = []
                for _, row in df.iterrows():
                    objects.append(
                        DataRow(
                            file=uploaded_file,
                            advertiser=row["Advertiser"],
                            brand=row["Brand"],
                            start_date=(
                                row["Start"]
                                if row["Start"] is datetime.date in row
                                else row["Start"].date()
                            ),
                            end_date=(
                                row["End"]
                                if row["End"] is datetime.date in row
                                else row["End"].date()
                            ),
                            format=row["Format"],
                            platform=row["Platform"],
                            impr=row["Impr"],
                        )
                    )
                difference = num_rows - len(objects)
                if len(objects) < num_rows:
                    if difference == num_rows:
                        uploaded_file.status = False
                        uploaded_file.error = "No valid data"
                        uploaded_file.save()
                        return render(
                            request,
                            "data_aggregator/upload.html",
                            {
                                "form": form,
                                "error_message": "Error processing file",
                                "error_message_details": "No valid data",
                            },
                        )
                    else:
                        DataRow.objects.bulk_create(objects)
                        uploaded_file.status = True
                        uploaded_file.save()
                        message_details = f"{num_rows - len(objects)} rows from {num_rows} rows were omitted due to incorrect data"
                        return render(
                            request,
                            "data_aggregator/upload.html",
                            {
                                "form": form,
                                "message": "File uploaded successfully",
                                "message_details": message_details,
                            },
                        )
                else:
                    DataRow.objects.bulk_create(objects)
                    uploaded_file.status = True
                    uploaded_file.save()
                    return render(
                        request,
                        "data_aggregator/upload.html",
                        {
                            "form": form,
                            "message": "File uploaded successfully",
                        },
                    )

            except Exception as e:
                uploaded_file.status = False
                uploaded_file.error = str(e)
                uploaded_file.save()
                return render(
                    request,
                    "data_aggregator/upload.html",
                    {
                        "form": form,
                        "error_message": "Error processing file",
                        "error_message_details": str(e),
                    },
                )
    else:
        form = UploadFileForm()
    return render(request, "data_aggregator/upload.html", {"form": form})


@login_required
def summary(request):
    is_admin = request.user.is_admin

    period = request.GET.get("period", "year")

    if period == "month":
        if is_admin:
            summary_data = (
                DataRow.objects.annotate(
                    year=F("start_date__year"), month=F("start_date__month")
                )
                .values("year", "month")
                .annotate(total_impr=Sum("impr"))
                .order_by("year", "month")
            )
        else:
            summary_data = (
                DataRow.objects.filter(file__upload_by=request.user)
                .annotate(year=F("start_date__year"), month=F("start_date__month"))
                .values("year", "month")
                .annotate(total_impr=Sum("impr"))
                .order_by("year", "month")
            )
    else:
        if is_admin:
            summary_data = (
                DataRow.objects.annotate(year=F("start_date__year"))
                .values("year")
                .annotate(total_impr=Sum("impr"))
                .order_by("year")
            )
        else:
            summary_data = (
                DataRow.objects.filter(file__upload_by=request.user)
                .annotate(year=F("start_date__year"))
                .values("year")
                .annotate(total_impr=Sum("impr"))
                .order_by("year")
            )

    return render(
        request,
        "data_aggregator/summary.html",
        {"summary_data": summary_data, "period": period},
    )
