from archytas.tool_utils import AgentRef, LoopControllerRef, is_tool, tool, toolset
from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.config import config
from beaker_kernel.lib.context import BeakerContext

class HarmopizationAgent(BeakerAgent):
    """
    An agent that will help a user leverage NYU's BDIKit library for data harmonization.
    """

    @tool()
    async def output_statement(self, message: str, agent: AgentRef) -> str:
        """
        This function outputs a message to the user.
        The target is a string representing the message that the user wants repeated back to them.

        Args:
            message (str): The message that the user wants repeated back to them.

        Returns:
            str: returns the message

        You should show the user the result after this function runs.
        """

        code = agent.context.get_code(
            "output_statement",
            {
                "message": message,
            },
        )
        result = await agent.context.evaluate(
            code,
            parent_header={},
        )

        return result
