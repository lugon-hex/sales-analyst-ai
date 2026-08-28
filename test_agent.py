from dotenv import load_dotenv

load_dotenv()

from app.agent.agent import ask_agent


question = "Qual produto teve o maior faturamento?"

answer = ask_agent(question)

print()
print("================================")
print("AGENT RESPONSE")
print("================================")
print(answer)

