
"""
File: PierCheckerGUI[ver.1.0]
Purpose: Create a page that allows user input of piers and returns missing and 
duplicate piers.
Author: Ben Sershen
Date: 04/08/21
Version: 1.1 - 
    Input
        .xlsx spreadsheet file (see example: 'S:\techs\reynolds, r\2020 Field Reports\22492A-092320-Geopier Install.xlsx')
    Output
        Output overall unique, duplicate, missing piers
        Output Daily unique, duplicate, missing piers
    
"""
import PySimpleGUI as sg
import pandas as pd
import warnings

# Hide warnings from appearing in output window
warnings.filterwarnings('ignore')

# Add a touch of color to window
sg.theme('DarkAmber')   

# Setting up the window gui
sg.set_options(auto_size_buttons=True)
layout = [
    [sg.Text('This program is used to compile and sort recorded piers and check for missing and duplicate piers.')],  
    [sg.Text('Pier Installation .xlsx File'), sg.Input(key="-INPUT-"),
     sg.FileBrowse(file_types=[('xlsx file', "*.xlsx")])],
    [sg.Button('Run'), sg.Button('Clear'), sg.Button('Close')],
    [sg.Output(size=(50,30), key = '-OUTPUT-')]]

# Create the Window
window = sg.Window('Pier Chcker v1.1', layout, default_element_size=(40, 1), grab_anywhere=False).Finalize()

#filePath = 'C:/Users/bsershen/Documents/11111A-010121-Geopier Install (TEST).xlsx'

# Event Loop to process "events" and get the "values" of the inputs   
while True:
    event, values = window.read()
       
    # Print results when 'Run' is clicked
    if event == 'Run':
            
            filePath = values['-INPUT-']
            
            # Print the date of the report
            dfDate = pd.read_excel(filePath, sheet_name ='VSC', usecols=[14], skiprows=(1))
            dfDate = dfDate.squeeze()
            dfDate = dfDate[0]
            print(' ')
            print('-Installation Date: ' + dfDate.strftime('%b/%d/%Y'))
        
            # Create a dataframe of pier column
            df = pd.read_excel(filePath, sheet_name='VSC', usecols=[1], skiprows=(9))
            df = df.dropna()
            dfSeries = df.squeeze()         
            
            # Minimum number pier
            dfMin = df.min()
            dfMin = int(dfMin[0])
            
            # Maximum number pier
            dfMax = df.max()
            dfMax = int(dfMax[0])
            
            # Range of piers
            dfRange = dfMax-dfMin
            print('Pier installation ranged from pier ' + str(int(dfMin+0.5)) + 
                  ' to ' + str(int(dfMax+0.5)))
            
            # Finding duplicates
            dfDups = df[df.duplicated(keep=False)]
            dfDups = dfDups.squeeze()
            dfUniqueDups = pd.unique(dfDups)
            dfUniqueDups = pd.Series(dfUniqueDups)
            
            if len(dfDups) > 0:
                print('Duplicate piers found: ')
                for i in range(len(dfUniqueDups)):
                         print(int(dfUniqueDups.iloc[i]), end=(' '), flush=True)
                print(' ')
           
            else:
                print('No duplicate piers found')
                
            # Display number of unique piers
            dfUniqueList= pd.unique(dfSeries)
            dfUniquePiers = len(dfUniqueList)
            print('Total Unique Piers: ' + str(dfUniquePiers))
            
            # Estimate missing piers from range of piers
            dfRangeList = []
            for i in range(dfMin,dfMax):
                dfRangeList.append(i)      

    elif event == 'Clear':
        window.Element('-INPUT-').Update(values['-INPUT-'], )
        window.Element('-OUTPUT-')('')

    elif event in (sg.WIN_CLOSED, 'Close'):
        window.close()
        break

window.close()     