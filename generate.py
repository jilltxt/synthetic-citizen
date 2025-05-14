import os
from dotenv import load_dotenv
from openai import OpenAI

def load_api_key() -> str:
    """
    Loads the OpenAI API key from a .env file.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return api_key

def create_openai_client(api_key: str) -> OpenAI:
    """
    Creates an OpenAI client using the provided API key.
    """
    return OpenAI(api_key=api_key)

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

def generate_response(client: OpenAI, prompt: str) -> str:
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

def run_survey_loop(client: OpenAI):
    """
    Iterates over all gender and county combinations, generating and printing responses.
    """
    genders = ["mann", "kvinne"]
    counties = [
        "Oslo", "Viken", "Vestfold og Telemark", "Agder",
        "Rogaland", "Vestland", "Møre og Romsdal",
        "Trøndelag", "Nordland", "Troms og Finnmark"
    ]

    for gender in genders:
        for county in counties:
            prompt = generate_prompt(gender, county)
            response = generate_response(client, prompt)
            print(f"{gender.title()} fra {county}: {response}")

if __name__ == "__main__":
    api_key = load_api_key()
    client = create_openai_client(api_key)
    run_survey_loop(client)
