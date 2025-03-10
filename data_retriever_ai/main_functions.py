from api_services import api_services
import json
import asyncio
import datetime
import calendar

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
    
def validate_data_type(value, data_type):
    if data_type == "STRING":
        return str(value)
    elif data_type == "NUMBER":
        return float(value)
    elif data_type == "INTEGER":
        return int(value)
    elif data_type == "ARRAY":
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            # if value is not a valid JSON array, wrap it in a list
            return [value]
    elif data_type == "BOOLEAN":
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise ValueError("Invalid boolean value")
    else:
        raise ValueError("Unknown data type")

def get_bookings_count(necessary_parameters, function_declar_json):
    all_parameters = function_declar_json['object']['properties']
    original_params = function_declar_json['original_parameters']
    date_params = function_declar_json['date_parameters']
    
    client_params = [
        "Client Status IDs",
        "Gender"
    ]
    
    necessary_client_params = {}

    bookings_payload = {}
    for parameter in necessary_parameters:
        name = parameter["filter_variable_name"]
        value = parameter["value"]
        if name in original_params:
            value = validate_data_type(value, all_parameters[name]["type"])

            if all_parameters[name]["type"] == "ARRAY":
                for i in range(len(value)):
                    value[i] = validate_data_type(value[i], all_parameters[name]["items"]["type"])

            if name in date_params:
                value = date_to_code(value)

            bookings_payload[name] = value
        elif name in client_params:
            necessary_client_params[name] = value

    print("payload", bookings_payload)
    bookings_dict = api_services.fetch_data(method="POST",endpoint="get_bookings_request", payload=bookings_payload)
    bookings_ids = bookings_dict.get("payload", [])["Booking IDs"]

    final_bookings_count = len(bookings_ids)

    if necessary_client_params:
        clients_detail_payload = {}
        # Check if "Client Status IDs" is in necessary_client_params
        if "Client Status IDs" in necessary_client_params:
            value = validate_data_type(necessary_client_params["Client Status IDs"], all_parameters["Client Status IDs"]["type"])
            if all_parameters["Client Status IDs"]["type"] == "ARRAY":
                for i in range(len(value)):
                    value[i] = validate_data_type(value[i], all_parameters["Client Status IDs"]["items"]["type"])

            clients_detail_payload["Client Status IDs"] = value

        # if "Client Status IDs" is not in necessary_client_params, the payload will go with empty
        clients_detail_dict = api_services.fetch_data(method="POST",endpoint="get_clients_details_request", payload=clients_detail_payload)
        clients = clients_detail_dict.get("payload", [])["Clients"]

        if "Gender" in necessary_client_params:
            value = validate_data_type(necessary_client_params["Gender"], all_parameters["Gender"]["type"])
            if all_parameters["Gender"]["type"] == "ARRAY":
                for i in range(len(value)):
                    value[i] = validate_data_type(value[i], all_parameters["Gender"]["items"]["type"])

            clients = [client for client in clients if client["Gender"] in value]

        client_accounts_dict = api_services.fetch_data(method="POST",endpoint="get_client_accounts_request", payload={"Client IDs": [client["Client ID"] for client in clients]})
        client_accounts = client_accounts_dict.get("payload", [])["Client Accounts"]

        final_bookings_count = len([client_acc for client_acc in client_accounts if client_acc["Booking ID"] in bookings_ids])

    return final_bookings_count