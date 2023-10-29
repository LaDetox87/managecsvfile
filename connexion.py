import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

connected = False

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

c = connect.cursor()

def convertvaleur(query):
    # Rechercher les occurrences de valeurs au format "1,2001E+11" dans la requête
    # et les convertir en entiers
    if "E+" in query and "," in query:
        query = float(query.replace(',', ''))
        converted_value = int(query)
        return(converted_value)
    return(query)

def querysql(query):
    printquery = config.get('PARAM','printquery')
    if printquery:
        print("requete en cours : {}".format(query))
    if query[-1]!=";":
        query+=";"
    c.execute(query)
    c.execute("commit;")

def querycreatetable(nomtable,listeentete,listdata):
    query = "create table if not exists {} (id int auto_increment primary key, {} {}".format(nomtable,listeentete[0],typedatasql(listdata[0]))
    for i in range(1,len(listeentete)):
        query+=", {} {}".format(listeentete[i],typedatasql(listdata[i]))
    query+=");"
    print()
    querysql(query)

def queryinsertinto(nomtable, listeentete, listdata):
    query = "insert into {}({}".format(nomtable,listeentete[0])
    for i in range(1,len(listeentete)):
        query+=", {}".format(listeentete[i])
    query+=") values ({}".format(listdata[0])
    for i in range(1,len(listdata)):
        listdata[i] = convertvaleur(listdata[i])
        try:
            listdata[i] = int(listdata[i])
            query+=", {}".format(listdata[i])
        except:
            if typedatasql(listdata[i]) == "varchar(100)" and listdata[0]!="'" and listdata[-1]!="'":
                listdata[i] = "'" + listdata[i] + "'"
            query+=", {}".format(convertvaleur(listdata[i]))
    query+=");"
    print("\n" + query + "\n")

    c.execute(query)
    connect.commit()

def typedatasql(data): #retourne le type d'une donnee python en format mysql
    try:
        data = int(data)
        return('bigint')
    except:
        try:
            data = float(data)
            return('decimal')
        except:
            return('varchar(100)')
        
def convertion(data):
    try:
        return int(data)
    except:
        try:
            return float(data)
        except:
            return str(data)
