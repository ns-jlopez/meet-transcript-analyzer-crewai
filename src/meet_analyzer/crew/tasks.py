from crewai import Task


def create_speech_task(agent, transcript):
    return Task(
        description=(
            "Analyze the following meeting transcript for spoken language patterns.\n\n"
            "Focus on:\n"
            "- Filler words (um, uh, like, you know, so, basically) — count frequency and give examples\n"
            "- Repetitive phrases or verbal tics\n"
            "- Sentence cadence issues (run-on speech, abrupt stops, unfinished thoughts)\n"
            "- Speaking confidence indicators (hedging, unnecessary qualifiers)\n\n"
            "Provide specific examples from the transcript for each issue found.\n\n"
            f"TRANSCRIPT:\n{transcript}"
        ),
        expected_output=(
            "A structured Markdown report with sections for each analysis area. "
            "Each section should include specific examples quoted from the transcript, "
            "frequency counts where applicable, and concrete improvement suggestions."
        ),
        agent=agent,
    )


def create_grammar_task(agent, speech_task):
    return Task(
        description=(
            "Analyze the following meeting transcript for grammar and syntax quality.\n\n"
            "Focus on:\n"
            "- Sentence structure issues (fragments, run-ons, dangling modifiers)\n"
            "- Subject-verb agreement errors\n"
            "- Tense consistency\n"
            "- Word choice and vocabulary level (imprecise or informal words)\n"
            "- Clarity and conciseness improvements\n\n"
            "Note: The speech analysis has already been completed. "
            "Focus on grammar and syntax — do not repeat speech pattern observations. "
            "Provide specific examples from the transcript for each issue.\n\n"
            "The transcript is the same one used in the speech analysis task above."
        ),
        expected_output=(
            "A structured Markdown report with sections for each grammar dimension. "
            "Each section should include specific examples quoted from the transcript "
            "and concrete rewrite suggestions."
        ),
        agent=agent,
        context=[speech_task],
    )
