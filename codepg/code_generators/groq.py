import os
import re
import yaml
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from .generator import Generator

class GroqGenerator(Generator):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.chat = ChatGroq(
            groq_api_key=api_key,
            model_name="mixtral-8x7b-32768"  # Using Mixtral model
        )
        
        # Load prompt template
        prompt_path = Path(__file__).parent.parent / "prompts" / "code_generation.yaml"
        with open(prompt_path, 'r') as f:
            self.prompt_template = yaml.safe_load(f)['template']

    def generate(self, programming_language: str, prompt: str) -> str:
        """Generates code in specified language based on the prompt"""
        formatted_prompt = self.prompt_template.format(
            language=programming_language,
            prompt=prompt
        )
        
        messages = [HumanMessage(content=formatted_prompt)]
        response = self.chat.invoke(messages)
        
        # Extract code blocks using regex
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response.content, re.DOTALL)
        
        if code_blocks:
            return code_blocks[0].strip()
        else:
            return response.content.strip()

    def __str__(self):
        """Returns generator information"""
        return "Groq Generator (Mixtral-8x7b)"
    
if __name__ == '__main__':
    generator = GroqGenerator()
    response = generator.generate(
        programming_language="python",
        prompt="Write a function to calculate the factorial of a number"
    )
    print(response)
