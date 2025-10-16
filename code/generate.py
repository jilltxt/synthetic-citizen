import openai
import os
from dotenv import load_dotenv
import pandas as pd
import yaml

from data_mapping.get_parameters import gender, age, county, edu, occupation

def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def load_questions(path="data/survey_questions.yaml"):
    """Load questions from YAML file into a dict keyed by id.
    Questions in the YAML file are in the format
    - id: Q1
      text: "Hva er din holdning til X?"
    This function converts it to a list of dicts each with the keys id and text

    [
    {"id": "Q07", "text": "Diskriminering mot kvinner ..."},
    {"id": "Q08", "text": "Om en person er mann eller kvinne ..."}
    ]
    It adds q to the start of id and text so qid is question id and qtext is question text.
    This is used in generate_prompt()
    """

    with open(path, encoding="utf-8") as f:
        questions = yaml.safe_load(f)
    return {question_["id"]: question_["text"] for q in questions}

def generate_prompt(gender_key, edu_key, age_key, county_key, occupation_key) -> str:
    """
    Generates a survey prompt for a specific gender and county.
    Draws on the mappings in get_parameters.py
    """

    return (f"Du er en {gender[gender_key]} født i {age[age_key]} og du "
            f"bor i {county[county_key]}. Du har utdanning fra {edu[edu_key]}, "
            f"og er yrkesmessig tilknyttet {occupation[occupation_key]}. "
            f"Du deltar i en spørreundersøkelse. Svar kun med et tall. "
            f"Hva svarer du på følgende spørsmål:\n\n{question}")

def generate_responses(csv_path, yaml_path="data/survey_questions.yaml"):
    """Iterate over respondents and questions, collect AI responses.
    This needs work - also need to get the random_sample.csv file from generate10k.py"""
    df = pd.read_csv(csv_path)
    questions = load_questions(yaml_path)
    client = get_openai_client()

    survey_data = []

    for i, row in df.iterrows():
        for question_id, question_text in questions.items():
            print(f"Iteration #{i}, respondent {row['resp_id']}, question {question_id}")

            prompt = generate_prompt(
                row["gender"], row["age"], row["county"],
                row["edu"], row["occupation"], question_text
            )

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=150
            )

            survey_response = response.choices[0].message.content.strip()

            survey_data.append({
                "resp_id": row["resp_id"],
                "question_id": qid,
                "response": survey_response,
                "gender": row["gender"],
                "age": row["age"],
                "county": row["county"],
                "edu": row["edu"],
                "occupation": row["occupation"]
            })

    out_path = "data/survey_results.csv"
    pd.DataFrame(survey_data).to_csv(out_path, index=False)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    load_questions("data/survey_questions.yaml")

    # example run:
#    generate_responses("code/random_sample.csv", "data/survey_questions.yaml")