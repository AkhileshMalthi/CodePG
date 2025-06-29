import re
from pathlib import Path

import ollama
import yaml

from codepg.ai import AI


class OllamaAI(AI):
    def __init__(self, model_name: str = "llama3.2"):
        """Initialize Ollama generator with specified model"""
        self.model_name = model_name

        # Load prompt template
        prompt_path = Path(__file__).parent.parent / "prompts" / "code_generation.yaml"
        with open(prompt_path) as f:
            self.prompt_template = yaml.safe_load(f)["template"]

    def generate(self, programming_language: str, prompt: str) -> str:
        """Generates code in specified language based on the prompt"""
        try:
            # Format prompt using template
            formatted_prompt = self.prompt_template.format(
                language=programming_language, prompt=prompt
            )

            # Generate response using Ollama
            response = ollama.generate(model=self.model_name, prompt=formatted_prompt)

            if not response or "response" not in response:
                raise RuntimeError("No response received from Ollama")

            # Extract code blocks using regex
            code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response["response"], re.DOTALL)

            if code_blocks:
                return str(code_blocks[0]).strip()
            else:
                return str(response["response"]).strip()

        except Exception as e:
            raise RuntimeError(f"Error generating code with Ollama: {str(e)}") from e

    def __str__(self) -> str:
        """Returns generator information"""
        return f"OllamaAI({self.model_name})"


if __name__ == "__main__":
    generator = OllamaAI()
    response = generator.generate(
        programming_language="python",
        prompt="Write a function to calculate the factorial of a number",
    )
    print(response)
