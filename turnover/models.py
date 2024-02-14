from django.db import models
from django.db.models import Count, FloatField, Func
from django.db.models.functions import ExtractMonth, ExtractYear

class Turnover(models.Model):
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
    def get_mean_active_employees_on_period(cls, init_date, end_date):
        month_diference = end_date - init_date
        month_diference = month_diference.days/30
        employee_count = cls.objects.filter(dt_reference_month__range=[init_date, end_date], fg_status=True).count()
        return employee_count/month_diference
    
    @classmethod
    def get_turnover_linechart(cls, init_date, end_date):
        employee_dismissal = cls.objects.filter(dt_reference_month__range=[init_date, end_date], fg_dismissal_on_month=True)
        employee_dismissal = employee_dismissal.values(year=ExtractYear('dt_reference_month'), month=ExtractMonth('dt_reference_month'))
        mean_active_employees = cls.get_mean_active_employees_on_period(init_date, end_date)
        return employee_dismissal.annotate(count=Func(
        Count('id') / float(mean_active_employees) * 100,
        function='ROUND',
        template='%(function)s(%(expressions)s, 2)',
        output_field=FloatField(),))
    
    @classmethod
    def get_turnover_categorychart(cls, init_date, end_date, category):
        active_employees = cls.objects.filter(dt_reference_month__month=end_date.month, dt_reference_month__year=end_date.year, fg_status=True, ds_category_5=category).count()
        employees_dismissal = cls.objects.filter(dt_reference_month__month=end_date.month, dt_reference_month__year=end_date.year, fg_dismissal_on_month=True, ds_category_5=category)
        return employees_dismissal.values('ds_category_4').annotate(count=Func(
        Count('id') / float(active_employees) * 100,
        function='ROUND',
        template='%(function)s(%(expressions)s, 2)',
        output_field=FloatField(),))