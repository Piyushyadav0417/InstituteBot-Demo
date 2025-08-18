# InstituteBot-Demo
AI-powered Institute Chatbot Demo — answers student queries about courses, trainers, and institute info using Django ORM, LangChain, and GPT-4.


## InstituteBot Demo 🎓

This is a demo of an **AI-powered assistant for educational institutes**.  
The bot integrates **OpenAI GPT-4** with **Django models** (`Course`, `Trainer`, `About`) using **LangChain agents**.  
It allows students to ask natural language questions like:  

- "Who teaches the Python course?"  
- "What is the duration of the Data Science course?"  
- "Show me all beginner-level courses."  
- "Give me Ravi Kumar’s LinkedIn profile."  

Behind the scenes, the agent safely generates **Django ORM queries** and executes them, returning precise answers.  

Key Features:
- ✅ Safe execution of ORM queries (no raw SQL or unsafe eval)  
- ✅ Conversational memory to handle multi-turn Q&A  
- ✅ GPT-4 powered natural language understanding  
- ✅ Built with LangChain’s Conversational React Agent  
- ✅ Extendable for any institute/edtech platform  
