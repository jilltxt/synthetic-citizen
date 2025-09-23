import openai
import os
from dotenv import load_dotenv
import random
import pandas as pd
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

    #Pre-prompt here - comment out the language we don't want to use
    return (f"Du er en {gender[gender_key]} født i {age[age_key]}. Du bor i {county[county_key]}. Du deltar i en spørreundersøkelse. Svar kun med et tall. Hva svarer du på følgende spørsmål:\n\n{question}")
    #return (f"You are a {gender[gender_key]} born in {age[age_key]}. You live in {county[county_key]}. You are participating in a survey. Answer with a number and nothing else. What is your response to the following question:\n\n{question}")

def generate_responses(n_responses):
    survey_data = []
    client = get_openai_client()

    for i in range(n_responses):
        print(f"Iteration # {i}")
        demographics = generate_synthetic_citizen()
        gender_key, age_key, county_key = demographics  # unpack - Do we need this? Inflexible, we could just put "demographics" directly into generate_prompt
        print(f"Demographics: {demographics}")  # optional for debugging

        prompt = generate_prompt(gender_key, age_key, county_key)
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
            "gender_key": gender_key,
            "age_key": age_key,
            "county_key": county_key,
            "response": survey_response
        })

    df = pd.DataFrame(survey_data)
    df.to_csv("data/survey_results.csv", index=False)
    print("Saved to survey_results.csv")
    print(df)


if __name__ == "__main__":
    # prompt = generate_prompt(1,3,3)
    # some other time we can import demographic profiles from a CSV file here instead
    # print(prompt)

    # spørsmål uten tall -> nekter stort sett å svare - "som en AI..."

    # r31_inruw
    '''question = """Hvor enig eller uenig er du i påstanden nedenfor?
    Norge har en moralsk plikt til å støtte Ukraina i kampen mot Russland. 
    
    Her er svaralternativene - velg ett:
    Svært enig
    Enig
    Noe enig
    Verken enig eller uenig
    Noe uenig
    Uenig
    Svært uenig"""
    '''

    '''question = """To what extent do you agree or disagree with the following statement?
    
    Norway has no moral obligation to support Ukraine in its fight against Russia.
    
    1 Strongly agree
    2 Agree
    3 Agree somewhat
    4 Neither agree nor disagree
    5 Disagree somewhat
    6 Disagree
    7 Strongly disagree"""'''


    # spørsmål med tall -> svarer 4 på nesten alt
''' question = """Hvor enig eller uenig er du i påstanden nedenfor?
 Norge har ikke en moralsk plikt til å støtte Ukraina i kampen mot Russland. 

     Her er svaralternativene - velg ett:
     1   Svært enig
     2   Enig
     3   Noe enig
     4   Verken enig eller uenig
     5   Noe uenig
     6   Uenig
     7   Svært uenig"""
 '''

'''question =  """«Hvor bekymret er du for klimaendringer?

    1 Ikke bekymret i det hele tatt
    2 Lite bekymret
    3 Noe bekymret
    4 Bekymret
    5 Svært bekymret»
    """
    '''

'''question = """Når det gjelder klimaendringer og alt du forbinder med det, hvor sterkt opplever du følgende følelser?

Apati

1 Ikke i det hele tatt
2 Lite
3 Noe
4 Sterkt
5 Svært sterkt"""'''

question = """Se på utsagnet nedenfor. I hvor stor grad er du enig eller uenig i det?

Teknologiske nyvinninger kommer til å løse klimaproblemene.

1 Svært enig
2 Enig
3 Noe enig
4 Verken enig eller uenig
5 Noe uenig
6 Uenig
7 Svært uenig"""

'''question =  """«Hvor bekymret er du for klimaendringer?

Ikke bekymret i det hele tatt
Lite bekymret
Noe bekymret
Bekymret
Svært bekymret»
"""
'''

'''question = """«Hva er de viktigste politiske sakene eller saksfeltene for deg personlig?

Vennligst list de tre viktigste sakene der 1 er den viktigste, 2 er den nest viktigste og 3 er den tredje viktigste saken.
»
"""
'''

'''question = """Hvor enig eller uenig er du i utsagnet nedenfor? 

Diskriminering mot kvinner er ikke lenger et problem i Norge.

Her er svaralternativene - velg ett:
1   Svært enig
2   Enig
3   Noe enig
4   Verken enig eller uenig
5   Noe uenig
6   Uenig
7   Svært uenig"""
'''

'''question = """Spørsmålstekst:	
Hvor enig eller uenig er du i utsagnet nedenfor?

Om en person er mann eller kvinne avhenger av om personen føler seg som mann eller kvinne.

        Her er svaralternativene - velg ett:
    1   Svært enig
    2   Enig
    3   Noe enig
    4   Verken enig eller uenig
    5   Noe uenig
    6   Uenig
    7   Svært uenig"""'''

'''question = """Se for deg en tenkt situasjon:

Du har et barn som går i barnehage. Personalet i barnehagen oppfyller de formelle kravene til utdannelse blant barnehageansatte. Barnehagen er litt langt unna hjemmet.

Hvor enig eller uenig er du i følgende påstander:

Jeg ville begrenset tiden barnet mitt var i barnehagen.

0	Helt uenig
1
2
3
4
5
6
7
8
9
10    Helt enig"""'''

'''question = """Den offentlige forvaltningen kan i framtiden bruke kunstig intelligens for å hjelpe med å ta beslutninger i enkelte saker. Formålet er å redusere kostnader og behandlingstid, og å gjøre beslutninger bedre og mer treffsikre. Et eksempel kan være å lære en datamaskin å forutsi omtrent hvor lenge en person vil være sykmeldt, basert på informasjon om sykdommen og personen. Det kan en saksbehandler da bruke for å velge passende tiltak. Andre eksempler er å bruke kunstig intelligens til å bosette flyktninger i kommuner, og til å vurdere prøveløslatelse av innsatte i fengsel.
Spørsmålstekst:	Hvor bekymret –eller ikke—er du for bruk av maskinlæring og kunstig intelligens i den offentlige forvaltningen?

1 Ikke bekymret i det hele tatt
2 Lite bekymret
3 Noe bekymret
4 Bekymret
5 Svært bekymret»"""'''

response = generate_responses(10)

# scitizen = generate_synthetic_citizen()
# print(scitizen)
# gender=get_gender(1)
# print(gender)
# exit()
#
# client = get_openai_client()
# main(client)
