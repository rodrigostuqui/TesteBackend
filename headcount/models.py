from django.db import models
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear

class Headcount(models.Model):
    id_employee = models.CharField(max_length=300, null=False)
    ds_category_1 = models.CharField(max_length=300, null=False)
    ds_category_2 = models.CharField(max_length=300, null=False)
    ds_category_3 = models.CharField(max_length=300, null=False)
    ds_category_4 = models.CharField(max_length=300, null=False)
    ds_category_5 = models.CharField(max_length=300, null=False)
    fg_status = models.IntegerField()
    fg_dismissal_on_month = models.IntegerField()
    dt_reference_month = models.DateField()

    @classmethod
    def count_employees_by_period(cls, init_date : datetime, end_date : datetime):
        employee_counts = cls.objects.filter(dt_reference_month__range=[init_date, end_date], fg_status=True)
        employee_counts = employee_counts.values(year=ExtractYear('dt_reference_month'), month=ExtractMonth('dt_reference_month'))
        return employee_counts.annotate(count = Count('id'))
    
    @classmethod
    def count_employees_by_category(cls, init_date : datetime, end_date : datetime, category : str):
        employee_counts = cls.objects.filter(dt_reference_month__month=end_date.month, dt_reference_month__year=end_date.year, fg_status=True, ds_category_5=category)
        return employee_counts.values('ds_category_4').annotate(count = Count('id'))
        