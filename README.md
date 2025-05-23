<h1 align="center">
  <a href="https://github.com/UoS-Darwin-Team-Pi/harpi">
    <picture>
      <source height="125" media="(prefers-color-scheme: dark)" srcset="./img/harpi_logo_dark.svg">
      <img height="125" alt="HarPi" src="./img/harpi_logo_dark.svg">
    </picture>
  </a>
</h1>
<p align="center">
  <em>HarPi is an LLM-powered harmonisation tool for data harmonisation, built on top of <a href="https://github.com/jataware/beaker-kernel">Beaker</a> and utilsing <a href="https://github.com/VIDA-NYU/bdi-kit">BDI-Kit</a>.</em>
</p>

---

## ⚙️ Installation

First, add your OpenAI API key to the environment:

```
export OPENAI_API_KEY=your key goes here
```

Then use `docker compose` to build and run the Beaker Development Interface:

```
docker compose build
docker compose up -d
```

Navigate to [localhost:8888](localhost:8888) to open the interface.

> [!IMPORTANT]
> To activate the agent, click on the top-left button to open the "Configure Context" window, select the `bdikit_context`, and then click "Apply". To will start a kernel with access to the BDIKit agent.

## Demo

## Adding tools for the agent

[](https://github.com/VIDA-NYU/harmonia#adding-tools-for-the-agent)

Currently the agent supports multiple bdi-kit tools, including** **`match_schema()`,** **`match_values()`, and** **`materialize_mapping()`. Tools are implemented defined in** **`src/bdikit_context/agent.py`. Additional tools can easily be added by copying the template for the** **`match_schema` tool.

One thing to note is that** **`@tools` are managed by** **[Archytas](https://github.com/jataware/archytas). Archytas allows somewhat restricted argument types and does not allow direct passing of** **`pandas.DataFrame`. Instead, dataframes should be referenced by their variable names as a** **`str`. The actual code procedure that is executed (see** **`procedures/python3/match_schema.py`) treats the arguments from the** **`@tool` as variable names; when they should actually** ***be strings* they should be wrapped in quotes as in the** **`match_schema.py` example. Procedures invoked by tools can have their arguments passed in using Jinja templating. For example:

```
column_mappings = bdi.match_schema({{ dataset }}, target="{{ target }}", method="{{ method }}")
```

Here** **`{{ dataset }}` is the string name of a** **`pandas.DataFrame` and is interpreted as a variable, where as** **`"{{ target }}"` is treated as a string such as** **`"gdc"`.

## Prompt modification

[](https://github.com/VIDA-NYU/harmonia#prompt-modification)

There are two main places to edit the agent's prompt. In** **`src/bdikit_context/context.py` the** **`auto_context` is a place to provide additional context. Currently the tools are enumerated here though this isn't strictly necessary. Additionally, prompt can be edited/managed in the** **`agent.py` `BDIKitAgent` docstring.
