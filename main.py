'''

This script serves as the holder of the streamlit webpage. All the main functions that deal with the documentation and such, will be held in another scripts

'''


import streamlit as st
import streamlit_toggle as tog
from functions import *
import numpy as np
st.set_page_config(layout="wide")

"""
# Wind report
"""


stDict = {}


st.divider()

coly, colx = st.columns(2)

with colx:

    uploadedFiles = st.file_uploader("Drag here the wind calculation file (.txt or .pdf), the excel file of the turbine model (.xlsx or .csv) and the pictures of the wind resource and turbulence heatmaps (.png). Make sure the heatmaps have a visible legend.", accept_multiple_files = True)
    
    flagDict = False


with coly:

    st.caption("Example files")
    with open("resources\Wind report files.zip", "rb") as fp:
        btn = st.download_button(
            label="Download example files",
            data=fp,
            file_name="Wind report files.zip",
            mime="application/zip"
        )



for uploadedFile in uploadedFiles:


    if uploadedFile.name.endswith('txt'):

        stDict['softwareWind'] = 'Furow'

        dict, df = textreaderFurow(uploadedFile)

        stDict.update(dict)

        # dictMaker(stDict, stDict['softwareWind'], df)

        st.text(stDict)

        
        flagDict = False

    elif uploadedFile.name.endswith('xlsx'):

        xls = pd.ExcelFile(uploadedFile)

        df_power = pd.read_excel(xls, 'Sheet3')
        df_thrust = pd.read_excel(xls, 'Sheet4')




st.divider()
'''
## People
'''
colp1, colp2, colp3 = st.columns(3)

with colp1:
    user = st.text_input("Name of the writer")


with colp2:
    stDict['TOMname'] = st.text_input("Technical Office Manager")

with colp3:
    stDict['pdName'] = st.text_input("Project Developer")

if user: 
    stDict['elaboratedDoc'] = initials(user)

    
st.divider()
'''
## Project
'''
df_countries = countryValues()

stDict['nameWF'] = st.text_input("Name of the project")
stDict['ISOvalue'] = st.text_input("System Operator")
country = st.selectbox('Select country', df_countries['Country'], index = None)

countryFlag = True
territorial2Flag = True

if country:

    try:
        dir = f'resources/Countries/{country}.csv'
        ms_reader(dir)
        countryFlag = False

        colpr1, colpr2, colpr3 = st.columns(3)


        with colpr1:
            stDict['territorial1Key'] = df_countries.loc[df_countries['Country']==country,'territorial1Key'].unique()[0]
            df_country = ms_reader(dir)
            territorial1 = df_country['territorial1Key'].sort_values().unique()
            stDict['territorial1'] = st.selectbox(stDict['territorial1Key'], territorial1, disabled = countryFlag, index = None)

        with colpr2:
            stDict['territorial2Key'] = df_countries.loc[df_countries['Country']==country,'territorial2Key'].unique()[0]
            territorial2Flag = False
            territorial2 =  df_country.loc[df_country['territorial1Key']==stDict['territorial1'],'territorial2Key'].sort_values().unique()
            stDict['territorial2'] = st.selectbox(stDict['territorial2Key'], territorial2, disabled = territorial2Flag, index = None)

        with colpr3:
            stDict['territorial3Key'] = df_countries.loc[df_countries['Country']==country, 'territorial3Key'].unique()[0]
            territorial2Flag = False
            territorial3 =  df_country.loc[df_country['territorial2Key']==stDict['territorial2'],'territorial3Key'].sort_values().unique()
            stDict['territorial3'] = st.selectbox(stDict['territorial3Key'], territorial3, disabled = territorial2Flag, index = None)

        flag_bash = False


    except Exception as e:
        st.markdown('The selected country has no database yet.')



stDict['numYears'] = st.selectbox('Years of the historical data', range(1,15), index = None)

if flagDict:

    dictMaker(stDict, stDict['softwareWind'], df)


pass






    
    










#flagDone es lo que indica que ya se ha hecho todo el tx pero falta pasar todo al word

# if flagDone:

#     stDict['versionDoc'] = st.text_input("Documment version")
#     stDict['tableComments'] = st.text_input("Document comments (can be left blank)")
#     stDict['modelWind'] = st.selectbox('Database of the wind model', ('MERRA-2', 'ERA-5', 'EMD Global Wind Data'))



