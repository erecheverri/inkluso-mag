"""
A simple wrapper around the OpenAI chat completions API.  This module is used by the
Inkluso Magazine pipeline to delegate online research tasks to OpenAI’s Agent Mode
(chat completions with a system prompt).

To configure this module, set the environment variables `OPENAI_API_KEY` and
`OPENAI_MODEL`.  The model defaults to `gpt-5-reasoning` if `OPENAI_MODEL` is
not provided.
"""
import os
import httpx


def run_agent(prompt: str, tools: list | None = None, system: str = "You are a precise magazine production agent.") -> str:
    """
    Send a prompt to OpenAI’s chat completions API and return the assistant’s reply.

    Parameters
    ----------
    prompt : str
        The user prompt to send to the agent.
    tools : list | None, optional
        Reserved for future use (e.g. Agent Mode tool selection).  Not currently used.
    system : str
        The system prompt to set the assistant’s behavior.

    Returns
    -------
    str
        The content of the assistant’s reply.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    model = os.environ.get("OPENAI_MODEL", "gpt-5-reasoning")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }
    response = httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
