import PySimpleGUI as sg
import decompress as dc


sg.theme('SandyBeach')

ok_button = 'Transform files to cbr'
app_name = 'CbrCreator'

layout = [      
    [
        sg.Text('Print comix\\manga folder here:\n')
    ],
    [
        sg.FolderBrowse(button_text='Choose', size=(20, 1)),
        sg.Input(size=(83, 1))
    ],
    [        
        sg.OK(button_text=ok_button, size=(27, 2)),
        sg.Frame(layout=
        [      
            [
                sg.Checkbox('Look for .zip', size=(17,1), default=True, key='zip'),  
                sg.Checkbox('Look for .rar', size=(16,1), key='rar'),  
                sg.Checkbox('Remove trash folders', size=(16,1), key='folders')
            ],      
        ], title=' Options ',title_color='#000', border_width=6)
    ], 
    [
        sg.Frame(layout=
        [    
            [
                sg.Output(size=(100, 20))
            ]
        ], title=' Output ',title_color='#000', border_width=5)
    ],    
    [
        sg.ProgressBar(1000, orientation='h', size=(58, 20),
            key='progbar', bar_color=('green', '#EFECCB'))
    ],
    [
        sg.Text('0 %', justification='center', size=(94, 1), key='percent_progress')
    ],
]

window = sg.Window(app_name, layout)

while True:
    try:
        event, values = window.Read() 

        progressBarValue = 0
        window['progbar'].update_bar(0)
        if(not event):
            print("\"",app_name,"\" closed")
            window.close()
            break
        print("Starting decompressing...")

        listOfZips, listOfRars, progressBarPerStep = dc.findArchives(values, event, ok_button)

        if values['zip']:
            print("\nStarting .zip decompressing...")
            progressBarValue = dc.decompressZip(listOfZips, values, window, progressBarValue, progressBarPerStep)

        if values['rar']:
            print("\nStarting .rar decompressing...")
            dc.decompressRar(listOfRars, values, window, progressBarValue, progressBarPerStep)
        
        window['progbar'].update_bar(1000)
        window['percent_progress'].update('100 %')
        print("--------------------------------------------------")
        print("Decompressing is over", 5*"\n")
    except Exception as e:
        print("× Error -", e)
        continue