'''

This script serves as the holder of the streamlit webpage. All the main functions that deal with the documentation and such, will be held in another scripts

'''


import streamlit as st
import streamlit_toggle as tog
from functions import *
import numpy as np
import matplotlib.pyplot as plt
import io
from docx import Document
import os
from PIL import Image

class pict:
    def __init__(self, name, file):
        self.name = name
        self.file = file

st.set_page_config(layout="wide")

if 'finalCheck' not in st.session_state:
    st.session_state['finalCheck'] = None
    st.session_state['generarDocumento'] = None
    st.session_state['picsDone'] = None
    st.session_state['tablesDone'] = None
    st.session_state['wordsDone'] = None
    st.session_state['documentDone'] = None

"""
# Wind report
"""

stDict = {}


st.divider()

coly, colx = st.columns(2)

with colx:

    st.markdown(
    """
    Upload the following documents:
    - Wind calculation file (.txt)
    - Excel file of the turbine model (.xlsx)
    - Figure of the wind farm location (.png) (name it location)
    - Figure of the wind farm layout (.png) (name it layout)
    - Figures of wind resource  (name it wind resource) (.png) *, **
    - Figures of turbulence heatmap (name it turbulence) (.png) *, **
    
    ###### * Make sure the legend is visible. Download the example zip file to get an idea.
    ###### ** Name of the files is not case sensitive, as long as it is named as indicated.
    """
    )
    
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


picDict = {}

for uploadedFile in uploadedFiles:

    if uploadedFile.name.endswith('txt'):

        stDict['softwareWind'] = 'Furow'

        dict, df = textreaderFurow(uploadedFile)

        stDict.update(dict)
        
        flagDict = True

    elif uploadedFile.name.endswith('xlsx'):

        df_power, df_thrust = model_reader(uploadedFile)

        fig, ax = plt.subplots()
        ax.plot(df_power['Wind Speed'], df_power['1.225'])
        ax.set_xlabel('Wind Speed (m/s)')
        ax.set_ylabel('Power (kW) @ air 1.225 kg/m3')
        ax.set_title('Power curve')

        fig_io = io.BytesIO()
        fig.savefig(fig_io, format = 'png')
        fig_io.seek(0)

        picDict[pict('powerCurvePic', fig_io).name] = pict(uploadedFile.name, fig_io).file
        
        # In case we want to show the turbine
        # st.image(fig_io)

        # st.pyplot(fig)

    elif uploadedFile.name.endswith('png'):

        if 'layout' in uploadedFile.name.lower():
            layoutPic = uploadedFile
            picDict[pict('layout', layoutPic).name] = pict('layout', layoutPic).file
        
        elif 'location' in uploadedFile.name.lower():
            locationPic = uploadedFile
            picDict[pict('location', locationPic).name] = pict('location', locationPic).file

        elif 'wind resource' in uploadedFile.name.lower():
            wrPic = uploadedFile
            picDict[pict('wind resource', wrPic).name] = pict('wind resource', wrPic).file

        elif 'turbulence' in uploadedFile.name.lower():
            turbulencePic = uploadedFile
            picDict[pict('turbulence', turbulencePic).name] = pict('turbulence', turbulencePic).file

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

    except Exception as e:
        st.markdown('The selected country has no database yet.')

flagDone = False

stDict['numYears'] = st.selectbox('Years of the historical data', range(1,15))

if flagDict:

    flagDone = dictMaker(stDict, stDict['softwareWind'], df)


#flagDone es lo que indica que ya se ha hecho todo el tx pero falta pasar todo al word

if flagDone:

    st.divider()

    stDict['versionDoc'] = st.text_input("Document version")
    stDict['tableComments'] = st.text_input("Document comments (can be left blank)")
    stDict['modelWind'] = st.selectbox('Database of the wind model', ('MERRA-2', 'ERA-5', 'EMD Global Wind Data'), index = None, key = 'finalCheck')



if st.session_state.finalCheck is not None:

    st.button("Generar documento", key = 'generarDocumento')
    doc_file = duplicateDoc()


if st.session_state.generarDocumento:

    with st.spinner('Preparing document'):

        # First, we insert pictures

        insert_image_in_cell(doc_file, picDict)
        docWriter(doc_file, stDict)
        doc_modelo_bio = io.BytesIO()
        doc_file.save(doc_modelo_bio)
        doc_modelo_bio.seek(0)
        st.session_state.documentDone = True
        pass

if st.session_state.documentDone:
        
    btn = st.download_button(
            label="Descarga archivos",
            data=doc_modelo_bio,
            file_name="hola.docx",
            mime="application/zip"
        )
        



