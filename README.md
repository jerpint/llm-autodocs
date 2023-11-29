# llm-autodocs 🪄

## Overview 🌞

`autodocs` is a Python-based command-line tool for automatically generating documentation for git-tracked Python files in a project. It leverages LLMs to generate documentation automatically and asynchronously.

## Features ⚡️
* Git Integration: Only selects Python files that are tracked by Git within a specified directory.
* Custom File Selection: Offers the flexibility to specify files to include or exclude in the documentation process.
* LLM Support: Currently supports OpenAI gpt models
* Asynchronous Execution: Improves performance by handling multiple files concurrently.

## Quickstart 🚴‍♂️

Install the library:

```bash
pip install llm-autodocs
```

Navigave to your git project and run:

```bash
cd my_project/
autodocs --directory .
```


This will run in the root of your project and include all tracked .py files. By default it uses `gpt-3.5-turbo`.

You will be prompted to review the files affected before continuing.

## Examples

Specify a specific directory:

    autodocs --directory ./src

Specify a different openai model (can be any of the gpt-3.5* or gpt-4* patterns):

    autodocs --documenter gpt-4

Allow only certain file patterns:

    autodocs --allowed-files utils.py data_model.py

Exclude certain file patterns:

    autodocs --ignored-files __init__.py