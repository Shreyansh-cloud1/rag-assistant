from app.llm import generate_answer

context = """
Oracle RMAN is Oracle's Recovery Manager used for backup and recovery.
"""

question = "What is RMAN used for?"

answer = generate_answer(context, question)

print("Response from Gemini:")
print(answer)