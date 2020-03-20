import PySimpleGUI as sg
import patoolib
import zipfile
import os
import shutil


def findArchives(values, event, ok_button):
    listOfZips = []
    listOfRars = []

    if values['Choose'] != '' and event == ok_button: 
        invalidFormatZip = ["....zip", "...zip", "..zip", "  .zip", " .zip"]
        invalidFormatRar = ["....rar", "...rar", "..rar", "  .rar", " .rar"]

        os.chdir(values['Choose'])  # Перейти по пути

        # Найти все .zip / .rar -> занести в список listOfZips / listOfRars
        for root, _, files in os.walk(".", topdown=False):
            for name in files:
                fileName = os.path.join(root, name)
                if fileName.endswith('.zip'):
                    newFileName = fileName
                    for i in invalidFormatZip:
                        newFileName = newFileName.replace(i, ".zip")
                    os.rename(fileName, newFileName)
                    newFileName = newFileName[1:len(
                        newFileName)].replace("\\", "/")
                    listOfZips.append(newFileName)
                elif fileName.endswith('.rar'):
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

# Открыть каждый zip и разархивировать
def decompressZip(listOfZips, values, window, progressBarValue, progressBarPerStep):    
    for i in listOfZips:
        try:
            pathToZip = values['Choose'] + i
            pathToFolder = pathToZip[0:len(pathToZip)-4]
            if os.path.exists(pathToFolder):
                print("! Warning directory is exist for - ", i)
                if values['trashFolders']: 
                    trashFolders(pathToFolder, 0, pathToFolder)
            elif zipfile.is_zipfile(pathToZip):
                z = zipfile.ZipFile(pathToZip, 'r')
                z.extractall(pathToFolder)
                z.close()
                os.chmod(pathToZip, 0o777)
                os.remove(pathToZip)
                if values['trashFolders']: 
                    trashFolders(pathToFolder, 0, pathToFolder)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .zip") 

            progressBarValue += progressBarPerStep
            window['progbar'].update_bar(progressBarValue + 1)
            window['percent_progress'].update(str(round(progressBarValue/10)) + ' %')
        except Exception as e:
            print("× Error in decompressZip -", e)
            continue
    return progressBarValue

# Открыть каждый rar и разархивировать
def decompressRar(listOfRars, values, window, progressBarValue, progressBarPerStep):    
    for i in listOfRars:
        try:
            pathToRar = values['Choose'] + i
            pathToFolder = pathToRar[0:len(pathToRar)-4]
            if os.path.exists(pathToFolder):
                print("! Warning directory is exist for - ", i)
                if values['trashFolders']: 
                    trashFolders(pathToFolder, 0, pathToFolder)
            elif patoolib.get_archive_format(pathToRar)[0] == "rar":
                patoolib.extract_archive(pathToRar, outdir=pathToFolder, verbosity=-1)
                os.chmod(pathToRar, 0o777)
                os.remove(pathToRar)
                if values['trashFolders']: 
                    trashFolders(pathToFolder, 0, pathToFolder)
                print("v Done - ", i)
            else:
                print("× Error - ", i, " - is not .rar")
                    
            progressBarValue += progressBarPerStep
            window['progbar'].update_bar(progressBarValue + 1)
            window['percent_progress'].update(str(round(progressBarValue/10)) + ' %') 
        except Exception as e:
            print("× Error in decompressRar -", e)
            continue

def trashFolders(pathToFolder, caveCounter, mainPath):
    try:        
        listDirs, listFiles, mainPath = findDirs(pathToFolder, caveCounter, mainPath)

        if len(listDirs) == 0:
            if not(len(listFiles) == 0) and not(mainPath == pathToFolder):
                #print(caveCounter,"root: ",mainPath,"\ncurr: ",pathToFolder,"\n\n")                
                for f in listFiles:
                    shutil.move(pathToFolder+"/"+f, mainPath) # переместить каждый файл в указанный dir
                listDirs, _, _ = findDirs(mainPath, 1, '') # выписать dir, которую удалить
                shutil.rmtree(mainPath + "/" + listDirs[0], ignore_errors=True) # удалить ненужный dir
            return
        elif len(listDirs) == 1:
            trashpath = pathToFolder + "/" + listDirs[0]
            caveCounter += 1
            trashFolders(trashpath, caveCounter, mainPath)
        else:
            for i in listDirs:
                trashpath = pathToFolder + "/" + i
                trashFolders(trashpath, 0, mainPath + "/" + i)

    except Exception as e:
        print("× Error in trashFolders -", e)

# В указанном дириктории pathToFolder выполняет
# поиск файлов, папок текущего уровня и выписывается
# текущий каталог, как root дириктория
def findDirs(pathToFolder, caveCounter, mainPath):
    for root, dirs, files in os.walk(pathToFolder):
            if caveCounter == 0:
                mainPath = root
            break
    return dirs, files, mainPath