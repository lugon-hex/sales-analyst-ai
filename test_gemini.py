from app.agent.llm import GeminiLLM


llm = GeminiLLM()

response = llm.generate(
    "Responda apenas: Gemini funcionando!"
)

print(response)