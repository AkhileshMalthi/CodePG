"""Module for AI-powered code generation services."""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import json

# LangChain imports
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import ollama

# CrewAI imports
from crewai import Agent, Task, Crew, Process

# Local imports
from .logger import setup_logger

# Set up module logger
logger = setup_logger(__name__)

# Templates for different file types
CODE_GENERATION_TEMPLATES = {
    "python": """
    You are an expert Python programmer. Write a Python program that accomplishes the following:
    
    {prompt}
    
    The code should be:
    - Well-commented
    - Follow PEP8 standards
    - Be efficient and readable
    - Include error handling where appropriate
    
    Return only the code without any explanations or markdown formatting.
    """,
    
    "javascript": """
    You are an expert JavaScript programmer. Write a JavaScript program that accomplishes the following:
    
    {prompt}
    
    The code should be:
    - Well-commented
    - Follow modern JS best practices
    - Be efficient and readable
    - Include error handling where appropriate
    
    Return only the code without any explanations or markdown formatting.
    """,
    
    # Templates for other languages can be added here
}

def get_default_template() -> str:
    """Get the default code generation template."""
    return """
    You are an expert programmer. Write code that accomplishes the following:
    
    {prompt}
    
    The code should be:
    - Well-commented
    - Follow best practices for the language
    - Be efficient and readable
    - Include error handling where appropriate
    
    Return only the code without any explanations or markdown formatting.
    """

class AICodeGenerator:
    """Class for generating code using AI models."""
    
    def __init__(self, model_type: str = "groq", api_key: Optional[str] = None, model_name: Optional[str] = None):
        """Initialize the code generator."""
        logger.info(f"Initializing AI code generator with model type: {model_type}")
        self.model_type = model_type.lower()
        
        # Try to get API key from parameter, then environment
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        # Default model names
        if model_name is None:
            if model_type.lower() == "groq":
                self.model_name = "mixtral-8x7b-32768"  # Updated to newer model
            else:
                self.model_name = "llama2"  # Default for Ollama
        else:
            self.model_name = model_name
        
        logger.debug(f"Using model: {self.model_name}")
        
        # Validate setup
        if self.model_type == "groq":
            if not self.api_key:
                logger.error("No Groq API key provided")
                raise ValueError(
                    "Groq API key is required. Please either:\n"
                    "1. Set GROQ_API_KEY environment variable\n"
                    "2. Pass api_key parameter\n"
                    "3. Set api_key in config file using:\n"
                    "   codepg config --set groq_api_key your_key_here\n"
                    "\nGet your API key from: https://console.groq.com/keys"
                )
            # Basic API key validation
            if not self._is_valid_api_key(self.api_key):
                logger.error("Invalid Groq API key format")
                raise ValueError(
                    "The provided Groq API key appears to be invalid.\n"
                    "Please check that you have copied the entire key correctly.\n"
                    "Valid API keys should start with 'gsk_' and be the correct length.\n"
                    "Get a new key from: https://console.groq.com/keys"
                )
        
        logger.info("AI code generator initialized successfully")

    def _is_valid_api_key(self, api_key: str) -> bool:
        """
        Validate Groq API key format.
        
        Current Groq API keys:
        - Start with 'gsk_'
        - Are approximately 48-52 characters long
        - Contain only alphanumeric characters and underscores
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Check basic format
        if not api_key.startswith('gsk_'):
            return False
            
        # Check approximate length (allowing some flexibility)
        if not (45 <= len(api_key) <= 55):
            return False
            
        # Check character set
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        return all(c in valid_chars for c in api_key[4:])  # Skip 'gsk_' prefix in validation

    def _get_groq_chain(self, template: str):
        """Create a LangChain chain using Groq API."""
        try:
            llm = ChatGroq(
                api_key=self.api_key,
                model=self.model_name,
                temperature=0.1
            )
            prompt = ChatPromptTemplate.from_template(template)
            return prompt | llm | StrOutputParser()
        except Exception as e:
            logger.error(f"Error creating Groq chain: {str(e)}")
            if "Invalid API Key" in str(e):
                raise ValueError(
                    "Invalid Groq API key. Please check your API key and try again.\n"
                    "Get your API key from: https://console.groq.com/keys"
                )
            raise

    def _use_ollama(self, template: str, prompt: str) -> str:
        """Generate code using local Ollama model."""
        try:
            formatted_prompt = template.format(prompt=prompt)
            response = ollama.generate(
                model=self.model_name,
                prompt=formatted_prompt,
                options={"temperature": 0.1}
            )
            
            if not response or 'response' not in response:
                raise ValueError("No response received from Ollama")
                
            return response['response']
        except Exception as e:
            logger.error(f"Error using Ollama: {str(e)}")
            if "connection refused" in str(e).lower():
                raise ConnectionError(
                    "Could not connect to Ollama. Please make sure Ollama is running.\n"
                    "Start Ollama with: 'ollama serve'"
                )
            raise

    def _use_crewai(self, language: str, prompt: str) -> str:
        """Generate code using CrewAI for more complex tasks."""
        try:
            if self.model_type == "groq":
                os.environ["LANGCHAIN_GROQ_API_KEY"] = self.api_key
                os.environ["GROQ_API_KEY"] = self.api_key
                
            # Create a programmer agent
            programmer = Agent(
                role="Senior Software Developer",
                goal=f"Write high-quality {language} code",
                backstory=f"You are an expert {language} developer with years of experience building clean, efficient code.",
                verbose=True,
                allow_delegation=False,
                tools=[]
            )
            
            # Create a code review agent
            reviewer = Agent(
                role="Code Reviewer",
                goal=f"Ensure code quality and best practices for {language}",
                backstory=f"You have deep expertise in {language} and are known for your attention to detail and code quality standards.",
                verbose=True,
                allow_delegation=False,
                tools=[]
            )
            
            # Create tasks
            coding_task = Task(
                description=f"Write {language} code that accomplishes: {prompt}. The code should be well-commented, follow best practices, and include error handling.",
                expected_output="Clean, working code that solves the given problem.",
                agent=programmer
            )
            
            review_task = Task(
                description="Review the code for bugs, inefficiencies, or style issues. Make improvements if necessary.",
                expected_output="Reviewed and improved code.",
                agent=reviewer,
                context=[coding_task]
            )
            
            # Create the crew
            crew = Crew(
                agents=[programmer, reviewer],
                tasks=[coding_task, review_task],
                verbose=2,
                process=Process.sequential
            )
            
            # Execute the tasks
            result = crew.kickoff()
            
            # Extract just the code from the result
            code_lines = []
            in_code_block = False
            
            for line in result.split("\n"):
                if "```" in line:
                    if not in_code_block:
                        in_code_block = True
                    else:
                        in_code_block = False
                elif in_code_block:
                    code_lines.append(line)
            
            # If no code block was found, return the whole result
            if not code_lines:
                return result
                
            return "\n".join(code_lines)
            
        except Exception as e:
            logger.error(f"Error using CrewAI: {str(e)}")
            raise

    def generate_code(self, language: str, prompt: str, use_crew: bool = False) -> str:
        """Generate code for the specified language based on the prompt."""
        logger.info(f"Generating {language} code with prompt: {prompt[:50]}...")
        
        try:
            # Select the appropriate template
            template = CODE_GENERATION_TEMPLATES.get(language.lower(), get_default_template())
            
            # For more complex tasks, use CrewAI
            if use_crew:
                logger.info("Using CrewAI for code generation")
                return self._use_crewai(language, prompt)
            
            # Use the appropriate model
            if self.model_type == "groq":
                logger.info("Using Groq API for code generation")
                try:
                    # Use Groq API via LangChain
                    chain = self._get_groq_chain(template)
                    result = chain.invoke({"prompt": prompt})
                    
                    # Validate the response
                    if isinstance(result, str) and result.strip():
                        logger.info("Code generated successfully")
                        return result
                    logger.error("Empty response from Groq API")
                    raise ValueError("Empty or invalid response from Groq API")
                    
                except json.JSONDecodeError:
                    logger.error("Invalid JSON response from Groq API")
                    raise ValueError("Invalid response format from Groq API")
                except Exception as e:
                    if "Invalid API Key" in str(e):
                        logger.error("Invalid Groq API key")
                        raise ValueError(
                            "Invalid Groq API key. Please check your API key and try again.\n"
                            "Get your API key from: https://console.groq.com/keys"
                        )
                    raise
                    
            elif self.model_type == "ollama":
                logger.info("Using Ollama for code generation")
                return self._use_ollama(template, prompt)
            else:
                logger.error(f"Unsupported model type: {self.model_type}")
                raise ValueError(f"Unsupported model type: {self.model_type}")
        
        except ValueError as e:
            logger.error(f"Value Error: {str(e)}")
            return f"# Error: {str(e)}\n# Please check your configuration and try again."
        except ConnectionError as e:
            logger.error(f"Connection Error: {str(e)}")
            return f"# Error: {str(e)}\n# Please check your network connection and try again."
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return (
                "# An unexpected error occurred while generating code.\n"
                f"# Error: {str(e)}\n"
                "# Please check your configuration and try again.\n"
                "# If the problem persists, try:\n"
                "#  1. Checking your API key\n"
                "#  2. Using a different model type\n"
                "#  3. Checking your network connection"
            )
