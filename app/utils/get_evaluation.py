from langchain_ollama import ChatOllama
import yaml
import json
from app.utils.store_debug_log import store_debug_log
from langchain_core.messages.base import message_to_dict
from app.models.query_model import Query
from app.models.response_model import Response

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
    ).with_structured_output(schema=Response, include_raw=True)

    # Set up message

    messages = [
        ("system", f"{PROMPT}"),
        ("user", f"{query.model_dump_json()}")
    ]

    response = llm.invoke(messages)

    raw_response = response['raw']
    parsing_error = bool(response['parsing_error'])

    parsed_response = response['parsed'] if not parsing_error else ''

    response = message_to_dict(raw_response)
    response['parsed'] = str(parsed_response)

    path = store_debug_log(response)

    return parsed_response, path