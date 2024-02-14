from django.shortcuts import render
from .models import Headcount
from datetime import datetime
from django.http import JsonResponse
from utils import DataUtils
def headcount_linechart(request):
    if request.method == 'GET':
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        init_date = datetime.strptime(init_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        employee_counts = Headcount.count_employees_by_period(init_date=init_date, end_date=end_date)
        data = DataUtils.transform_query_in_json_linechart(employee_counts)
        return JsonResponse(data, safe=False)


def headcount_categorychart(request):
    if request.method == 'GET':
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        category = request.GET.get('category')
        init_date = datetime.strptime(init_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        employee_counts = Headcount.count_employees_by_category(init_date, end_date, category)
        data = DataUtils.transform_query_in_json_categorychart(employee_counts)
        return JsonResponse(data, safe=False)


