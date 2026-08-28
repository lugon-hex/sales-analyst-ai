from app.agent.llm import GeminiLLM
from app.agent.prompts import (
    build_sql_prompt,
    build_analysis_prompt,
)
from app.agent.tools import get_database_schema
from app.database.queries import execute_read_only_query


class SalesAgent:
    """
    Agente responsável por transformar perguntas
    em consultas SQL e interpretar os resultados.
    """

    def __init__(self):
        self.llm = GeminiLLM()

    def generate_sql(self, question: str) -> str:
        """
        Gera uma consulta SQL baseada na pergunta do usuário.
        """

        schema = get_database_schema()

        prompt = build_sql_prompt(
            question=question,
            schema=schema,
        )

        response = self.llm.generate(prompt)

        sql = response.strip()

        # Remove possíveis blocos Markdown:
        #
        # ```sql
        # SELECT ...
        # ```
        #

        if sql.startswith("```sql"):
            sql = sql[len("```sql"):]

        elif sql.startswith("```"):
            sql = sql[len("```"):]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()

    def analyze(self, question: str) -> dict:
        """
        Executa o fluxo completo:

        pergunta
            ↓
        Gemini
            ↓
        SQL
            ↓
        SQLite
            ↓
        Gemini
            ↓
        resposta
        """

        sql = self.generate_sql(question)

        results = execute_read_only_query(sql)

        prompt = build_analysis_prompt(
            question=question,
            sql=sql,
            results=results,
        )

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "sql": sql,
            "results": results,
            "answer": answer,
        }


def ask_agent(question: str) -> str:
    """
    Função pública utilizada pela aplicação.
    """

    if not question.strip():
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    agent = SalesAgent()

    result = agent.analyze(question)

    return result["answer"]