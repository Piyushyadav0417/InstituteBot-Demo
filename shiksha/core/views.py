from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    return render(request, 'core/home.html')
    return HttpResponse("Hello! This is the home page.")

def about(request):
    return HttpResponse("This is the about page.")

# chatboat/views.py
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .agent import ask_agent  # assuming your agent code is in chatboat/agent.py

# @csrf_exempt
# def chatboat_view(request):
#     user_input = None
#     bot_response = None

#     if request.method == "POST":
#         user_input = request.POST.get("message")
#         if user_input:
#             bot_response = ask_agent(user_input)

#     return render(request, "core/chat.html", {
#         "user_input": user_input,
#         "bot_response": bot_response,
#     })


from django.views.decorators.csrf import csrf_exempt
from langchain.schema import messages_from_dict, messages_to_dict
from .agent import ask_agent, memory  # agent has a global memory object

# @csrf_exempt
# def chatboat_view(request):
#     user_input = None
#     bot_response = None
#     if "chat_history" not in request.session:
#         request.session["chat_history"] = []

#     chat_history = request.session["chat_history"]
#     if request.method == "POST":
#         user_input = request.POST.get("message")

#         if user_input:
#             bot_response = ask_agent(user_input)
#             chat_history.append({
#                 "question": user_input,
#                 "answer": bot_response
#             })
#             request.session["chat_history"] = chat_history  

#     return render(request, "core/chat.html", {
#         "user_input": user_input,
#         "bot_response": bot_response,
#     })

@csrf_exempt
def chatboat_view(request):
    # Initialize chat history if missing
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    chat_history = request.session["chat_history"]

    if request.method == "POST":
        user_input = request.POST.get("message")
        if user_input:
            bot_response = ask_agent(user_input)
            chat_history.append({
                "question": user_input,
                "answer": bot_response
            })
            request.session["chat_history"] = chat_history
            request.session.modified = True  # Ensure session is updated

            return redirect("chat_page")  # 👈 Fix: prevent duplicate resubmission

    return render(request, "core/chat.html", {
        "chat_history": chat_history
    })


def testin(request):
    
    print('--------------------', )
    pass