import random

from data_mapping.get_gender import get_gender #change to get_parameters when that file is created

gender = {
    1: "mann",
    2: "kvinne"
}

age = {1: "1945",
       2: "1955",
       3: "1965",
       4: "1975",
       5: "1985",
       6: "1995",
       7: "2005"
}

def create_random_citizen():
    gender_key = random.choice(list(gender.keys()))
    age_key = random.choice(list(age.keys()))
    print(f"Du er en {gender[gender_key]} født i {age[age_key]}")

if __name__ == "__main__":
    create_random_citizen()
