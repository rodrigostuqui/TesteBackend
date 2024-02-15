from django.shortcuts import render
from datetime import datetime
from .models import Turnover
from django.http import JsonResponse
from utils import DataUtils

def turnover_linechart(request):
    if request.method == 'GET':
        # Get the initial and end dates from the GET parameters
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        if init_date is None or end_date is None:
            return JsonResponse({"error": { "message": "Missing parameters", "details": {
                                "required_parameters": ["init_date", "end_date"]
                                }}})
        # Convert the date strings to datetime objects
        try:
            init_date = datetime.strptime(init_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, safe=False)
        # Query the database for turnover data within the specified period
        employee_dimissal = Turnover.get_turnover_linechart(init_date, end_date)
        # Transform the query result into JSON format suitable for a line chart
        data = DataUtils.transform_query_in_json_linechart(employee_dimissal)
        return JsonResponse(data, safe=False)

def turnover_categorychart(request):
    if request.method == 'GET':
        # Get the initial date, end date, and category from the GET parameters
        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')
        category = request.GET.get('category')
        if init_date is None or end_date is None or category is None:
            return JsonResponse({"error": { "message": "Missing parameters", "details": {
                                "required_parameters": ["init_date", "end_date", "category"]
                                }}}, safe=False)
        # Convert the date strings to datetime objects
        try:
            init_date = datetime.strptime(init_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, safe=False)
        # Query the database for turnover data within the specified period and category
        employee_dimissal = Turnover.get_turnover_categorychart(init_date, end_date, category)
        # Transform the query result into JSON format suitable for a category chart
        data = DataUtils.transform_query_in_json_categorychart(employee_dimissal)
        return JsonResponse(data, safe=False)
