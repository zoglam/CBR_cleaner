import PySimpleGUI as sg
import decompress as dc

sg.theme('DarkBrown1')

ok_button = 'Transform files to cbr'
app_name = 'CbrCreator'


layout = [
    [
        sg.Text('Print comix\\manga folder here:')
    ],
    [
        sg.FolderBrowse(button_text='Choose', size=(27, 1)),        
        sg.Input(size=(58, 1)) 
    ],
    [        
        sg.OK(button_text=ok_button, size=(27, 2)),
        sg.Frame(layout=
        [
            [
                sg.Checkbox('Look for .zip', size=(10,1), default=True, key='zip'),  
                sg.Checkbox('Look for .rar', size=(10,1), default=True, key='rar'),  
                sg.Checkbox('Remove trash folders', size=(15,1), default=True,key='trashFolders')
            ],      
        ], title=' Options ',title_color='#FDCB52', border_width=2)
    ],   
    [
        sg.ProgressBar(1000, orientation='h', size=(49, 20), border_width=1,
            key='progbar', bar_color=('green', '#2C2825'))
    ],
    [
        sg.Text('0 %', justification='center', size=(79, 1), key='percent_progress')
    ],
]

window = sg.Window(app_name, layout)

while True:
    try:
        event, values = window.Read()
        progressBarValue = 0
        window['progbar'].update_bar(0)
        if(not event):
            window.close()
            break
        sg.Print("Starting decompressing...", text_color=dc.colorForPrint("black"))

        listOfZips, listOfRars, progressBarPerStep = dc.findArchives(values, event, ok_button)

        if values['zip']:
            if len(listOfZips) == 0:
                sg.Print("! Warning - Nothing to decompress .zip", text_color=dc.colorForPrint("yellow"))
            else:
                sg.Print("Starting .zip decompressing...", text_color=dc.colorForPrint("black"))
                progressBarValue = dc.decompressZip(listOfZips, values, window, 
                    progressBarValue, progressBarPerStep)

        if values['rar']:
            if len(listOfRars) == 0:
                sg.Print("! Warning - Nothing to decompress .rar", text_color=dc.colorForPrint("yellow"))
            else:
                sg.Print("\nStarting .rar decompressing...", text_color=dc.colorForPrint("black"))
                dc.decompressRar(listOfRars, values, window, progressBarValue, progressBarPerStep)
        
        window['progbar'].update_bar(1000)
        window['percent_progress'].update('100 %')
        sg.Print(50 * "-", text_color=dc.colorForPrint("black"))
        sg.Print("Decompressing is over", 5*"\n", text_color=dc.colorForPrint("black"))
    except Exception as e:
        sg.Print("× Error in main cycle -", e, text_color=dc.colorForPrint("red"))
        continue