import openai
import os
from dotenv import load_dotenv
import random
import csv

from data_mapping.get_parameters import gender, age, county


def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


# Discussion on 27 May 2025 about two approaches:
# 1) Use a matrix of (real or synthetic) demographic variables in combination, produce responses based on that.
# 2) Generate one random synthetic citizen at a time, produce prompt, return AI-generated responses based on that.
# The second option requires that the function also returns the randomly generated values for the demographics.
# Also, doing 1) based on real demographics could produce reputational risk for NCP, so we will hold off on that.

def generate_synthetic_citizen(*dict):
    """
    Generates a synthetic citizen with random demographic attributes, in the form of keys (numbers)
    """
    from data_mapping.get_parameters import gender, age, county
    random_keys = []
    random_keys.append(random.choice(list(gender.keys())))
    random_keys.append(random.choice(list(age.keys())))
    random_keys.append(random.choice(list(county.keys())))
    # add: occupation
    # add: education
    return random_keys


''''# Generate 100 random draws
random_draws = [get_random_keys(dict1, dict2, dict3) for _ in range(100)]

# Write to CSV file
with open("random_draws.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Dict1_Key", "Dict2_Key", "Dict3_Key"])  # Column headers
    writer.writerows(random_draws)

print("CSV file 'random_draws.csv' created successfully!")
'''

def generate_prompt(gender_key, age_key, county_key) -> str:
    """
    Generates a survey prompt for a specific gender and county.
    """
    # gender_key = random.choice(list(gender.keys()))
    # age_key = random.choice(list(age.keys()))
    # county_key = random.choice(list(county.keys()))
    return (f"""
    Se for deg at du er en {gender[gender_key]} født i {age[age_key]}. Du bor i {county[county_key]}."
    Du deltar i en spørreundersøkelse. Hva svarer du på følgende spørsmål:

    «Hvor bekymret er du for klimaendringer?
    
    1 Ikke bekymret i det hele tatt
    2 Lite bekymret
    3 Noe bekymret
    4 Bekymret
    5 Svært bekymret»
# """
            )


#     return f"""
# Se for deg at du er en {gender} fra {county}. Du deltar i en spørreundersøkelse. Hva svarer du på følgende spørsmål:
#
# «Hvor bekymret er du for klimaendringer?
#
# 1 Ikke bekymret i det hele tatt
# 2 Lite bekymret
# 3 Noe bekymret
# 4 Bekymret
# 5 Svært bekymret»
# """

def generate_response(client, prompt: str) -> str:
    """
    Generates a response from the OpenAI model for a given prompt.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Du er et menneske bosatt i Norge som svarer på en spørreundersøkelse. Svar kun med ett tall fra 1 til 5 som beskrevet i prompten"
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


def main(client):
    """
    Iterates over all gender and county combinations, generating and printing responses.
    """

    for gender in genders:
        for county in counties:
            prompt = generate_prompt(gender, county)
            response = generate_response(client, prompt)
            print(f"{gender.title()} fra {county}: {response}")


if __name__ == "__main__":
    demographics = generate_synthetic_citizen()
    print(demographics)
    # prompt = generate_prompt(1,3,3)
        # some other time we can import demographic profiles from a CSV file here instead
    # print(prompt)
    prompt = generate_prompt(*demographics)
    print(prompt)
    #scitizen = generate_synthetic_citizen()
    #print(scitizen)
    # gender=get_gender(1)
    # print(gender)
    # exit()
    #
    # client = get_openai_client()
    # main(client)
