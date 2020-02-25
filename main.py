import PySimpleGUI as sg
import patoolib
import zipfile
import os


def decompress(values):
    listOfZips = []
    listOfRars = []
    invalidFormatZip = ["....zip", "...zip", "..zip", "  .zip", " .zip"]

    if values != '' and event == 'Transform files to cbr':
        print("Starting decompressing...")
        os.chdir(values)  # Перейти по пути

        # Найти все .zip / .rar -> занести в список listOfZips / listOfRars
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                fileName = os.path.join(root, name)
                if fileName[len(fileName)-4:len(fileName)] == '.zip':
                    newFileName = fileName
                    for i in invalidFormatZip:
                        newFileName = newFileName.replace(i, ".zip")
                    os.rename(fileName, newFileName)
                    newFileName = newFileName[1:len(
                        newFileName)].replace("\\", "/")
                    listOfZips.append(newFileName)
                elif fileName[len(fileName)-4:len(fileName)] == '.rar':
                    newFileName = fileName.replace("....rar", ".rar")
                    os.rename(fileName, newFileName)
                    newFileName = newFileName[1:len(
                        newFileName)].replace("\\", "/")
                    listOfRars.append(newFileName)
                elif fileName[len(fileName)-4:len(fileName)] == '.cbr':
                    newFileName = fileName[0:len(fileName)-4] + '.rar'
                    newFileName = newFileName.replace("....rar", ".rar")
                    os.rename(fileName, newFileName)
                    newFileName = newFileName[1:len(
                        newFileName)].replace("\\", "/")
                    listOfZips.append(newFileName)

        print(
            "------------------------------------------------------------------------------")
        print("Starting .zip decompressing...")
        # Открыть каждый zip и разархивировать
        for i in listOfZips:
            pathToZip = values + i
            pathToFolder = pathToZip[0:len(pathToZip)-4]
            if os.path.exists(pathToFolder):
                print("! Warning directory is exist - ", i)
            elif zipfile.is_zipfile(pathToZip):
                z = zipfile.ZipFile(pathToZip, 'r')
                z.extractall(pathToFolder)
                z.close()
                os.chmod(pathToZip, 0o777)
                os.remove(pathToZip)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .zip")

        print(
            "------------------------------------------------------------------------------")
        print("Starting .rar decompressing...")
        for i in listOfRars:
            pathToRar = values + i
            pathToFolder = pathToRar[0:len(pathToRar)-4]
            if os.path.exists(pathToFolder):
                print("× Error directory for -", i, " - is exist")
            elif patoolib.get_archive_format(pathToRar)[0] == "rar":
                patoolib.extract_archive(
                    pathToRar, outdir=pathToFolder, verbosity=-1)
                os.chmod(pathToRar, 0o777)
                os.remove(pathToRar)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .rar")
        print(
            "------------------------------------------------------------------------------")
        print("Decompressing is over")
        print(
            "------------------------------------------------------------------------------")


sg.theme('SandyBeach')
layout = [[sg.Text('Print comix\\manga folder here:\n')],
          [sg.FolderBrowse(button_text='Choose', size=(10, 1)),
           sg.Input(size=(37, 1))],
          [sg.Text()],
          [sg.OK(button_text='Transform files to cbr', size=(44, 1))]]
window = sg.Window('CbrCreator', layout)

event = ''
while event != 'None':
    event, values = window.Read()
    if(not event):
        break
    decompress(values[0])
print("\"CbrCreator\" closed")
window.close()
