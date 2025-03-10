from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from . import data_retriever_ai

ai_assistant = data_retriever_ai.DRAssistantAI()

def ai_chat_page_view(request):
    context = {'history_messages': []}

    for history in ai_assistant.chat_session.history:
        context['history_messages'].append({"role": history.role, "content": history.parts[0].text})

    print(context)

    return render(request, 'data_retriever_ai/ai_chat_page.html', context)

@csrf_exempt  # Use only in development; use CSRF token in production
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        bot_response = ai_assistant.send_message(question=user_message)

        # Here, you can process the message, send it to an AI model, or perform any logic
        #bot_response = f"I received: {user_message}"  # Placeholder response

        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)