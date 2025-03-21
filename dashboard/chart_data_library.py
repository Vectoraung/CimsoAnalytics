class ChartLibrary:
    def __init__(self):
        self.chart_data = {}

    def add_chart_data(self, chart_name, filter, data):
        if chart_name not in self.chart_data:
            self.chart_data[chart_name] = []

        self.chart_data[chart_name].append({"filter": filter, "value": data})

    def get_chart_data(self, chart_name):
        return self.chart_data.get(chart_name, [])

chart_library = ChartLibrary()