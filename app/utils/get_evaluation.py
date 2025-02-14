from langchain_ollama import ChatOllama
import yaml

def get_evaluation(rubric_component: str, student_response: str):

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
        ("user", f"""rubricComponent: {rubric_component},\nstudentResponse: {student_response}""")
    ]

    response = llm.invoke(messages)

    content = response.content

    return content