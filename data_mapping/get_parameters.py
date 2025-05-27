# get_parameters.py
# defines the numeric and text values for the Norwegian Citizen Panel variables used in the
# Synthetic Citizen project
# May, 2025
# gender, age, county, age (decades), occupation

gender = {
    1: "mann",
    2: "kvinne"
}

def get_gender(code):
    """convert the code to the label"""
    return gender[code]

# prompt: "du er født i ..."
age = {1: "1945",
       2: "1955",
       3: "1965",
       4: "1975",
       5: "1985",
       6: "1995",
       7: "2005"
}

'''
Verdi 	Merkelapp 	Enheter 	Prosent 	
1 	1949 eller tidligere 	1654 	15.6% 	
2 	1950-1959 	2666 	25.1% 	
3 	1960-1969 	2418 	22.8% 	
4 	1970-1979 	1629 	15.3% 	
5 	1980-1989 	1051 	9.9% 	
6 	1990-1999 	711 	6.7% 	
7 	2000 eller senere 	488 	4.6% 	
'''

def get_age(code):
    """convert the code to the label"""
    return age[code]


