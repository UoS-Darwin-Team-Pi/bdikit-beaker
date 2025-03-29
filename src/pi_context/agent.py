from archytas.tool_utils import AgentRef, LoopControllerRef, is_tool, tool, toolset
from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.config import config
from beaker_kernel.lib.context import BeakerContext

class HarmopizationAgent(BeakerAgent):
    """
    An agent that will help a user leverage NYU's BDIKit library for data harmonization.
    """

    @tool()
    async def identify_mappings(self, primary_dataframe: str, secondary_dataframe: str, agent: AgentRef) -> str:
        """
        This function identifies a set of column mappings between a primary dataframe and a secondary dataframe.

        Args:
            primary_dataframe (str): The name of the primary dataset variable.
            secondary_dataframe (str): The name of the secondary dataset variable.

        Returns:
            str: returns the matched columns

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "identify_mappings",
            {
                "primary_dataframe": primary_dataframe,
                "secondary_dataframe": secondary_dataframe,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        match_result = result.get("return")

        return match_result

    @tool()
    async def top_matches(self, source: str, target: str, columns: str, agent: AgentRef) -> str:
        """
        Returns the top 10 schema matches between the source and target tables. This is useful
        for evaluating alternative column mappings.

        Args:
            source (str): The name of the source dataframe variable.
            target (str): The name of the target dataframe variable.
            columns (str): The column to match.

        Returns:
            str: returns the top 10 matches
        """

        code = agent.context.get_code(
            "top_matches",
            {
                "source_df": source,
                "target_df": target,
                "columns": columns,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        match_result = result.get("return")

        return match_result

    @tool()
    async def match_values(self, primary_dataframe: str, secondary_dataframe: str, primary_column: str, secondary_column: str, agent: AgentRef) -> str:
        """
        This function is used to identify value matches between columns in two dataframes.

        This function takes as input the source datasets and the column names to match between.

        Args:
            primary_dataframe (str): The name of the primary dataset variable.
            secondary_dataframe (str): The name of the secondary dataset variable.
            primary_column (str): The name of the column in primary_dataframe containing values that the secondary column should be mapped to.
            secondary_column (str): The name of the column in secondary_dataframe containing values which should be mapped to values within the primary dataframe.

        Returns:
            str: returns the identified value matches

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "match_values",
            {
                "primary_dataframe": primary_dataframe,
                "secondary_dataframe": secondary_dataframe,
                "primary_column": primary_column,
                "secondary_column": secondary_column,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        joined_table = result.get("return")

        return joined_table

    @tool()
    async def perform_join(self, primary_dataframe: str, secondary_dataframe: str, column_mappings: str, agent: AgentRef) -> str:
        """
        This function is used to join two dataframes together using identified column mappings.

        This function takes as input the source datasets and the column mappings, formated as a dictionary object.
        This dictionary object must include the primary and secondary column names that map to one another,
        and a value mapper object that transforms the values of the secondary column into the primary.

        The mapping specification must be a list of dictionaries.
        These dictionaries must have:
        - `primary`: The name of the primary table column.
        - `secondary`: The name of the secondary table column.
        - `mapper` (optional): A ValueMapper instance or an object that can be used to
          create one using :py:func:`~bdikit.api.create_mapper()`. Examples of valid objects
          are Python functions or lambda functions. If empty, an IdentityValueMapper
          is used by default.
        - `matches` (optional): Specifies the identified value matches. It must be a list of dictionaries containing
          secondary values and primary values, in the format [{"primary": "primaryvalue", "secondary": "secondaryvalue"}].

        Example:

        .. code-block:: python

            column_mappings = [
                {
                    # When no value mapping is need, specifying the primary and secondary is enough
                    "primary": "primary_column1",
                    "secondary": "secondary_column1",
                },
                {
                    # Data transformations can be specified using a mapper, which can be a custom Python lambda function (or a regular function)
                    "primary": "primary_column2",
                    "secondary": "secondary_column2",
                    "mapper": lambda age: -age * 365.25,
                },
                {
                    "primary": "primary_column3",
                    "secondary": "secondary_column3",
                    "matches": [
                        {
                            "primary": "primary_value1",
                            "secondary": "secondary_value1",
                        },
                        {
                            "primary": "primary_value2",
                            "secondary": "secondary_value2",
                        },
                    ]
                }
            ]

        Args:
            primary_dataframe (str): The name of the primary dataset variable.
            secondary_dataframe (str): The name of the secondary dataset variable.
            column_mappings (str): The name of the variable containing the dataframe of identified column mappings.

        Returns:
            str: returns the joined dataframe

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "perform_join",
            {
                "primary_dataframe": primary_dataframe,
                "secondary_dataframe": secondary_dataframe,
                "column_mappings": column_mappings,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        joined_table = result.get("return")

        return joined_table
