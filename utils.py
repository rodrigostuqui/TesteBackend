import calendar

class DataUtils:
    linechart = {
        "xAxis": {
            "type": "category",
            "data": []
        },
        "yAxis": {
            "type": "value"
        },
        "series": {
            "type": "stacked_line",
            "series": []
        },
        "title": "Headcount por Ano",
        "grid": 6,
        "color": [
            "#D4DDE2",
            "#A3B6C2"
        ]
    }

    categorychart = {
        "xAxis": {
            "type": "value",
            "show": True,
            "max": {}
        },
        "yAxis": {
            "type": "category",
            "data": []
        },
        "series": {
            "type": "horizontal_stacked",
            "series": []
        },
        "title": "Empresa",
        "grid": 6,
        "color": [
            "#2896DC"
        ],
        "is%": False
}

    @classmethod
    def transform_query_in_json_linechart(cls, query):
        months = cls.get_months_in_period(query)
        count_months = [0]*len(months)
        year = query[0]['year']
        series = list()
        for x in query:
            if x['year'] == year:
                count_months[months.index(calendar.month_abbr[x['month']])] = x['count']
            else:
                series.append({"name" : year, "type" : "line", "data" : count_months})
                year = x['year']
                count_months = [0]*len(months)
        series.append({"name" : year, "type" : "line", "data" : count_months})
        cls.linechart['xAxis']['data'] = months
        cls.linechart['series']['series'] = series
        
        return cls.linechart

    @classmethod
    def transform_query_in_json_categorychart(cls, query):
        cls.categorychart['yAxis']['data'] = [x['ds_category_4'] for x in query]
        cls.categorychart['series']['series'] = [{"name": "Colaboradores", 
                                               "data": [x['count'] for x in query], 
                                               "type" : "bar"}]
        return cls.categorychart

    def get_months_in_period(query):
        abbr_months = calendar.month_abbr
        months_list = [x['month'] for x in query]
        months_list.sort()

        return [abbr_months[x] for x in set(months_list)]