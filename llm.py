import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()


class GeminiLLM:
    """
    Wrapper para a Gemini API.

    Tenta o modelo configurado no .env e, caso o servidor
    esteja temporariamente indisponível, tenta modelos
    alternativos.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY não encontrada no ambiente."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

        self.fallback_models = [
            self.model,
            "gemini-3.5-flash-lite",
        ]

        # Remove duplicados mantendo a ordem
        self.fallback_models = list(
            dict.fromkeys(self.fallback_models)
        )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate(self, prompt: str) -> str:
        """
        Gera uma resposta usando Gemini.

        Se um modelo retornar 503, tenta o próximo modelo.
        """

        if not prompt.strip():
            raise ValueError(
                "Prompt não pode estar vazio."
            )

        last_error = None

        for model in self.fallback_models:

            for attempt in range(2):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt,
                        )
                    )

                    if not response.text:
                        raise RuntimeError(
                            "Gemini retornou uma resposta vazia."
                        )

                    return response.text

                except errors.ServerError as error:

                    last_error = error

                    print(
                        f"[Gemini] Modelo {model} "
                        f"indisponível "
                        f"(tentativa {attempt + 1}/2)."
                    )

                    if attempt == 0:
                        time.sleep(2)

        raise RuntimeError(
            "Nenhum modelo Gemini está disponível no momento."
        ) from last_error
