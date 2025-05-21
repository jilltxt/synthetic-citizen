import openai
import os
from dotenv import load_dotenv

from data_mapping.get_gender import get_gender


def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def generate_prompt(gender: str, county: str) -> str:
    """
    Generates a survey prompt for a specific gender and county.
    """
    return f"""
Se for deg at du er en {gender} fra {county}. Du deltar i en spørreundersøkelse. Hva svarer du på følgende spørsmål:

«Hvor bekymret er du for klimaendringer?

1 Ikke bekymret i det hele tatt  
2 Lite bekymret  
3 Noe bekymret  
4 Bekymret  
5 Svært bekymret»
"""

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
    genders = ["mann", "kvinne"]
    counties = [
        "Oslo", "Viken", "Vestfold", "Telemark", "Agder",
        "Rogaland", "Vestland", "Møre og Romsdal",
        "Trøndelag", "Nordland", "Troms" , "Finnmark"
    ]

    for gender in genders:
        for county in counties:
            prompt = generate_prompt(gender, county)
            response = generate_response(client, prompt)
            print(f"{gender.title()} fra {county}: {response}")

if __name__ == "__main__":
    gender=get_gender(1)
    print(gender)
    exit()

    client = get_openai_client()
    main(client)
