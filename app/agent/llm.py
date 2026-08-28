import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiLLM:
    """
    Small wrapper around the Gemini API.

    The rest of the application does not need
    to know how Gemini is called.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.7-flash",
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found in the environment."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate(self, prompt: str) -> str:
        """
        Generate a text response from Gemini.
        """

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text
