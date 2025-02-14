import yaml
from app.utils.get_evaluation import get_evaluation

def main():

    # Load config.yaml, read values and store them into constants

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    RUBRIC_COMPONENT = config['rubricComponent'][0]['component']
    STUDENT_RESPONSE = config['studentResponse'][0]

    response, path = get_evaluation(rubric_component=RUBRIC_COMPONENT, student_response=STUDENT_RESPONSE)

    print(response)

if __name__ == "__main__":
    main()