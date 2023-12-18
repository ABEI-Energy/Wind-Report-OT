'''

This script contains the functions to be called from streamlit.py

'''
import pandas as pd
import locale as lc
import datetime as dt
import streamlit as st
import requests
import utm


lc.setlocale(lc.LC_ALL,'es_ES.UTF-8')

month = dt.datetime.now().strftime("%B %Y")
year = month.split(' ')[-1]

@st.cache_data
def textreaderFurow(file):

    dictFurow = dict()

    lines = file.getvalue().decode('ANSI').split('\r\n')

    lines = [line.strip().split('\t') for line in lines]

    # Get key values
    for i, row in enumerate(lines):
        if len(row)==2:
            dictFurow[row[0]] = row[1]

    # Get table 
    w1 = "General characteristics"
    for i, row in enumerate(lines):
        if w1 in row:
            i += 1
            break
    lines = lines[i:]
    df = pd.DataFrame(columns = lines[0])
    lines = lines[1:]
    for i, row in enumerate(lines):
        if len(row)!=1:
            df.loc[len(df)] = row
    
    df['Wake losses (%)'] = 100 - df['Array Efficiency [%]'].apply(float)

    # Añadimos coordenadas de 

    dictFurow['wakeLoss'] = df['Array Efficiency [%]'].apply(float).mean()

    # Calculamos el centroide del parque
    dictFurow['latUTMProj'] = df['Y [m]'].apply(float).sum()/df['Y [m]'].count()
    dictFurow['longUTMProj'] = df['X [m]'].apply(float).sum()/df['X [m]'].count()    

    return dictFurow, df

@st.cache_data
def dictMaker(dict, program, df):

    dict['dateTime'] = month
    dict['currentYear'] = year
    dict['yearMinus'] = str(float(year) - float(dict['numYears']))
    dict['dateTable'] = dt.datetime.now().strftime("%d/%m/%y")
    
    
    if program == 'Furow':
    
        dict['equivalentHours'] = dict.pop('Net Full load hours [h]')
        dict['husoUTM'] = dict.pop('UTM Zone')
        dict['powerWF'] = dict.pop('Total Capacity Installed [MW]')
        dict['capacityFactor'] = dict.pop('Net Capacity Factor [%]')
        dict['anualProd'] = dict.pop('Net Yield [MWh]')
        dict['anualProdGross'] = dict.pop('Ideal Yield [MWh]')
        dict['numTurbines'] = dict.pop('Number of turbines')
        dict['wakeSpeed'] = dict.pop('Mean Wake Affected Wind Speed [m/s]')
        dict['windSpeed'] = dict.pop('Mean Free Wind Speed [m/s]')
        dict['turbineModel'] = df['Turbine Type'].unique()[0]
        dict['hubHeight'] = df['Hub Height [m]'].unique()[0]
        dict['rotorSize'] = df['Rotor Diameter [m]'].unique()[0]
        dict['turbinePower'] = df['Capacity [kW]'].unique()[0]

        utm_to_latLon(dict)

        get_elevation(dict)



    else:
        pass
    
@st.cache_data
def initials(user):
    user = user.strip().split(' ')
    auxUser = []
    for word in user:
        auxUser.append([*word][0])
    user = '.'.join(auxUser)
    return user

@st.cache_data
def normalize(string):
    return str(string.replace(",", "."))

@st.cache_data
def get_elevation(dict):

    lat = dict['latProj']
    lon = dict['longProj']
    url = ('https://api.opentopodata.org/v1/test-dataset'f'?locations={lat},{lon}')
    while True:
        try:
           response = requests.get(url).json()
        except Exception as e:
           continue
        break
   
    elevation = response['results'][0]['elevation']

    dict['altProj'] = elevation

@st.cache_data
def utm_to_latLon(dict):
    lat_utm = float(dict['latUTMProj'])
    long_utm = float(dict['longUTMProj'])
    huso = int(dict['husoUTM'].split(' ')[0])
    zone = dict['husoUTM'].split(' ')[-1].strip()
    coordinates = utm.to_latlon(long_utm, lat_utm, huso, zone)
    dict['latProj'] = coordinates[0]
    dict['longProj'] = coordinates[-1]
    dict.update(dict)

@st.cache_data
def countryValues():
    df_countries = pd.read_csv('countries.csv', index_col=None).sort_values(by='Country')
    return df_countries

@st.cache_data
def ms_reader(directory):
    
    if 'csv' in directory:
        df = pd.read_csv(directory, index_col=None)

    elif 'xlsx' in directory:
        pass

    return df





