
"""
Purpose: Create a page that allows user input of piers and returns missing and 
duplicate piers.
Author: Ben Sershen
Date: 10/15/20
Version: 0.3 - Added working 'Clear' button.
"""
20, 1, 5, 10
import PySimpleGUI as sg
import collections
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('This page is used to compile and sort recorded piers and check for missing and duplicate piers.')],
            [sg.Text('Enter piers:'), sg.MLine('',key=('-INPUT-'))],
            [sg.Button('Run'), sg.Button('Clear')],
            [sg.Output(size=(50,30), key = '-OUTPUT-')] ]

# Create the Window
window = sg.Window('Pier Chcker v0.4', layout, default_element_size=(40, 1), grab_anywhere=False)

# Event Loop to process "events" and get the "values" of the inputs   
while True:
    event, values = window.read()
    #Item input and manipulation
    listTotal = values['-INPUT-']
    listTotal = tuple(map(int, listTotal.split(', ')))
    
    #sortedTotal is a tuple of listTotal sorted by ascending order.
    sortedTotal = sorted(listTotal)
    #print(sortedTotal)
    
    listMin = sortedTotal
    print(' ')
    print('Pier installation ranged from pier ' + str(sortedTotal[0]) + 
                  ' to ' + str(sortedTotal[-1]))
            
    
    # find_missing function to check for missing piers *REMOVED*
    
    def find_missing(lst): 
        return [i for x, y in zip(lst, lst[1:])  
            for i in range(x + 1, y) if y - x > 1] 
    ''' *REMOVED*
    if len(find_missing(sortedTotal)) > 0:
        missingPiers= 'Missing piers: ' + str(find_missing(sortedTotal))
        
    else:
        missingPiers = str("No missing piers found")
    '''
    #Converts the total sorted piers into a set of unique items (removes duplicates).
    setTotal = set(listTotal)
    uniquePiers = str(len(setTotal))
    totalNum = str(len(listTotal))

    contains_duplicates = len(listTotal) != len(setTotal)

    #Prints any duplicate piers if previous statement is true.
    if contains_duplicates == True:
        dupPiers = 'Duplicate Piers: ' + str([item for item,
                        count in collections.Counter(sortedTotal).items() if count > 1])

    else:
        dupPiers = str("No duplicates piers found")

    
    # Print results when 'Ok' is clicked
    if event == 'Run':
        find_missing(listTotal)
        print('Total unique piers: ' + uniquePiers)
        print(dupPiers)    
        print('Total recorded piers: ' + totalNum)
        
    # Clear output and reset elements when 'Clear' is clicked.
    elif event == 'Clear':
        window.Element('-INPUT-').Update(values['-INPUT-'], )
        window.Element('-OUTPUT-')('')

    '''
    elif event in (sg.WIN_CLOSED, 'Close'):
        window.close()
        break
    '''
        
window.close()