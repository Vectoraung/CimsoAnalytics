from datetime import datetime
import google.generativeai as ggenai
from pprint import pprint
from google.ai.generativelanguage_v1beta.types import content
import asyncio
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

import json
import os
from django.conf import settings

from . import chart_data_library

class ReportGenerator:
    def __init__(self):
        self.saved_reports = {}
        ggenai.configure(api_key=settings.GOOGLE_API_KEY)

    def get_chart_data(self, chart_title):
        return self.saved_reports.get(chart_title)

    def generate_report(self, data):
        system_instruction="""You are an AI report creator for hotel bookings analytics. Your role is to generate insightful and concise reports based on chart data provided.

Report Guidelines:
Context & Summary:

Clearly state what the data represents (e.g., total bookings, cancellations, revenue, occupancy rates).
If the chart has only a single value (e.g., "Bookings Arrivals Today: 28"), provide relevant context without unnecessary filler.
Trend Analysis (If Applicable):

Compare with previous data if available (e.g., “This is a 15% increase from yesterday”).
Identify significant patterns, seasonal trends, or anomalies.
Business Insights:

Explain what the data implies for operations, revenue, or customer behavior.
Provide actionable insights where relevant (e.g., "High check-ins today may require additional staff at reception").
Brevity & Clarity:

Keep reports easy to read, avoiding unnecessary complexity.
For single-value data, include only what is meaningful. Avoid forced interpretations.
Example Reports:

For Detailed Data:
“The hotel received 150 new bookings this week, a 10% increase from last week. This upward trend suggests growing demand, potentially due to the upcoming holiday season. Consider adjusting room rates accordingly.”

For a Single Value:
“28 bookings are arriving today. Ensure front desk readiness during peak check-in hours.”

Generate reports effectively based on these principles."""

        # Create the model
        generation_config = {
        "temperature": 2,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            required = ["report"],
            properties = {
                "report": content.Schema(
                    type = content.Type.ARRAY,
                    items = content.Schema(
                        type = content.Type.OBJECT,
                        required = ["paragraph_title", "context"],
                        properties = {
                            "paragraph_title": content.Schema(
                                type = content.Type.STRING,
                            ),
                            "context": content.Schema(
                                type = content.Type.STRING,
                            ),
                        },
                    ),
                ),
            },
        ),
        "response_mime_type": "application/json",
        }

        model = ggenai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=system_instruction
            )
        
        chat_session = model.start_chat(history=[])

        prompt = str(data)
        if self.saved_reports.get(data.get('Chart title')):
            prompt = f"{prompt}\nThis was your last response:\n{self.saved_reports[data.get('Chart title')][-1]}\nTry not to repeat the last response if possible.\nIf the current data is different, try to compare it with the last response."

        print("prompt",prompt)
        response = chat_session.send_message(prompt)

        response_json = json.loads(response.text)

        print(data)

        if not self.saved_reports.get(data.get('Chart title')):
            self.saved_reports[data.get('Chart title')] = []

        self.saved_reports[data.get('Chart title')].append(response_json)

        return response_json
    
report_generator = ReportGenerator()
    
@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def generate_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            request_context = {
                "Chart title": data["title"],
                "data": chart_data_library.chart_library.get_chart_data(data["title"])
            }

            report = report_generator.generate_report(request_context)

            print(report)
            return JsonResponse({"report": report})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)