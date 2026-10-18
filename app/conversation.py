"""Conversation history: rewrite follow-up questions into standalone questions.

A follow-up like "Can you explain it more simply?" cannot be searched in Chroma:
it does not say what "it" is. Using the previous messages, the LLM first rewrites
it into a standalone question ("Can you explain atomicity in ACID more simply?"),
which is then used for both retrieval and generation.
"""
from langchain_core.prompts import ChatPromptTemplate

from app.generation import llm

# Only the last messages are sent, to keep the prompt short (and fast on CPU)
MAX_HISTORY_MESSAGES = 6
MAX_MESSAGE_CHARS = 500

condense_prompt = ChatPromptTemplate.from_template(
    """
Given the conversation below and a follow-up question, rewrite the follow-up question
so that it can be understood on its own, without the conversation.

Rules:
- Replace words like "it", "this", "that", "they" with what they refer to.
- Keep the same language and the same intent. Do not answer the question.
- If the question is already understandable on its own, return it unchanged.
- Return only the rewritten question, nothing else.

Conversation:
{history}

Follow-up question: {question}

Standalone question:"""
)

condense_chain = condense_prompt | llm


def format_history(history):
    lines = []
    for message in history[-MAX_HISTORY_MESSAGES:]:
        speaker = "Student" if message.role == "user" else "Tutor"
        lines.append(f"{speaker}: {message.content[:MAX_MESSAGE_CHARS]}")
    return "\n".join(lines)


def condense_question(question, history):
    """Return a standalone version of the question (unchanged if there is no history)."""
    if not history:
        return question

    standalone = condense_chain.invoke({
        "history": format_history(history),
        "question": question
    }).content.strip().strip('"')

    # Safety net: never send an empty question to the retriever
    return standalone or question
