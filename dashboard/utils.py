import datetime
import calendar

class Utils():
    def __init__(self):
        pass

    @staticmethod
    def change_date_format(date_str):
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    
    @staticmethod
    def date_to_month_code(date_str):
        day, month, _ = date_str.split('-')
        return f"{month}{day.zfill(2)}"

    @staticmethod
    def date_to_code(date_str):
        date_format = "%d-%m-%Y"
        try:
            day, month, year = map(int, date_str.split('-'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1 <= year <= 9999):
                return "Error: Invalid date components."
            if day > calendar.monthrange(year, month)[1]:
                return "Error: Day is out of range for the given month."
            date_obj = datetime.datetime(year, month, day)
            ref_date = datetime.datetime(1899, 12, 30)
            delta = date_obj - ref_date
            return delta.days
        except ValueError:
            return "Error: Invalid date string. Please use the format dd-mm-yyyy."
        
    @staticmethod
    def code_to_date(date_code):
        ref_date = datetime.datetime(1899, 12, 30)
        date_obj = ref_date + datetime.timedelta(days=date_code)
        return date_obj.strftime('%d-%m-%Y')
    
    @staticmethod
    def convert_date_to_minutes(date_str):
        # Parse the date string into a datetime object
        date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y, %H:%M')

        # Define the base date (30 December 1899, at 00:00)
        base_date = datetime.datetime(1899, 12, 30)

        # Calculate the difference between the date and the base date
        delta = date_obj - base_date

        # Convert the difference to minutes
        minutes = delta.days * 24 * 60 + delta.seconds // 60

        return minutes