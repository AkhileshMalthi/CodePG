import os
import re
from pathlib import Path

import yaml
from groq import Groq

from codepg.ai import AI


class GroqAI(AI):
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        self.client = Groq(api_key=api_key)
        self.model_name = "mixtral-8x7b-32768"  # Using Mixtral model

        # Load prompt template
        prompt_path = Path(__file__).parent.parent / "prompts" / "code_generation.yaml"
        with open(prompt_path) as f:
            self.prompt_template = yaml.safe_load(f)["template"]

    def generate(self, programming_language: str, prompt: str) -> str:
        """Generates code in specified language based on the prompt"""
        formatted_prompt = self.prompt_template.format(language=programming_language, prompt=prompt)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=0.1,
            max_tokens=2048,
        )

        content = response.choices[0].message.content or ""

        # Extract code blocks using regex
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", content, re.DOTALL)

        if code_blocks:
            return str(code_blocks[0]).strip()
        else:
            return str(content).strip()

    def __str__(self) -> str:
        """Returns generator information"""
        return f"Groq AI ({self.model_name})"


if __name__ == "__main__":
    generator = GroqAI()
    response = generator.generate(
        programming_language="python",
        prompt="Write a function to calculate the factorial of a number",
    )
    print(response)
