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

# County
# not needed: countyrange = {}
county = {
    3  :  "Oslo",
    11 :  "Rogaland",
    15 :  "Møre og Romsdal",
    18 :  "Nordland",
    31 :  "Østfold",
    32 :  "Akershus",
    33 :  "Buskerud",
    34 :  "Innlandet",
    39 :  "Vestfold",
    40 :  "Telemark",
    42 :  "Agder",
    46 :  "Vestland",
    50 :  "Trøndelag",
    55 :  "Troms",
    56 :  "Finnmark"
    }

'''
(from Norwegian Citizen Panel codebook:)
Verdi 	Merkelapp 	Enheter 	Prosent 	
3 	Oslo 	1659 	15.6% 	
11 	Rogaland 	1027 	9.7% 	
15 	Møre og Romsdal 	410 	3.9% 	
18 	Nordland 	392 	3.7% 	
31 	Østfold 	465 	4.4% 	
32 	Akershus 	1526 	14.4% 	
33 	Buskerud 	454 	4.3% 	
34 	Innlandet 	576 	5.4% 	
39 	Vestfold 	526 	5.0% 	
40 	Telemark 	275 	2.6% 	
42 	Agder 	532 	5.0% 	
46 	Vestland 	1482 	14.0% 	
50 	Trøndelag 	885 	8.3% 	
55 	Troms 	302 	2.8% 	
56 	Finnmark 	106 	1.0% 	
'''

def get_county(code):
    """convert the code to the label"""
    return county[code]

