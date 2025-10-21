import openai
import os
from dotenv import load_dotenv
import random
import pandas as pd
import csv

from data_mapping.get_parameters import gender, age, county, edu, occupation

synthetic_citizens = pd.read_csv("code/random_sample.csv")

def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


# Discussion on 27 May 2025 about two approaches:
# 1) Use a matrix of (real or synthetic) demographic variables in combination, produce responses based on that.
# 2) Generate one random synthetic citizen at a time, produce prompt, return AI-generated responses based on that.
# The second option requires that the function also returns the randomly generated values for the demographics.
# Also, doing 1) based on real demographics could produce reputational risk for NCP, so we will hold off on that.

# def generate_synthetic_citizen(*dict):
#     """
#     Generates a synthetic citizen with random demographic attributes, in the form of keys (numbers)
#     """
#     from data_mapping.get_parameters import gender, age, county, edu, occupation
#     random_keys = []
#     random_keys.append(random.choice(list(gender.keys())))
#     random_keys.append(random.choice(list(age.keys())))
#     random_keys.append(random.choice(list(county.keys())))
#     random_keys.append(random.choice(list(edu.keys())))
#     random_keys.append(random.choice(list(occupation.keys())))
#
#     return random_keys



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

def generate_responses(n_responses):
    survey_data = []
    client = get_openai_client()

    # use n_responses from the CSV file instead of generating on the fly and use gender_key etc to convert
    # each row (each "synthetic_citizen") into a prompt


    for i in range(n_responses):
        print(f"Iteration # {i}")
        #should fetch from random_sample.csv instead of generating on the fly
        demographics = synthetic_citizens.iloc[i]
        respid, gender_key, age_key, county_key, edu_key, occupation_key = demographics  # unpack - Do we need this? Inflexible, we could just put "demographics" directly into generate_prompt
        print(f"Demographics: {demographics}")  # optional for debugging

        prompt = generate_prompt(gender_key, age_key, county_key, edu_key, occupation_key)
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
        model = response.model
        print(f"Stripped response: {survey_response}\n\n\n")

        survey_data.append({
            "respid": respid,
            "gender_key": gender_key,
            "age_key": age_key,
            "county_key": county_key,
            "edu_key": edu_key,
            "occupation_key": occupation_key,
            "response": survey_response
        })

    df = pd.DataFrame(survey_data)
    df.to_csv("data/survey_results.csv", index=False)
    print("Saved to survey_results.csv")
    print(df)


if __name__ == "__main__":

    question =  """«Hvor bekymret er du for klimaendringer?
    
    Ikke bekymret i det hele tatt
    Lite bekymret
    Noe bekymret
    Bekymret
    Svært bekymret»
    """

    generate_responses(2)
