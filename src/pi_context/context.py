from typing import Dict, Any
from beaker_kernel.lib.context import BeakerContext

from .agent import HarmopizationAgent

class PiContext(BeakerContext):

    enabled_subkernels = ["python3"]

    SLUG = "pi_context"

    def __init__(self, beaker_kernel: "BeakerKernel", config: Dict[str, Any]):
        super().__init__(beaker_kernel, HarmopizationAgent, config)

    async def setup(self, context_info=None, parent_header=None):
        super().setup(context_info, parent_header)

    async def auto_context(self):
            return f"""
            You are an assistant whose sole purpose is to repeat messages back to the user.
            You have access to the "output_statement" tool, which can be used to repeat a message.
            
            You should always explain which tool you are using, how you are calling it, and the output of the tool.
            """.strip()
