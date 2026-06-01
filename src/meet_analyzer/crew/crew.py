import json

from crewai import Crew

from meet_analyzer.crew.agents import create_speech_agent, create_grammar_agent
from meet_analyzer.crew.llm import create_llm
from meet_analyzer.crew.tasks import create_speech_task, create_grammar_task


def _patch_bedrock_tool_arg_parsing():
    """Normalize Bedrock-style tool calls into OpenAI-style before CrewAI's executor processes them.

    Bedrock returns tool calls as dicts with 'name' and 'input' keys.
    CrewAI's executor expects OpenAI-style objects with a 'function.arguments' string.
    """
    from crewai.agents.crew_agent_executor import CrewAgentExecutor

    _original = CrewAgentExecutor._handle_native_tool_calls

    def _patched(self, tool_calls, available_functions):
        normalized = []
        for tc in tool_calls:
            if isinstance(tc, dict) and "input" in tc and "function" not in tc and "name" in tc:
                obj = type("ToolCall", (), {
                    "function": type("Function", (), {
                        "name": tc["name"],
                        "arguments": json.dumps(tc.get("input", {})),
                    })(),
                    "id": tc.get("toolUseId") or tc.get("id") or f"call_{id(tc)}",
                })()
                normalized.append(obj)
            else:
                normalized.append(tc)
        return _original(self, normalized, available_functions)

    CrewAgentExecutor._handle_native_tool_calls = _patched


_patch_bedrock_tool_arg_parsing()


class TranscriptAnalyzerCrew:
    def __init__(self, transcript, llm_provider="bedrock", llm_model=None):
        self.transcript = transcript
        self.llm_provider = llm_provider
        self.llm_model = llm_model

    def run(self):
        llm = create_llm(self.llm_provider, self.llm_model)
        speech_agent = create_speech_agent(llm)
        grammar_agent = create_grammar_agent(llm)
        speech_task = create_speech_task(speech_agent, self.transcript)
        grammar_task = create_grammar_task(grammar_agent, speech_task)
        crew = Crew(agents=[speech_agent, grammar_agent], tasks=[speech_task, grammar_task], verbose=True)
        return crew.kickoff()
