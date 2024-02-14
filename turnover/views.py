from django.shortcuts import render
from datetime import datetime
from .models import Turnover
from django.http import JsonResponse
from utils import DataUtils
# Create your views here.
def turnover_linechart(request):
    if request.method == 'GET':
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        init_date = datetime.strptime(init_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        employee_dimissal = Turnover.get_turnover_linechart(init_date, end_date)
        data = DataUtils.transform_query_in_json_linechart(employee_dimissal)
        return JsonResponse(data, safe=False)

def turnover_categorychart(request):
    if request.method == 'GET':
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        category = request.GET.get('category')
        init_date = datetime.strptime(init_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        employee_dimissal = Turnover.get_turnover_categorychart(init_date, end_date, category)
        data = DataUtils.transform_query_in_json_categorychart(employee_dimissal)
        return JsonResponse(data, safe=False)
