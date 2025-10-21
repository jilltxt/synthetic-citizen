import openai
import os
from dotenv import load_dotenv
import pandas as pd

from data_mapping.get_parameters import gender, age, county, edu, occupation

synthetic_citizens = pd.read_csv("code/random_sample.csv")

def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)



def generate_prompt(demographics, question) -> str:
    """
    Generates a survey prompt for a specific gender and county.
    Draws on the mappings in get_parameters.py
    """

    return (f"Du er en {gender[demographics['gender']]} født i {age[demographics['age']]} og du "
            f"bor i {county[demographics['county']]}. Du har utdanning fra {edu[demographics['edu']]}, "
            f"og er yrkesmessig tilknyttet {occupation[demographics['occupation']]}. "
            f"Du deltar i en spørreundersøkelse. Svar kun med et tall. "
            f"Hva svarer du på følgende spørsmål:\n\n{question}")

def generate_responses(n_responses):
    survey_data = []
    client = get_openai_client()

    for i in range(n_responses):
        print(f"Iteration # {i}")
        #should fetch from random_sample.csv instead of generating on the fly
        demographics = synthetic_citizens.iloc[i].to_dict()
        print(f"Demographics: {demographics}")  # optional for debugging

        prompt = generate_prompt(demographics)
        print(f"The prompt is: {prompt}")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=150
        )
        print(f"Response: {response}\n")

        survey_response = response.choices[0].message.content.strip()
        print(f"Stripped response: {survey_response}\n\n\n")

        survey_data.append({
            "respid": demographics['respid'],
            "gender": demographics['gender'],
            "edu": demographics['edu'],
            "age": demographics['age'],
            "county": demographics['county'],
            "occupation": demographics['occupation'],
            "response": survey_response,
            #add refusal
        })

    df = pd.DataFrame(survey_data)
    df.to_csv("data/survey_results.csv", index=False) #add date, model, temperature to filename
    print("Saved to survey_results.csv")
    print(df)


if __name__ == "__main__":

    '''question =  """«Hvor bekymret er du for klimaendringer?
    
    1 Ikke bekymret i det hele tatt
    2 Lite bekymret
    3 Noe bekymret
    4 Bekymret
    5 Svært bekymret»
    """
    '''

    generate_responses(5)
