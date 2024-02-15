import calendar

class DataUtils:
    # JSON template for a line chart
    linechart = {
        "xAxis": {
            "type": "category",
            "data": []  # Placeholder for X-axis data (e.g., months)
        },
        "yAxis": {
            "type": "value" 
        },
        "series": {
            "type": "stacked_line", 
            "series": []  # Placeholder for series data
        },
        "title": "Headcount por Ano",
        "grid": 6,
        "color": [
            "#D4DDE2",
            "#A3B6C2"
        ]
    }

    # JSON template for a category chart
    categorychart = {
        "xAxis": {
            "type": "value",
            "show": True,
            "max": {}
        },
        "yAxis": {
            "type": "category",
            "data": []  # Placeholder for Y-axis data
        },
        "series": {
            "type": "horizontal_stacked", 
            "series": []  # Placeholder for series data
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
        # Return the line chart template if query is empty
        if len(query) == 0:
            return cls.linechart
        year = query[0]['year'] 
        series = list()
        for x in query:
            if x['year'] == year:
                # add the count from query in the respective month
                count_months[months.index(calendar.month_abbr[x['month']])] = x['count']
            else:
                # Append series data for the previous year
                series.append({"name": year, "type": "line", "data": count_months})
                year = x['year']
                count_months = [0]*len(months)
        # Append series data for the last year
        series.append({"name": year, "type": "line", "data": count_months})
        cls.linechart['xAxis']['data'] = months
        cls.linechart['series']['series'] = series
        return cls.linechart

    @classmethod
    def transform_query_in_json_categorychart(cls, query):
        cls.categorychart['yAxis']['data'] = [x['ds_category_4'] for x in query]  # Update Y-axis data with categories
        cls.categorychart['series']['series'] = [{"name": "Colaboradores", 
                                                   "data": [x['count'] for x in query], 
                                                   "type": "bar"}]  # Update series data with counts
        return cls.categorychart

    @staticmethod
    def get_months_in_period(query):
        abbr_months = calendar.month_abbr  # Get the abbreviation for each month
        months_list = [x['month'] for x in query]  # Extract months from the query result
        months_list.sort() 
        # Return the list of unique month abbreviations
        return [abbr_months[x] for x in set(months_list)]