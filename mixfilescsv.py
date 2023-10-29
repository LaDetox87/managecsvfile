#fusionne des fichiers csv qui n'ont pas les memes datas
import os
import csv

def include(filename):
    if os.path.exists(filename):
        exec(open(filename).read())

def addlinecsv(file,line):
     #ajoute la ligne en parametre dans un fichier csv en parametre
     filewriter = csv.writer(file)
     filewriter.writerow(line)

def iscsv(file):
    #return true si le fichier en parametre est un fichier csv sinon return false
    return (file[-1] == 'v' and file[-2] == 's' and file[-3] == 'c' and file[-4] == '.')

def tomixfilecsv():
    countfile = 0
    counteveryline = 0
    listcsvfile = []
    directorypath = input("path of directory?  ") # chemin du dossier des fichiers csv
    output = input("name of ouput file ?  ")      # chemin de sortie du fichier final csv
    if iscsv(output)==False:
        output+='.csv'
    files = os.listdir(directorypath)
    for file in files:
        if iscsv(file):
            listcsvfile.append(file) # on recupere tous les fichiers csv du dossier dans une liste python
    result=open(output,'w')
    for csvfile in listcsvfile: # pour chaque fichier csv dans la liste
        csvfile=open(csvfile)
        countfile+=1
        countline=0
        for line in csv.reader(csvfile): # pour chaque ligne du fichier csv
            counteveryline+=1
            countline+=1
            if countline==1: #si on est dans l'entete
                if countfile==1:# si on est dans l'entete du premier fichier
                    addlinecsv(result,line) #on ajoute la ligne de l'entete
                else:
                    counteveryline-=1 # on ne compte pas l'entete non rajoutee comme une ligne de data parcourue
            else: # si c'est une ligne de data
                addlinecsv(result,line) 
    print("Count of file : " + str(countfile) + "\nCount of line : " + str(counteveryline))