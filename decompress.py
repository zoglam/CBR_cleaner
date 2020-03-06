import PySimpleGUI as sg
import patoolib
import zipfile
import os


def findArchives(values, event, ok_button):
    listOfZips = []
    listOfRars = []
    invalidFormatZip = ["....zip", "...zip", "..zip", "  .zip", " .zip"]
    invalidFormatRar = ["....rar", "...rar", "..rar", "  .rar", " .rar"]

    if values['Choose'] != '' and event == ok_button:
        os.chdir(values['Choose'])  # Перейти по пути

        # Найти все .zip / .rar -> занести в список listOfZips / listOfRars
        for root, _, files in os.walk(".", topdown=False):
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
                    newFileName = fileName
                    for i in invalidFormatRar:
                        newFileName = newFileName.replace(i, ".rar")
                    os.rename(fileName, newFileName)
                    newFileName = newFileName[1:len(
                        newFileName)].replace("\\", "/")
                    listOfRars.append(newFileName)

    if values['zip'] and values['rar']:        
        progressBarPerStep = 1000 / ( len(listOfZips) + len(listOfRars) + 0.01)
    elif values['zip']:
        progressBarPerStep = 1000 / ( len(listOfZips) + 0.01)
    elif values['rar']:
        progressBarPerStep = 1000 / ( len(listOfRars)  + 0.01)
    else:
        progressBarPerStep = 1000

    return listOfZips, listOfRars, progressBarPerStep


def decompressZip(listOfZips, values, window, progressBarValue, progressBarPerStep):
    # Открыть каждый zip и разархивировать
    for i in listOfZips:
        try:
            pathToZip = values['Choose'] + i
            pathToFolder = pathToZip[0:len(pathToZip)-4]
            if os.path.exists(pathToFolder):
                print("! Warning directory is exist for - ", i)
            elif zipfile.is_zipfile(pathToZip):
                z = zipfile.ZipFile(pathToZip, 'r')
                z.extractall(pathToFolder)
                z.close()
                os.chmod(pathToZip, 0o777)
                os.remove(pathToZip)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .zip") 

            progressBarValue += progressBarPerStep
            window['progbar'].update_bar(progressBarValue + 1)
            window['percent_progress'].update(str(round(progressBarValue/10)) + ' %')
        except Exception as e:
            print("× Error -", e)
            continue
    return progressBarValue


def decompressRar(listOfRars, values, window, progressBarValue, progressBarPerStep):    
    for i in listOfRars:
        try:
            pathToRar = values['Choose'] + i
            pathToFolder = pathToRar[0:len(pathToRar)-4]
            if os.path.exists(pathToFolder):
                print("! Warning directory is exist for - ", i)
            elif patoolib.get_archive_format(pathToRar)[0] == "rar":
                patoolib.extract_archive(
                    pathToRar, outdir=pathToFolder, verbosity=-1)
                os.chmod(pathToRar, 0o777)
                os.remove(pathToRar)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .rar")
                    
            progressBarValue += progressBarPerStep
            window['progbar'].update_bar(progressBarValue + 1)
            window['percent_progress'].update(str(round(progressBarValue/10)) + ' %') 
        except Exception as e:
            print("× Error -", e)
            continue