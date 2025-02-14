from langchain_ollama import ChatOllama
import yaml
import json
from app.utils.store_debug_log import store_debug_log
from langchain_core.messages.base import message_to_dict
from app.utils.models.query_model import Query

def get_evaluation(query: Query):

# Load config.yaml, read values and store them into constants

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    PROMPT = config['prompt']
    MODEL = config['model']
    TEMPERATURE = config['temperature']

    # Instantiate Ollama instance

    llm = ChatOllama(
        model=MODEL,
        temperature=TEMPERATURE,
    )

    # Set up message

    messages = [
        ("system", f"{PROMPT}"),
        ("user", f"{query.model_dump_json()}")
    ]

    response = llm.invoke(messages)

    content = response.content
    response = message_to_dict(response)

    path = store_debug_log(response)

    return content, path