import os
import re
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

    def generate(self, prompt):
        """Generates response using Groq API and extracts code"""
        messages = [HumanMessage(content=prompt)]
        response = self.chat.invoke(messages)
        
        # Extract code blocks using regex
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response.content, re.DOTALL)
        
        if code_blocks:
            # Return the first code block found
            return code_blocks[0].strip()
        else:
            # If no code blocks found, return the raw response
            return response.content.strip()

    def __str__(self):
        """Returns generator information"""
        return "Groq Generator (Mixtral-8x7b)"
    
if __name__ == '__main__':
    generator = GroqGenerator()
    prompt = "Write a Python program to calculate the factorial of a number."
    response = generator.generate(prompt)
    print(response)
