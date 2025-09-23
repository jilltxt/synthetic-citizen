# get_parameters.py
# defines the numeric and text values for the Norwegian Citizen Panel variables used in the
# Synthetic Citizen project
# May, 2025
# gender, age, county, age (decades), occupation

# Gender, based on NCP variable P1
gender = {
    1: "mann",
    2: "kvinne"
}

# def get_gender(code):
#     """convert the code to the label"""
#     return gender[code]

# Region, based on NCP variable P2 (landsdel)
# Suggested prompt: "Du bor ..."
region = {
    1 : "i Oslo",
    2 : "på Østlandet",
    3 : "på Sørlandet",
    4 : "på Vestlandet",
    5 : "i Trøndelag",
    6 : "i Nord-Norge"
    }


# Age (decade). Suggested prompt: "du er født i ..."
age = {1: "1945",
       2: "1955",
       3: "1965",
       4: "1975",
       5: "1985",
       6: "1995",
       7: "2005"
}

# occupation. Suggested prompt: "Yrkesmessig er du tilknyttet ..."
# Based on NCP variables [c29_bgind_1 ... c29_bgind_20]
occupation = {1 : "offentlig sentralforvaltning/myndighet",
              2 : "barnehage/skole/undervisning",
              3 : "helsetjenester",
              4 : "sosialtjenester/barnevern",
              5 : "pleie- og omsorgstjenester",
              6 : "forsvar/politi/rettsvesen/vakthold",
              7 : "landbruk/skogbruk/fiske",
              8 : "industri/teknikk",
              9 : "bygg/anlegg",
              10: "varehandel/butikk",
              11: "transport/samferdsel",
              12: "kultur/idrett/organisasjoner",
              13: "media/reklame/PR/informasjon",
              14: "forskning/analyse",
              15: "reiseliv/hotell",
              16: "restaurant/servering",
              17: "telekommunikasjon/IT",
              18: "bank/forsikring/finans",
              19: "forretningsmessig service-/tjenesteyting",
              20: "olje/gass"}

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

''' Note:  r33_Weight4
Variabeletikett: 	Vekt basert på variablene P1, P2, P4_1 
(Merk! todelt utdanning: 1) vgs og lavere, og 2) universitet og høyskole) og alder. 
'''

# Education
# Based on Norwegian Citizen Panel variable c33_bgedu3
# Suggested prompt: "Du har utdanning fra ..."
edu = {
    1 : "grunnskole",
    2 : "videregående skole",
    3 : "høgskole/universitet"
    }

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

# Weight-relevant variables: based on r33_Weight4
# Variabeletikett: 	Vekt basert på variablene P1 (kjønn), P2 (Landsdel), P4_1 ()