from crewai import Agent


def create_speech_agent(llm):
    return Agent(
        role="Speech and Pronunciation Coach",
        goal="Analyze spoken language patterns in the meeting transcript and provide actionable feedback",
        backstory=(
            "You are an expert speech coach with 20 years of experience helping professionals "
            "improve their spoken English. You specialize in identifying filler words, verbal tics, "
            "cadence issues, and speaking confidence patterns from transcripts. You provide specific, "
            "constructive feedback with concrete examples from the text."
        ),
        llm=llm,
        verbose=True,
    )


def create_grammar_agent(llm):
    return Agent(
        role="Professional English Grammarian",
        goal="Analyze grammar and syntax quality in the meeting transcript and provide structured improvement suggestions",
        backstory=(
            "You are a professional English grammarian and writing coach with deep expertise in "
            "syntax, sentence structure, and professional communication. You analyze transcripts "
            "to identify grammar errors, awkward constructions, and vocabulary improvement opportunities. "
            "You provide clear, prioritized feedback that helps speakers write and speak more precisely."
        ),
        llm=llm,
        verbose=True,
    )
