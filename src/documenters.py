from abc import ABC, abstractmethod
import aiofiles
import asyncio
from openai import AsyncOpenAI


class Documenter(ABC):
    """
    An abstract base class for a documenter service.
    """

    async def document(self, filename: str):
        """
        Method to automatically generate documentation for the provided file.

        Args:
            filename (str): The name of the file to document.
        """
        # Open the file asynchronously
        print(f"Beginning documentation of {filename=}")
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
        """
        Abstract method meant to be overriden by concrete implementation. It handles
        the generation of docstrings.

        Args:
            content (str): The content of the file to be documented.

        Returns:
            str: The updated content with generated docstrings.
        """
        pass


class ChatGPTDocumenter(Documenter):
    """
    Concrete LLM implementation using ChatGPT model.
    """
    def __init__(self):
        self.client = AsyncOpenAI(
            timeout=100,
            max_retries=3,
        )

        self.completion_kwargs = {"model": "gpt-4"}

        self.system_prompt = '''You are a helpful coding assistant.
You will be helping to write docstrings for python code.

- You only add and modify docstrings.
- You will be given the entire contents of a .py file.
- You return the entire contents of the .py file with the additional docstrings.
- If docstrings are already there, make them clearer if necessary.

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

A user will now provide you with their code. Document it accordingly.
'''


    async def generate_docs(self, content: str) -> str:
        """
        Asynchronous implementation for generating docstrings using the GPT-3
        chat model.

        Args:
            content (str): The content of the file to be documented.

        Returns:
            str: The updated content with generated docstrings.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content},
        ]

        response = await self.client.chat.completions.create(
            messages=messages, **self.completion_kwargs
        )
        output: str = response.choices[0].message.content
        return await self.format_output(output)

    async def format_output(self, input_str: str) -> str:
        """
        Removes the first and last line of the given string if they are triple backticks.

        Args:
        input_str (str): The input string to be formatted.

        Returns:
        str: The formatted string with the first and last lines removed if they are triple backticks.
        """
        lines = input_str.split("\n")
        if "```" in lines[0] and "```" in lines[-1]:
            return "\n".join(lines[1:-1])
        return input_str


class MockDocumenter(Documenter):
    """
    Mock implementation for a documenter.
    """

    async def generate_docs(self, content: str) -> str:
        """
        Asynchronously mocks the process of generating docstrings.

        Args:
            content(str): File content to be documented.

        Returns:
            str: Content with auto generated documentation summary line.
        """
        await asyncio.sleep(2)
        return "# This is automatically generated documentation\n" + content


async def select_documenter(name: str) -> Documenter:
    """
    Factory function to create an instance of Documenter based on the provided name.

    Args:
        name (str): Name of the Documenter to create. Can be "ChatGPT" or "MockDocumenter".

    Returns:
        Documenter: Instance of Documenter class.

    Raises:
        NotImplementedError: Raised when the name does not match any existing Documenter.
    """
    if name == "ChatGPT":
        return ChatGPTDocumenter()
    elif name == "MockDocumenter":
        return MockDocumenter()
    else:
        raise NotImplementedError(f"Error: Unknown Documenter '{name}'.")
