from datetime import datetime
from pathlib import Path

import openai
import os
from dotenv import load_dotenv
import pandas as pd
import yaml
from typing import List, cast
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam

from data_mapping.get_parameters import gender, age, county, edu, occupation

MODEL = "gpt-4o-mini"
TEMP = 0.9

def get_openai_client():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def generate_identity_prompt(demographics) -> str:
    """
    Generates a survey prompt for a specific gender and county.
    Draws on the mappings in get_parameters.py
    """

    return (f"Du er en {gender[demographics['gender']]} født i {age[demographics['age']]} og du "
            f"bor i {county[demographics['county']]}. Du har utdanning fra {edu[demographics['edu']]}, "
            f"og er yrkesmessig tilknyttet {occupation[demographics['occupation']]}. "
            "Du deltar i en spørreundersøkelse. Du skal kun svare med et tall når du far sporsmålene.")

def generate_responses(n_responses, questionnaire_keys):
    survey_data = []
    client = get_openai_client()

    # Load questions
    p = Path('../data/survey_questions.yaml')
    with p.open("r", encoding="utf-8") as f:
        questionnaire_list = yaml.safe_load(f)

    # Load synthetic citizens
    synthetic_citizens = pd.read_csv("../code/random_sample.csv")

    try:
        n_available = len(synthetic_citizens)
        n = min(n_responses, n_available)

        for i in range(n_responses):
            print(f"Iteration # {i}")
            # --- Timing & progress estimation ---
            if i == 0:
                start_time = datetime.now()

            elapsed = datetime.now() - start_time
            elapsed_seconds = elapsed.total_seconds()

            # Avoid division by zero
            avg_time = elapsed_seconds / (i + 1)

            remaining = (n - (i + 1)) * avg_time
            finish_time = datetime.now() + pd.Timedelta(seconds=remaining)

            print(f"Elapsed time: {str(elapsed).split('.')[0]} "
                  f"(~{avg_time:.1f}s per respondent)")
            print(f"Estimated remaining: ~{remaining / 60:.1f} minutes")
            print(f"Expected finish time: {finish_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)

            #should fetch from random_sample.csv instead of generating on the fly
            try:

                demographics = synthetic_citizens.iloc[i].to_dict()
                print(f"Demographics: {demographics}")  # optional for debugging

                identity_prompt = generate_identity_prompt(demographics)
                print(f"The identity_prompt is: {identity_prompt}")

                identity_msg: ChatCompletionSystemMessageParam = {
                    "role": "system",
                    "content": identity_prompt,
                }
                messages: List[ChatCompletionMessageParam] = [identity_msg]

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=TEMP,
                    max_tokens=150
                )
                assistant_content = response.choices[0].message.content or ""
                messages.append(cast(ChatCompletionAssistantMessageParam, {
                    "role": "assistant",
                    "content": assistant_content,
                }))

                q_by_id = {q["id"]: q for q in questionnaire_list}

                # Ask each requested question in sequence
                for qid in questionnaire_keys:
                    q = q_by_id.get(qid)
                    if not q:
                        print(f"Warning: question id '{qid}' not found in YAML; skipping.")
                        continue

                    user_msg: ChatCompletionUserMessageParam = {
                        "role": "user",
                        "content": q["text"],
                    }
                    messages.append(user_msg)

                    response2 = client.chat.completions.create(
                        model=MODEL,
                        messages=messages,
                        temperature=TEMP,
                        max_tokens=150,
                    )
                    answer = response2.choices[0].message.content or ""
                    print(f"Q[{qid}]: {q['text']}\nA: {answer}\n")

                    # Keep conversation context
                    messages.append(cast(ChatCompletionAssistantMessageParam, {
                        "role": "assistant",
                        "content": answer,
                    }))

                    survey_data.append({
                        "respid": demographics["respid"],
                        "question_id": qid,
                        "response": answer,
                    })
            except Exception as e:
                print(f"Error on iteration {i}: {e}")
                continue
    finally:
        if survey_data:
            df_long = pd.DataFrame(survey_data).drop_duplicates(["respid", "question_id"], keep="last")
            date_tag = datetime.now().isoformat(timespec="seconds").replace(":", "-")

            # Sanitize to be filesystem-friendly
            model_tag = MODEL.replace("/", "_").replace(":", "_")
            temp_tag = f"t{TEMP}".replace(".", "_")

            out_dir = Path("../data")
            long_path = out_dir / f"survey_results_long_{date_tag}_{model_tag}_{temp_tag}.csv"
            df_long.to_csv(long_path, index=False)
            print(f"Saved long to '{long_path}'")

            # Pivot to wide: one row per respid, columns are question keys, values are responses
            df_wide = (
                df_long.pivot_table(
                    index="respid",
                    columns="question_id",
                    values="response",
                    aggfunc="last",
                )
                .reset_index()
            )
            df_wide.columns.name = None

            # Optional: order columns by questionnaire_keys if present
            desired_cols = ["respid"] + [c for c in questionnaire_keys if c in df_wide.columns]
            df_wide = df_wide.reindex(columns=desired_cols)

            wide_path = out_dir / f"survey_results_wide_{date_tag}_{model_tag}_{temp_tag}.csv"
            df_wide.to_csv(wide_path, index=False)
            print(f"Saved wide to '{wide_path}'")

if __name__ == "__main__":

    #questionnaire = ['climate_threat', 'ukr_notsupport', 'climate_threat'] #../data/survey_results_wide_2025-12-09T07-57-38_gpt-4o-mini_t0_9.csv
    #questionnaire = ['climate_personal', 'ukr_support']
    questionnaire = ['distrikt-mer']
    #questionnaire = ['distrikt-ikke-mer']
    #questionnaire = ['valg-ikke-fri-forby']
    #questionnaire = ['valg-ikke-fri-tillate']
    generate_responses(2000, questionnaire)

