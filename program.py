import os
import mysql.connector
import configparser

from connexion import querysql
from connexion import querycreatetable
from connexion import queryinsertinto
from mixfilescsv import addlinecsv
from mixfilescsv import iscsv

config = configparser.ConfigParser()
config.read_file(open('config.ini'))
dbuser = config.get('MYSQL','user')
dbpassword = config.get('MYSQL','password')
dbhost = config.get('MYSQL','host')
dbdatabase = config.get('MYSQL','database')
dbport = config.get('MYSQL','port')

connect = mysql.connector.connect(
    user=dbuser, 
    password=dbpassword, 
    host=dbhost, 
    database=dbdatabase,
    port=dbport
    )

def include(filename):
    if os.path.exists(filename):
        exec(open(filename).read())

def ajoutdonnee():
    try:
        # Tentative de connexion à la bd
        include('connexion.py')
        connected = True

        separator = config.get('PARAM','separator')
        filepath = config.get('PARAM','filepath')
        nomtable = input("table name ?   ")

        files = os.listdir(filepath)
        filecsv=0
        totalfile=0
        listproblemfile=[]
        listcsv=[]
        listeentete=[]
        listeentete2=[]
        listdata=[]
        listdata2=[]
        entetedone=False
        tableexist=False

        for file in files:
            try: # try par fichier
                if iscsv(file): # fichier csv
                    listcsv.append(str(file))
                    totalfile+=1
                    countline=0
                    filecsv+=1
                    f = open(file)
                    for ligne in f:
                        valeurligne=""
                        countline+=1
                        if countline==1: #entete
                            if not entetedone:
                                for lettre in ligne:
                                    if lettre!=separator:
                                        valeurligne+=str(lettre)
                                    else:
                                        listeentete.append(valeurligne)
                                        valeurligne=""
                                listeentete.append(valeurligne.replace("\n",""))
                                valeurligne=""
                                entetedone = True
                        else: # data
                                listdata.clear()
                                listdata2.clear()
                                listeentete2.clear()
                                valeurligne=""

                                for lettre in ligne:
                                    if lettre=="'":
                                        lettre=="''"
                                    elif lettre!=separator:
                                        valeurligne+=str(lettre)
                                    else:
                                        if valeurligne != "":
                                            valeurligne = valeurligne.replace("?","é")
                                            listdata.append(valeurligne)
                                            valeurligne=""
                                        else:
                                            listdata.append("NULL")

                                for i in range(0,len(listdata)):
                                    if listdata[i]!="NULL":
                                        listeentete2.append(listeentete[i])
                                        listdata2.append(listdata[i])

                                if tableexist==False:
                                    querycreatetable(nomtable,listeentete,listdata)
                                    tableexist = True
                                queryinsertinto(nomtable,listeentete2,listdata2)
                    f.close()
            except mysql.connector.Error as Err: # except par fichier
                listnocheck = ["config.ini","program.py","mixfilescsv.py","__pycache__","connexion.py"]
                if str(file) not in listnocheck:
                    listproblemfile.append(str(file))
                print(Err)
        

        message="\nLes fichiers que je ne peux pas parcourir sont :"
        if len(listproblemfile)>0:
            for fichiernotcsv in listproblemfile:
                message+=("\n" + fichiernotcsv)
            print(message)

        message2="\n" + str(totalfile) + " fichiers parcourus :"
        if len(listcsv)>0:
            for fichiercsv in listcsv:
                message2+=("\n" + fichiercsv)
            print(message2)
            print()

    except mysql.connector.Error as Err: # except programme
        if connected==False:
            print("Impossible de se connecter a la base de donnee, verifier le fichier connexion.ini")
        else:
            print(Err)

ajoutdonnee()
connect.close()