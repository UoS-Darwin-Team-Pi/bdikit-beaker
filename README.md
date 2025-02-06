# Harmonia: An Interactive Data Harmonization Agent

Harmonia is a data harmonization that leverages the [bdi-kit library](https://bdi-kit.readthedocs.io/en/latest/index.html) to perform data harmonization.

## Running Harmonia

First, add your OpenAI API key to the environment:

```
export OPENAI_API_KEY=your key goes here
```

Then use `docker compose` to build and run the BDIKit Beaker context:

```
docker compose build
docker compose up -d
```

Navigate to `localhost:8888` to open the UI.

> [!IMPORTANT]
> To activate the agent, click on the top-left button to open the "Configure Context" window, select the `bdikit_context`, and then click "Apply". To will start a kernel with access to the BDIKit agent.

## Example


The docker image includes a file named `dou.csv` by default that can be used. You can experiment with the following script that loads the file and executes a few harmonization tasks.

```
Load the file dou.csv as a dataframe and subset it to the following columns: Country, Histologic_Grade_FIGO, Histologic_type, FIGO_stage, BMI, Age, Race, Ethnicity, Gender, Tumor_Focality, Tumor_Size_cm.
```

```
Please match this to the GDC schema using the 'ct_learning' method, and fix any results that don't look correct.
```

```
Find alternative mappings for Histologic_type.
```

```
Find alternative mappings for Tumor_Size_cm.
```

```
Find value mappings for the columns Country, Histologic_Grade_FIGO, Histologic_type, FIGO_stage, Race, Ethnicity, Gender, Tumor_Focality. If there are any errors in the mappings, please provide suggestions.
```

```
Please create a final harmonized table based on the discovered column and value mappings and save it at "dou_harmonized.csv".
```

```
Show dou_harmonized.csv and the initial subsetted dou.csv file one after the other for comparison.
```

## Adding tools for the agent

Currently the agent supports multiple bdi-kit tools, including `match_schema()`, `match_values()`, and `materialize_mapping()`.
Tools are implemented defined in `src/bdikit_context/agent.py`.
Additional tools can easily be added by copying the template for the `match_schema` tool.

One thing to note is that `@tools` are managed by [Archytas](https://github.com/jataware/archytas). Archytas allows somewhat restricted argument types and does not allow direct passing of `pandas.DataFrame`. Instead, dataframes should be referenced by their variable names as a `str`. The actual code procedure that is executed (see `procedures/python3/match_schema.py`) treats the arguments from the `@tool` as variable names; when they should actually _be strings_ they should be wrapped in quotes as in the `match_schema.py` example. Procedures invoked by tools can have their arguments passed in using Jinja templating. For example:

```
column_mappings = bdi.match_schema({{ dataset }}, target="{{ target }}", method="{{ method }}")
```

Here `{{ dataset }}` is the string name of a `pandas.DataFrame` and is interpreted as a variable, where as `"{{ target }}"` is treated as a string such as `"gdc"`.

## Prompt modification
There are two main places to edit the agent's prompt. In `src/bdikit_context/context.py` the `auto_context` is a place to provide additional context. Currently the tools are enumerated here though this isn't strictly necessary. Additionally, prompt can be edited/managed in the `agent.py` `BDIKitAgent` docstring.