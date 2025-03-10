import requests
from requests.exceptions import RequestException

class ApiService:
    BASE_URL = 'https://ixschool.cimso.xyz/'  # Base URL for the API

    @staticmethod
    def call_api(endpoint, method="GET", headers=None, payload=None):
        url = f"{ApiService.BASE_URL}{endpoint}"
        headers = headers or {
            'Authorization': '{"Client Login ID":"CiMSO.dev","Client Password":"CiMSO.dev","hg_pass":"nGXUF1i^57I^ao^o"}',
            'Content-Type': 'application/json'
        }
        payload = payload or {}
        body = {"hg_code":"ixschool","payload":payload}

        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=headers, json=body)
            elif method.upper() == "GET":
                response = requests.get(url, headers=headers, params=body)
            else:
                raise ValueError("Unsupported HTTP method")
            
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            return response.json()
        except RequestException as e:
            return {"error": str(e)}
        
def fetch_data(endpoint, method="GET", payload=None):
    """
    Fetch data from the API using the ApiService class.
    
    :param endpoint: The API endpoint to call.
    :param method: HTTP method to use ('GET', 'POST', etc.).
    :param payload: Data to send to the API.
    :return: Response from the API.
    """
    return ApiService.call_api(endpoint, method=method, payload=payload)

# Example usage
'''payload = {"Client ID": -1438289273}
bookings_dict = fetch_data(method="POST",endpoint="get_bookings_request", payload=payload)'''