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
        # Calculate the difference in months between the initial and end dates
        month_difference = (end_date - init_date).days / 30
        # Count the number of active employees within the specified period
        employee_count = cls.objects.filter(dt_reference_month__range=[init_date, end_date], fg_status=True).count()
        # Calculate the mean active employees
        return employee_count / month_difference
    
    @classmethod
    def get_turnover_linechart(cls, init_date, end_date):
        # Filter employees dismissed within the specified period
        employee_dismissal = cls.objects.filter(dt_reference_month__range=[init_date, end_date], fg_dismissal_on_month=True)
        # Aggregate counts by year and month
        employee_dismissal = employee_dismissal.values(year=ExtractYear('dt_reference_month'), month=ExtractMonth('dt_reference_month'))
        mean_active_employees = cls.get_mean_active_employees_on_period(init_date, end_date)
        # Calculate turnover rate and round to two decimal places
        return employee_dismissal.annotate(count=Func(
            Count('id') / float(mean_active_employees) * 100,
            function='ROUND',
            template='%(function)s(%(expressions)s, 2)',
            output_field=FloatField(),
        ))
    
    @classmethod
    def get_turnover_categorychart(cls, init_date, end_date, category):
        # Count active employees within the specified month and category
        active_employees = cls.objects.filter(dt_reference_month__month=end_date.month, dt_reference_month__year=end_date.year, fg_status=True, ds_category_5=category).count()
        # Filter employees dismissed within the specified month and category
        employees_dismissal = cls.objects.filter(dt_reference_month__month=end_date.month, dt_reference_month__year=end_date.year, fg_dismissal_on_month=True, ds_category_5=category)
        # Calculate turnover rate for each category 4 and round to two decimal places
        return employees_dismissal.values('ds_category_4').annotate(count=Func(
            Count('id') / float(active_employees) * 100,
            function='ROUND',
            template='%(function)s(%(expressions)s, 2)',
            output_field=FloatField(),
        ))