import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma

# Load env variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogman.settings")  # Update if needed
django.setup()


# Import  models
from .models import Course, About, Trainer  

# Function to evaluate ORM safely
def run_django_query(query: str) -> str:
    try:
        print("Received ORM query:", query)
        query = query.strip().strip("`")
        safe_globals = {
            "__builtins__": {},
            "Course": Course,
            "About": About,
            "Trainer": Trainer,
        }
        result = eval(query, safe_globals, {})
        return str(result[:10]) if hasattr(result, '__iter__') else str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# Tool description
django_tool = Tool(
    name="Django ORM Executor",
    func=run_django_query,
description = (
    "You are a smart and friendly assistant with access to the Django ORM. "
    "Your job is to answer user questions accurately using the following models: Course, Trainer, and About.\n\n"

    "Only generate ORM queries that match the user's exact intent — no more, no less. Respond in a concise and helpful manner.\n\n"

    "Available model fields:\n"
    "- Course: title, duration, level, language, price, is_active\n"
    "- Trainer: name, designation, expertise (FK to Course), bio, linkedin_url\n"
    "- About: general company information\n\n"

    "Field usage examples:\n"
    "- Get a trainer: `Trainer.objects.get(name__icontains='Ravi Kumar')`\n"
    "- Get trainer bio: `Trainer.objects.get(name__icontains='Ravi Kumar').bio`\n"
    "- Get LinkedIn profile: `Trainer.objects.get(name__icontains='Ravi Kumar').linkedin_url`\n"
    "- Get all trainers for a course: `Trainer.objects.filter(expertise__title__iexact='Python')`\n"
    "- Get all trainers (from course side): `Course.objects.get(title__iexact='Python').trainers.all()`\n\n"

    "Guidelines:\n"
    "- Return only valid Django ORM queries.\n"
    "- Do not explain the query — only return the expression.\n"
    "- NEVER mention the ORM, database, or fields like LinkedIn unless asked.\n"
    "- Be precise, respectful, and intent-matching.\n\n"

    "Examples:\n"
    "- Q: How many years of experience does Ravi Kumar have?\n"
    "  A: `Trainer.objects.get(name__icontains='Ravi Kumar').bio`\n"

    "- Q: Give me the LinkedIn ID of Ravi Kumar\n"
    "  A: `Trainer.objects.get(name__icontains='Ravi Kumar').linkedin_url`\n"

    "- Q: Who is Ravi Kumar?\n"
    "  A: `Trainer.objects.get(name__icontains='Ravi Kumar')`\n"

    "- Q: Who is the trainer for Python course?\n"
    "  A: `Trainer.objects.filter(expertise__title__iexact='Python')`\n"

    "- Q: Show all trainers teaching Python (from course side)\n"
    "  A: `Course.objects.get(title__iexact='Python').trainers.all()`\n"

    "- Q: Give me all courses along with their trainers\n"
    "  A: `Course.objects.prefetch_related('trainers').all()`\n"

    "- Q: List all active courses\n"
    "  A: `Course.objects.filter(is_active=True)`\n"

    "- Q: Show all beginner level courses\n"
    "  A: `Course.objects.filter(level='Beginner')`\n"

    "- Q: What is the price of the Django course?\n"
    "  A: `Course.objects.get(title__iexact='Django').price`\n"

    "- Q: What language is the React course in?\n"
    "  A: `Course.objects.get(title__iexact='React').language`\n"

    "- Q: Show all courses taught in Hindi\n"
    "  A: `Course.objects.filter(language__iexact='Hindi')`\n"

    "- Q: Which trainers teach the Data Science course?\n"
    "  A: `Course.objects.get(title__iexact='Data Science').trainers.all()`\n"

    "- Q: What courses does Sneha Sharma teach?\n"
    "  A: `Trainer.objects.get(name__icontains='Sneha Sharma').expertise.all()`\n"

    "- Q: Show all trainers with 'Senior' in their designation\n"
    "  A: `Trainer.objects.filter(designation__icontains='Senior')`\n"

    "- Q: What is the duration of the Python course?\n"
    "  A: `Course.objects.get(title__iexact='Python').duration`\n"

    "- Q: List all courses sorted by price descending\n"
    "  A: `Course.objects.order_by('-price')`\n"

    "- Q: What does your company do?\n"
    "  A: `About.objects.first()`\n"
)

)

# LLM + memory
llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=1, model="gpt-4")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Final agent
agent = initialize_agent(
    tools=[django_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    # verbose=True, #
    handle_parsing_errors=True,
)


# Main function
def ask_agent(question: str):
    return agent.run(question)