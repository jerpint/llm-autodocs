from abc import ABC, abstractmethod
import aiofiles
from openai import AsyncOpenAI

# Base class for LLMs
class Documenter(ABC):
    async def document(self, filename: str):
        # Open the file asynchronously
        async with aiofiles.open(filename, "r") as f:
            content = await f.read()

        # Generate the docstrings
        try:
            modified_content = await self.generate_docs(content)
        except Exception as e:
            print(
                f"Something went wrong generating docs for {filename=}. See Traceback\n{e}"
            )
            return

        # Write the modified contents back to original file
        async with aiofiles.open(filename, "w") as f:
            await f.write(modified_content)

    @abstractmethod
    async def generate_docs(self, content: str) -> str:
        pass


# Concrete LLM implementations
class ChatGPTDocumenter(Documenter):
    def __init__(self):
        self.client = AsyncOpenAI(
            timeout=100,
            max_retries=3,
        )

        self.system_prompt = '''You are a helpful coding assistant.
You will be helping to write docstrings for python code.

- You only add and modify docstrings.
- You will be given the entire contents of a .py file.
- You return the entire contents of the .py file with the additional docstrings.
- If docstrings are already there, make them clearer if necessary.
- Do not include backticks when replying, like ```python\n...\n```

** YOU DO NOT MODIFY ANY CODE **

Here is an example of how you would operate. Given:

def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    if minimum < 1024:
        raise ValueError(f"Min. port must be at least 1024, not {minimum}.")
    port = self._find_next_open_port(minimum)
    if port is None:
        raise ConnectionError(
            f"Could not connect to service on port {minimum} or higher."
        )
    assert port >= minimum, f"Unexpected port {port} when minimum was {minimum}."
    return port

You would return:

def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    if minimum < 1024:
        # Note that this raising of ValueError is not mentioned in the doc
        # string's "Raises:" section because it is not appropriate to
        # guarantee this specific behavioral reaction to API misuse.
        raise ValueError(f"Min. port must be at least 1024, not {minimum}.")
    port = self._find_next_open_port(minimum)
    if port is None:
        raise ConnectionError(
            f"Could not connect to service on port {minimum} or higher."
        )
    assert port >= minimum, f"Unexpected port {port} when minimum was {minimum}."
    return port

Remember:

- You only add and modify docstrings.
- You will be given the entire contents of a .py file.
- You return the entire contents of the .py file with the additional docstrings.
- If docstrings are already there, make them clearer if necessary.
- Do not include backticks when replying, like ```python\n...\n```

A user will now provide you with their code. Document it accordingly.
'''

        self.completion_kwargs = {"model": "gpt-3.5-turbo-1106"}

    async def generate_docs(self, content: str) -> str:
        # Asynchronous implementation for LLM1
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content},
        ]

        response = await self.client.chat.completions.create(
            messages=messages, **self.completion_kwargs
        )
        output: str = response.choices[0].message.content
        return output


class MockDocumenter(Documenter):
    async def generate_docs(self, content: str) -> str:
        # Asynchronous mock implementation for LLM2
        return "# This is automatically generated documentation\n" + content


# Factory to create LLM instances
async def select_documenter(name: str) -> Documenter:
    if name == "ChatGPT":
        return ChatGPTDocumenter()
    elif name == "MockDocumenter":
        return MockDocumenter()
    else:
        raise NotImplementedError(f"Error: Unknown Documenter '{name}'.")
