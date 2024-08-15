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
            target (str): The target table or standard data vocabulary. Defaults to “gdc”.
            method (str): The method used for mapping. Defaults to “coma”.

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