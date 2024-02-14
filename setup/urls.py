"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from headcount.views import headcount_linechart, headcount_categorychart
from turnover.views import turnover_categorychart, turnover_linechart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('headcount/line_chart/', headcount_linechart, name='headcount_linechart'),
    path('headcount/category_chart/', headcount_categorychart, name='headcount_categorychart'),
    path('turnover/line_chart/', turnover_linechart, name='turnover_categorychart'),
    path('turnover/category_chart/', turnover_categorychart, name='turnover_categorychart'),
]
