from lib2to3.pytree import convert
import os
import sys
import subprocess
import PySimpleGUI as sg

#variables
window = ''
values = ''

lb_inputValues = []
lb_parameterValues = []
paramsList = []

longBoxSize = 150




#---Functions---#
def compileString():
    cmdString = 'pandoc '
    
    cmdString += '-o ' + values['-OUTPUT_FOLDER-'] + '/' + values['-OUTPUT-'] + ' '
    
    if (lb_inputValues != ''):
        for i in range(len(lb_inputValues)):
            cmdString += lb_inputValues[i] + ' '
    
    selectedList = window['-LB_PARAMS-'].get()
    selectedParams = selectedList

    if (selectedParams != ''):
        for i in range(len(selectedParams)):
            cmdString += selectedParams[i] + ' '
            
    cmdString += ' ' + values['-ADDITIONALPARAMS-']
    
    return cmdString


def readParams():
    global paramsList
    paramsFile = open("params.txt", "r")
    paramsConfig = paramsFile.read()
    paramsFile.close()
    paramsList = paramsConfig.split("\n")  #.replace('\n', ' ')
    window['-LB_PARAMS-'].update(paramsList)
    
    
def writeParams():
    global paramsList
    paramsFile = open("params.txt", "w")
    for items in paramsList:
        paramsFile.writelines(items+'\n')
    paramsFile.close()










#---Main---#

sg.theme('DarkAmber')   # Add a touch of color

# All the stuff inside your window.
layout = [            
            [sg.Text("Choose your files:")],
            [sg.Text(' Input'), sg.InputText(key="-INPUT-" ,change_submits=True), sg.FileBrowse(key="-IN-"), sg.Button('Add File')],          
            [sg.Listbox(key='-LB_INPUT-', values=lb_inputValues, size=(longBoxSize,15), change_submits=True)], #select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            [sg.Button("Move Up"), sg.Button("Move Down")],
            [sg.Button('Remove File')],
            
            [sg.Text('Output'), sg.InputText(key="-OUTPUT-", change_submits=True, size=(25,1)), sg.InputText(key="-OUTPUT_FOLDER-",change_submits=True), sg.FolderBrowse()],
            
            
            [sg.Text("Choose your parameters:")],
            [sg.Listbox(key='-LB_PARAMS-', values=paramsList, size=(25,15), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, change_submits=True), [sg.InputText(key='-NEW_PARAM-'), sg.Button('Add New Parameter', key='-ADD_NEW_PARAM-')],],
            [sg.Button('Remove Param'), sg.Text('*only remove one param at a time')],
            
            [sg.Text("Additional Parameters"), sg.InputText(key='-ADDITIONALPARAMS-', change_submits=True, size=(50,1))],
            
            [sg.Text("Final Command String:")],
            [sg.InputText(key='-FinalString-', change_submits=True, size=(longBoxSize,1))],
            [sg.Button('Convert')],
            
        ]



# Create the Window
window = sg.Window('Pandoc Interface', layout)

paramsReadBool = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    window.refresh()
    event, values = window.read(timeout=1000)
    
    paramsList = list(filter(None, paramsList))
    
    if (paramsReadBool == False):
        readParams()
        paramsReadBool = True
        
    if event=='Add File':
        lb_inputValues.append(values['-INPUT-'])
        print(values['-INPUT-'])
        window["-LB_INPUT-"].update(lb_inputValues)    
        
    if event=='Remove File':
        remove_list = window['-LB_INPUT-'].get()
        filterItem = remove_list[0]
        lb_inputValues.remove(filterItem)
        window["-LB_INPUT-"].update(lb_inputValues)    
        
        
    if event=='-ADD_NEW_PARAM-':
        paramsList.append(values['-NEW_PARAM-'])
        writeParams()
        readParams()
    
    if event=='Remove Param':
        remove_list = window['-LB_PARAMS-'].get()
        filterItem = remove_list[0]
        paramsList.remove(filterItem)
        window['-LB_PARAMS-'].update(paramsList)
        writeParams
          
    #continually update
    FinalString = compileString()
    window['-FinalString-'].update(FinalString)
    
    if event== 'Convert':
        os.system(FinalString)
    
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
window.close()    
    
    










