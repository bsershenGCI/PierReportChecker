"""
File: 'PierCheckerGUI[ver.2.0].py'
Purpose: Create a page that allows user input of piers and returns missing and 
duplicate piers.
Author: Ben Sershen
Date: 04/02/21
Version: 1.1 - 
    Input
        .xlsx spreadsheet file (see example: 'S:\techs\reynolds, r\2020 Field Reports\22492A-092320-Geopier Install.xlsx')
    Output
        Added a check for duplicate piers between multiple imported files
        Added input section to select file input type (Geopier-style vs VSC-style)

"""
import PySimpleGUI as sg
import pandas as pd
import warnings

# Stop warnings from appearing in output window
warnings.filterwarnings('ignore')

# Add a touch of color to window
sg.theme('DarkAmber')   

# Setting up the window GUI
sg.set_options(auto_size_buttons=True)
layout =[
    [sg.Text('This program is used to compile and sort recorded piers and check for missing and duplicate piers.')],
        [sg.Frame(layout=[
            [sg.Radio('Geopier', "RADIO1", key='_GEOPIER_', default=True, size=(10,1)), 
             sg.Radio('VSC'    , "RADIO1", key='_VSC_')]], title='Select Report Type',
                title_color='red', 
                relief=sg.RELIEF_SUNKEN, 
                tooltip='Select one before moving on')],
        [sg.Text('Pier Installation .xlsx File'), sg.Input(key="-INPUT-"),
         sg.FileBrowse(file_types=[('xlsx file', "*.xlsx")])],
        [sg.Button('Run'), sg.Button('Clear'), sg.Button('Close')],
        [sg.Button('Reset Multi-File Duplicate Check')],
        [sg.Output(size=(50,30), key = '-OUTPUT-')]]

# Create the Window
window = sg.Window('Pier Chcker v2.0', layout, default_element_size=(40, 1), grab_anywhere=False)

filePath = 'C:/Users/bsershen/Documents/11111A-010121-Geopier Install (TEST).xlsx'

DailyDupTracker = []
while True:
    event, values = window.read()
    
    # Print results when 'Run' is clicked
    if event == 'Run':
        if values['_GEOPIER_']: #"GEOPIER" radio selected
            
            filePath = values['-INPUT-']
            
            # Print the date of the report
            dfDate = pd.read_excel(filePath, sheet_name='Geopier', usecols=[14], skiprows=(1))
            dfDate = dfDate.squeeze()
            dfDate = dfDate[0]
            print(' ')
            print('-Installation Date: ' + dfDate.strftime('%b/%d/%Y'))
            
            # Create a dataframe of pier column
            df = pd.read_excel(filePath, sheet_name='Geopier', usecols=[1], skiprows=(8))
            df = df.dropna()
            dfSeries = df.squeeze()
            dfList = dfSeries.tolist()
            
            # Filter any non-numbers from pier column *REMOVED*
            '''
            def isnumber(x):
                try:
                    float(x)
                    return True
                except:
                    return False
            df[df.applymap(isnumber)]
            '''
            i = 0
            for i in range(len(dfList)):
                DailyDupTracker.append(dfList[i])
            # Python program to print duplicates from a list of integers
            def Repeat(x):
            	_size = len(x)
            	repeated = []
            	for i in range(_size):
            		k = i + 1
            		for j in range(k, _size):
            			if x[i] == x[j] and x[i] not in repeated:
            				repeated.append(x[i])
            	return repeated
            
            DailyDups = Repeat(DailyDupTracker)
            
            if len(DailyDupTracker) > len(dfList):
                if len(DailyDups) > 0:
                    print('Duplicates Found Between Files: '+ str(DailyDups))
                else:
                    print('No duplicate piers found between files')
            else:
                pass
            
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
            
            i = 0
            if len(dfDups) > 0:
                print('Duplicate piers found in file: ')
                for i in range(len(dfDups)):
                         print(int(dfDups.iloc[i]),sep=' ', end =', ', flush=True)
           
            else:
                print('No duplicate piers found')
                            
            print('')
            # Display number of unique piers
            dfUniqueList= pd.unique(dfSeries)
            dfUniquePiers = len(dfUniqueList)
            print('Total Unique Piers: ' + str(dfUniquePiers))
            
            # Estimate missing piers from range of piers
            i = 0
            dfRangeList = []
            for i in range(dfMin,dfMax):
                dfRangeList.append(i)
            
            '''
            ** Estimating daily piers with this method is inaccurate so it will be removed for now **
            dfMissing = []
            for i in range(0,dfRange-1):
                if dfSeries[i] != dfRangeList[i]:
                    dfMissing.append(i)
                else:
                    pass                    
            '''
        else:
            filePath = values['-INPUT-']
        
            # Print the date of the report
            dfDate = pd.read_excel(filePath, sheet_name='VSC', usecols=[7], skiprows=(2))
            dfDate = dfDate.squeeze()
            dfDate = dfDate[0]
            print(' ')
            print('-Installation Date: ' + dfDate.strftime('%b/%d/%Y'))
            
            # Create a dataframe of pier column
            df = pd.read_excel(filePath, sheet_name='VSC', usecols=[1], skiprows=(9))
            df = df.dropna()
            dfSeries = df.squeeze()
            dfList = dfSeries.tolist()
            
            # Filter any non-numbers from pier column *REMOVED*
            '''
            def isnumber(x):
                try:
                    float(x)
                    return True
                except:
                    return False
            df[df.applymap(isnumber)]
            '''
            i = 0
            for i in range(len(dfList)):
                DailyDupTracker.append(dfList[i])
            # Python program to print duplicates from a list of integers
            def Repeat(x):
            	_size = len(x)
            	repeated = []
            	for i in range(_size):
            		k = i + 1
            		for j in range(k, _size):
            			if x[i] == x[j] and x[i] not in repeated:
            				repeated.append(x[i])
            	return repeated
            
            DailyDups = Repeat(DailyDupTracker)
            
            if len(DailyDupTracker) > len(dfList):
                if len(DailyDups) > 0: 
                    print('Pier number(s) ' + str(DailyDups) + ' found in multiple files.' )
                else:
                    print('No duplicate piers found between files')
            else:
                pass
            
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
            
            i = 0
            if len(dfDups) > 0:
                print('Duplicate piers found: ')
                for i in range(len(dfDups)):
                         print(int(dfDups.iloc[i]))
           
            else:
                print('No duplicate piers found')
            
            # Display number of unique piers
            dfUniqueList= pd.unique(dfSeries)
            dfUniquePiers = len(dfUniqueList)
            print('Total Unique Piers: ' + str(dfUniquePiers))
            
            # Estimate missing piers from range of piers
            i = 0
            dfRangeList = []
            for i in range(dfMin,dfMax):
                dfRangeList.append(i)
    elif event == 'Clear':
        window.Element('-INPUT-').Update(values['-INPUT-'], )
        window.Element('-OUTPUT-')('')
    
    elif event == 'Reset Multi-File Duplicate Check':
        DailyDupTracker = []
    
    elif event in (sg.WIN_CLOSED, 'Close'):
        window.close()
        break
window.Close()