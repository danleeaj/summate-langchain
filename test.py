# import yaml
# from app.utils.get_evaluation import get_evaluation, evaluate_question
# from app.models.query_model import Query

# # Load config.yaml, read values and store them into constants

# with open("config.yaml", "r") as f:
#     config = yaml.safe_load(f)

# RUBRIC_COMPONENT = config['rubricComponent'][1]['component']
# RUBRIC_COMPONENTS = config['rubricComponent']
# STUDENT_RESPONSE = config['studentResponse'][0]

# def main():

#     # response, path = get_evaluation(Query(
#     #     rubricComponent=RUBRIC_COMPONENT,
#     #     studentResponse=STUDENT_RESPONSE
#     # ))

#     # print(response.model_dump_json(indent=2))

#     response_list, path_list = evaluate_question(
#         rubric_components=RUBRIC_COMPONENTS,
#         student_response=STUDENT_RESPONSE
#     )

#     for response in response_list:
#         print(response.model_dump_json(indent=2))

# if __name__ == "__main__":
#     main()

from app.utils.database_manager import DatabaseManager

with DatabaseManager() as db:
    question_id = db.add_question("Test")

print(question_id)