<h1 align="center">
  <a href="https://github.com/UoS-Darwin-Team-Pi/harpi">
    <picture>
      <source height="125" media="(prefers-color-scheme: dark)" srcset="./img/harpi_logo_dark.svg">
      <img height="125" alt="HarPi" src="./img/harpi_logo_light.svg">
    </picture>
  </a>
</h1>
<p align="center">
  <em>HarPi is an LLM-powered tool for data harmonisation, built on top of <a href="https://github.com/jataware/beaker-kernel">Beaker Kernel</a> and utilsing <a href="https://github.com/VIDA-NYU/bdi-kit">BDI-Kit</a>.</em>
</p>

## 📘 Introduction

Completed as part of the COM4520 Darwin Project, HarPi builds upon the functionality implemented in [Harmonia](https://github.com/VIDA-NYU/harmonia). HarPi adds the following functionality:

- Follows a definition of harmonisation outlined in the submitted paper. It generates a schema ad hoc by identifying similarities between multiple spreadsheets, and merges them together to match this custom-generated schema.
- Can generalise to any domain that is contained within the CSVs provided to it.
- Capable of handling an arbitrary number of spreadsheets.
- HarPi uses a [fork](https://github.com/UoS-Darwin-Team-Pi/bdi-kit) of BDI-kit for various bugfixes.

## 👥 Credits

Credit to the [Visualisation, Imaging, and Data Analysis Center at New York University (VIDA-NYU)](https://github.com/VIDA-NYU) and [Jataware](https://github.com/jataware).

## ⚙️ Installation

- Install [Docker](https://docs.docker.com/get-started/get-docker/).

- Add your OpenAI API key to the environment:

```
export OPENAI_API_KEY=your key goes here
```

- Then use `docker compose` to build and run the Beaker Development Interface:

```
docker compose build
docker compose up -d
```

- Navigate to `localhost:8888` to open the interface.

> [!IMPORTANT]
> To activate the agent, click on the top-left button to open the "Configure Context" window, select the `pi_context`, and then click "Apply". This will start a kernel with access to the HarPiContext agent.

## 🎬 Demo

> [!NOTE]
> Example CSVs can be found in `/csvs`.

The video below shows a short demo of the harmonisation process:

https://github.com/user-attachments/assets/56c52e94-44a1-46a9-868c-3bde1797c8eb

## 🛠️ Tools

- The agent supports the `top_matches()` and `match_values()` tools from [BDI-Kit](https://github.com/VIDA-NYU/bdi-kit). Documentation for their implementation are viewable [here](https://bdi-kit.readthedocs.io/stable/api.html).
- Tools implemented are defined in `src/pi_context/agent.py`.

HarPi implements the following tools:

| Function                                                                                   | Description                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `load_csvs(csv_paths)`                                                                   | Loads CSV files from user-specified file paths and stores them in a global variable. Accepts a list of file paths (e.g.,`["./my csv.csv", "/home/myuser/my csv directory"]`) and returns a list of variable names that the CSVs are stored under. |
| `get_csv_from_queue(exclude_csvs, remove_csv)`                                           | Retrieves the next available CSV from a queue. Optional arguments include `exclude_csvs` (a list of filenames to avoid) and `remove_csv` (a CSV filename to delete from the queue). Returns the name of the newly selected CSV.                 |
| `identify_mappings(primary_dataframe, secondary_dataframe)`                              | Identifies corresponding column mappings between two dataframes. Takes the variable names of the primary and secondary dataframes and returns the columns that match.                                                                               |
| `top_matches(source, target)`                                                            | Retrieves the top 10 schema matches between a source and target dataframe. Helps evaluate alternative column mappings. Returns the top 10 matching columns for each column in the source dataframe.                                                 |
| `match_values(primary_dataframe, secondary_dataframe, primary_column, secondary_column)` | Identifies matching values between specific columns in two dataframes. Takes the dataframe names and column names as input and returns value matches in markdown format.                                                                            |
| `perform_join(primary_dataframe, secondary_dataframe, column_mappings)`                  | Joins two dataframes using predefined column mappings and a value mapper. Returns the resulting joined dataframe.                                                                                                                                   |
| `save_join(path)`                                                                        | Saves the result of the join operation to a CSV file.                                                                                                                                                                                               |

## ➕ Adding Tools for the Agent

Additional tools can easily be added by copying the template for the `match_schema` tool in `/src/bdikit_context/agent.py`.

One thing to note is that `@tools` are managed by [Archytas](https://github.com/jataware/archytas). Archytas allows somewhat restricted argument types and does not allow direct passing of `pandas.DataFrame`. Instead, dataframes should be referenced by their variable names as a `str`. The actual code procedure that is executed (see `procedures/python3/match_schema.py`) treats the arguments from the `@tool` as variable names; when they should actually _be strings_ they should be wrapped in quotes as in the `match_schema.py` example. Procedures invoked by tools can have their arguments passed in using Jinja templating. For example:

```
column_mappings = bdi.match_schema({{ dataset }}, target="{{ target }}", method="{{ method }}")
```

Here `{{ dataset }}` is the string name of a `pandas.DataFrame` and is interpreted as a variable, where as `"{{ target }}"` is treated as a string such as `"gdc"`.

## ✏️ Prompt Modification

There are two main places to edit the agent's prompt. In `src/pi_context/context.py` the `auto_context` is a place to provide additional context. Currently the tools are enumerated here though this isn't strictly necessary. Additionally, prompt can be edited/managed in the `agent.py` `HarPiAgent` docstring.
