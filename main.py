import yaml
from app.utils.get_evaluation import get_evaluation
from app.models.query_model import Query

# Load config.yaml, read values and store them into constants

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

RUBRIC_COMPONENT = config['rubricComponent'][1]['component']
STUDENT_RESPONSE = config['studentResponse'][0]

def main():

    response, path = get_evaluation(Query(
        rubricComponent=RUBRIC_COMPONENT,
        studentResponse=STUDENT_RESPONSE
    ))

    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    main()