# generate10k.py
# produces a data set of 10,000 synthetic citizens
# with randomly drawn demographic characteristics (age, gender, region, education, work sector)
# These variables are independently drawn from each other. Consider at some point to prime the draws to make them more realistic.

import numpy as np
import pandas as pd
from get_parameters.py import gender, edu, age, region, occupation


# Set the number of observations
num_observations = 10000

# Define the lists of parameters
edu = {
    1: "grunnskole",
    2: "videregående skole",
    3: "høgskole/universitet"
}

# Convert the dictionary keys to a list for sampling
edu_keys = list(edu.keys())

# Generate random data for the variables
# For example, let's say we have three variables:
# 1. Age - Random integers between 18 and 70
# 2. Income - Random floats between 20,000 and 100,000
# 3. Education - Random choice from the 'edu' dictionary

age = np.random.randint(18, 71, num_observations)
income = np.random.uniform(20000, 100000, num_observations)
education = np.random.choice(edu_keys, num_observations)

# Map the random choices to their corresponding educational levels
education = [edu[key] for key in education]

# Put the data into a DataFrame for better readability and usability
data = pd.DataFrame({
    'Age': age,
    'Income': income,
    'Education': education
})

# Display the first few rows of the dataset
print(data.head())

# Optionally, you can save the data to a CSV file
data.to_csv('random_sample.csv', index=False)
