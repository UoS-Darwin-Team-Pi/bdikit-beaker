from archytas.tool_utils import AgentRef, LoopControllerRef, is_tool, tool, toolset
from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.context import BeakerContext


class BDIKitAgent(BeakerAgent):
    """
    An agent that will help a user leverage NYU's BDIKit library for data harmonization.
    """

    @tool()
    async def match_schema(self, dataset: str, target: str, method: str, agent: AgentRef) -> str:
        """
        This function performs schema mapping between the source table and the given target schema. 
        The target is either a DataFrame or a string representing a standard data vocabulary supported by the library. 
        Currently, only the GDC (Genomic Data Commons) standard vocabulary is supported.

        Args:
            dataset (str): The name of the dataset variable.
            target (str): The target table or standard data vocabulary. Defaults to "gdc".
            method (str): The method used for mapping. Defaults to "ct_learning".

        Returns:
            str: returns the matched columns

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "match_schema",
            {
                "dataset": dataset,
                "target": target,
                "method": method,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        match_result = result.get("return")

        return match_result


    @tool()
    async def top_matches(self, dataset: str, columns: str, target: str, agent: AgentRef) -> str:
        """
        Returns the top 10 schema matches between the source and target tables. This is useful
        for evaluating alternative column mappings.

        Args:
            dataset (str): The name of the dataset variable.
            columns (str): The column to match.
            target (str): The target table or standard data vocabulary. Defaults to “gdc”.

        Returns:
            str: returns the top 10 matches

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "top_matches",
            {
                "dataset": dataset,
                "columns": columns,
                "target": target
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        match_result = result.get("return")

        return match_result


    @tool()
    async def match_values(self, dataset: str, column_mapping: str, target: str, method: str, agent: AgentRef) -> str:
        """
        Returns the top 10 value matches between the value of the source and target columns.
        This is useful for evaluating value matches between a pair columns (column mappings) returned by the match_schema function.

        Args:
            dataset (str): The name of the dataset variable.
            column_mapping (tuple): The column and target names for which to find value matches for. The values must be separated by a comma, example: "source_column,target_column"
            target (str): The target table or standard data vocabulary. Defaults to “gdc”.
            method (str): The method used for mapping. Defaults to “tfidf”.

        Returns:
            str: returns the value matches for the given column mapping (source and target column names)

        You should show the user the result after this function runs.
        Uppon user's request, the output of match_values() can be fed to materialize_mapping() which materializes the final target using both schema and value mappings.
        """

        code = agent.context.get_code(
            "match_values",
            {
                "dataset": dataset,
                "column_mapping": tuple(column_mapping.split(',')),
                "target": target,
                "method": method,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        match_result = result.get("return")

        return match_result


    @tool()
    async def materialize_mapping(self, dataset: str, mapping_spec: str, output_file: str, agent: AgentRef) -> str:
        """
        Materializes the final (harmonized) table after applying data transformations specified by the schema mapping and value mappings specifications.

        This function takes as input the source dataset and the mapping specifications
        (schema and value mappings) formated as a MappingSpecLike dictionary object.
        The `MappingSpecLike` is a type alias that specifies mappings between source
        and target columns. It must include the source and target column names
        and a value mapper object that transforms the values of the source column
        into the target.

        The mapping specification can be (1) a DataFrame or (2) a list of dictionaries or DataFrames.
        If it is a list of dictionaries, they must have:
        - `source`: The name of the source column.
        - `target`: The name of the target column.
        - `mapper` (optional): A ValueMapper instance or an object that can be used to
          create one using :py:func:`~bdikit.api.create_mapper()`. Examples of valid objects
          are Python functions or lambda functions. If empty, an IdentityValueMapper
          is used by default.
        - `matches` (optional): Specifies the value mappings. It must be a list of tuples
          containing a pair of source and target values (<source_value>, <target_value>).
          Please make sure to always represent pairs of source and target values using
          Python tuples (with parenthesis). Do NOT use a lists of lists.

        Alternatively, the list can contain DataFrames. In this case, the DataFrames must
        contain not only the value mappings (as described in the `matches` key above) but
        also the `source` and `target` columns as DataFrame attributes. The DataFrames created
        by :py:func:`~bdikit.api.match_values()` include this information by default.
        If the mapping specification is a DataFrame, it must be compatible with the dictionaries
        above and contain `source`, `target`, and `mapper` or `matcher` columns.

        Example:

        .. code-block:: python

            mapping_spec = [
                {
                    # When no value mapping is need, specifying the source and target is enough
                    "source": "source_column1",
                    "target": "target_column1",
                },
                {
                    # Data transformations can be specified using a mapper, which can be a custom Python lambda function (or a regular function)
                    "source": "source_column2",
                    "target": "target_column2",
                    "mapper": lambda age: -age * 365.25,
                },
                {
                    "source": "source_column3",
                    "target": "target_column3",
                    "matches": [
                        ("source_value1", "target_value1"),
                        ("source_value2", "target_value2"),
                    ]
                }
            ]

        Args:
            dataset (str): The name of the dataset variable.
            mapping_spec (MappingSpecLike): the column and value mapping specificiation.
            output_file (str): The name of the output file to save the materialized target. Detaults to "harmonized_table.csv".

        Returns:
            str: returns the materialized target using both schema and value mappings
        """

        code = agent.context.get_code(
            "materialize_mapping",
            {
                "dataset": dataset,
                "mapping_spec": mapping_spec,
                "output_file": output_file,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        materialize_result = result.get("return")

        return materialize_result
