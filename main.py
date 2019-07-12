# ==========================================================================================
# ================================== Projet BAC - VIAPIE ===================================
# ==========================================================================================

# ===========================================
# ------------ BIBLOTHEQUES -----------------
# ===========================================
# On importe ici les bliblitohèques servant au fonctionnement du programme

from tkinter import *
import math
import serial
# ===========================================


# ===========================================
# ------------ CONFIGURATIONS ---------------
# ===========================================
# On configure la couleur souhaitee en arriere-plan
# Pour les couleurs disponibles, se diriger vers le site : http://wiki.tcl.tk/37701

color = "moccasin"
# ===========================================


# ===========================================
# ------------ SERIAL OS MODE ---------------
# ===========================================
# Cas 1 : Enlever le premier # pour configurer le Serial en fonction de l'OS utlisé
# Cas 2 : Mettre un # dans le cas contraire

Bluetooth = serial.Serial("/dev/cu.HC05-DevB", timeout=1)  # Mac OS
#Bluetooth = serial.Serial("COM6", timeout=1)               # Windows OS
# ===========================================


# ===========================================
# ------------ DATA DE SERIAL ---------------
# ===========================================
# On récupère les données présents sur le Serial
# On détecte le type de données récupérées (mode)
# On récupère la partie nombre des données (donnee)
# On associe à une variable précise "donnee" en fonction de "mode"

def BluetoothData():
    global Main, BluetoothData
    global distance, temperature, humidity, position, presence, situation
    
    modes = ["D", "T", "H", "P", "A"]
    nombres = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

    serie = str(Bluetooth.readline())
    liste = list(serie)
    mode = -1
    donnee = ""

    # Détection du mode
    for i in range(len(liste)):
        for a in range(len(modes)):
            if liste[i] == modes[a]:
                mode = a

    # Récupération des données
    for j in range(len(liste)):
        for b in range(len(nombres)):
            if liste[j] == nombres[b]:
                donnee += nombres[b]

    # Mise à jour donnée en fonction du mode
    if mode == 0: #HC-SR04
        distance.set(str(donnee))
    elif mode == 1: #DHT11 - Température
        if str(donnee) != "999.00" :
            temperature.set(str(donnee))
            if 30 <= float(str(donnee)) <= 45:
                situation.set("Chaleur détectée")
            elif float(str(donnee)) >= 45:
                situation.set("Seuil atteint ! État critique !")
            else:
                situation.set("Situation normale")
    elif mode == 2: #DHT11 - Humidité
        if str(donnee) != "999.00" :
            humidity.set(str(donnee))
    elif mode == 3: #Servo
        position.set(str(donnee))
    elif mode == 4: #HC-SR501
        if str(donnee) == "1":
            presence.set("Oui")
        else:
            presence.set("Non")
    else:
        donnee = "-1"

    Main.after(500, BluetoothData)

# ===========================================


# ===========================================
# ------------ AUTHENTIFICATION -------------
# ===========================================
# Fonction affichant la fenetre d'authentification

def security():
    global Main, Security
    global password
    
    Security = Tk()
    Security.title("PROGRAMME V.I.A.P.I.E")
    Security.geometry("700x400")
    Security.resizable(width=False, height=False)

    Security_MainFrame = Frame(Security, bg=color, padx=20, pady=30)
    Security_MainFrame.pack(side=TOP, fill="both")

    Security_TitleFrame = Frame(Security_MainFrame, bg=color, padx=20, pady=38)
    Security_TitleFrame.pack(side=TOP, fill="both")

    Label(Security_TitleFrame, text="PROGRAMME V.I.A.P.I.E", bg=color, font=("Times New Roman", 30)).pack()
    Label(Security_TitleFrame, text="", bg=color).pack()
    Label(Security_TitleFrame, text="Authentification requise", bg=color, font=("Times New Roman", 20)).pack()

    Security_PasswordFrame = Frame(Security_MainFrame, bg=color, padx=20, pady=30)
    Security_PasswordFrame.pack(side=TOP)

    password = StringVar()

    Entry(Security_PasswordFrame, textvariable=password, show="*", bg=color, width=35).grid(row=0, column=1)
    Button(Security_PasswordFrame, text="OK", bg=color, command=authentification).grid(row=0, column=2)

    Info_PasswordFrame = Frame(Security_MainFrame, bg=color, padx=20, pady=10)
    Info_PasswordFrame.pack(side=TOP)
    
    Label(Info_PasswordFrame, text="Copyright © 2016 - DECIAN J. & SIAO K.", bg=color).pack()
    Label(Info_PasswordFrame, text="Tout droits réservés", bg=color).pack()
    Label(Info_PasswordFrame, text="", bg=color).pack()

    Security.mainloop()
    
# Fonction permettant de vérifier l'authentification de l'utilisateur

def authentification() :
    global Main, Security
    global password
    
    if password.get() == "VIAPIE":
        Security.destroy()
        MainProgram()
    else:
        password.set("")

# Fonction fermant la session et permet un retour à la fenetre d'authentification

def session():
    global Main
    
    Main.destroy()
    security()
# ===========================================


# ===========================================
# --------- PROGRAMMES DU VÉHICULE ----------
# ===========================================
# Fonctions mettant en déplacement le véhicule

def mode():
    if state.get() == 1:
        code = "M"
        Bluetooth.write(code.encode("utf-8"))
    else:
        code = "A"
        Bluetooth.write(code.encode("utf-8"))

def arret():
    if state.get() == 1:
        code = "0"
        Bluetooth.write(code.encode("utf-8"))
    
def avant():
    if state.get() == 1:
        code = "1"
        Bluetooth.write(code.encode("utf-8"))
    
def arriere():
    if state.get() == 1:
        code = "2"
        Bluetooth.write(code.encode("utf-8"))
    
def droite():
    if state.get() == 1:
        code = "3"
        Bluetooth.write(code.encode("utf-8"))
    
def gauche():
    if state.get() == 1:
        code = "4"
        Bluetooth.write(code.encode("utf-8"))
# ===========================================    

# ===========================================
# --------- PROGRAMMES SECONDAIRES ----------
# ===========================================
# Programme consernant le Canvas : Sonar

def Sonar():
    global Main
    global radar
    global distance, position
    global obstacle, scale_value

    if distance.get() <= 4000:
        x = (distance.get()*scale_value.get())*math.cos(math.radians(position.get()))
        y = (distance.get()*scale_value.get())*math.sin(math.radians(position.get()))

        if position.get() <= 90:
            radar.delete(obstacle)
            obstacle = radar.create_rectangle(305-x, 305-y, 315-x, 315-y, fill="red")
        elif position.get() >= 90:
            radar.delete(obstacle)
            obstacle = radar.create_rectangle(305+x, 305-y, 315+x, 315-y, fill="red")
        else:
            radar.delete(obstacle)
    else:
        radar.delete(obstacle)

    Main.after(500, Sonar)
    
# Cela concerne les programmes annexes au programme principal

# Menu : V.I.A.P.I.E

def about():
    about = Tk()
    about.title("À propos du VIAPIE")
    about.geometry("400x280")
    about.resizable(width=False, height=False)

    about_Frame = Frame(about, width=400, height=280, bg=color)
    about_Frame.pack(side=TOP, fill="both")
    
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="Programme V.I.A.P.I.E", bg=color, font=("Times New Roman", 30)).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="Version 3.4.2", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="Copyright © 2016 - DECIAN J. & SIAO K.", bg=color).pack()
    Label(about_Frame, text="Tout droits réservés", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()
    Label(about_Frame, text="", bg=color).pack()

def creators():
    creators = Tk()
    creators.title("Créateurs")
    creators.geometry("400x400")
    creators.resizable(width=False, height=False)

    creators_Frame = Frame(creators, width=400, height=400, bg=color)
    creators_Frame.pack(side=TOP, fill="both")

    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="Qui sont les créateurs ?", bg=color, font=("Times New Roman", 25)).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="Le programme a été pensé et réalisé par deux élèves", bg=color).pack()
    Label(creators_Frame, text="de la Terminale Sa de la spécialité ISN du Lycée", bg=color).pack()
    Label(creators_Frame, text="La-Mennais :", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="DECIAN Jean", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="&", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="SIAO Kalei", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    Label(creators_Frame, text="", bg=color).pack()
    

def project():
    project = Tk()
    project.title("But du projet")
    project.geometry("500x500")
    project.resizable(width=False, height=False)

    project_Frame = Frame(project, width=500, height=500, bg=color)
    project_Frame.pack(side=TOP, fill="both")
    
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="Pourquoi ce projet ?", bg=color, font=("Times New Roman", 25)).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="Les pompiers prennent du temps avant d'intervenir.", bg=color).pack()
    Label(project_Frame, text="Ils doivent d'abord faire un diagnostic des lieux,", bg=color).pack()
    Label(project_Frame, text="car chaque incendie est différente, a sa", bg=color).pack()
    Label(project_Frame, text="particularité.", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="Ce retard peut-etre fatal : ", bg=color).pack()
    Label(project_Frame, text="- plus de dégats matérielles", bg=color).pack()
    Label(project_Frame, text="- des vies qui peuvent etre en jeu", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="L'objectif de ce projet étant d'aider au maximum les", bg=color).pack()
    Label(project_Frame, text="pompiers, pour pouvoir intervenir plus rapidement et", bg=color).pack()
    Label(project_Frame, text="plus efficacement lorsque qu'un incendie se déclare.", bg=color).pack()
    Label(project_Frame, text="Et les informations recueillies par notre VIAPIE seront", bg=color).pack()
    Label(project_Frame, text="transmises à un ordinateur qui va indiquer aux pompiers", bg=color).pack()
    Label(project_Frame, text="l'état de l'incendie, afin qu'ils prennent le moins de risque possible.", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    Label(project_Frame, text="", bg=color).pack()
    
# Menu : Aide

def use():
    
    use = Tk()
    use.title("Notice d'utilisation")
    use.geometry("600x400")

    use_Frame = Frame(use, width=600, height=400, bg=color)
    use_Frame.pack(side=TOP, fill="both")

    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="Comment utiliser le V.I.A.P.I.E", bg=color, font=("Times New Roman", 30)).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="Le V.I.A.P.I.E est à utiliser avec précaution, toute chute pourrait l'endommager.", bg=color).pack()
    Label(use_Frame, text="Le Bluetooth du V.I.A.P.I.E peut parfois se déconnecter : changer les piles.", bg=color).pack()
    Label(use_Frame, text="Lorsque le V.I.A.P.I.E n'envoie aucune donnée, redémarrer le V.I.A.P.I.E et le programme.", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="Il est recommandé d'utilser le V.I.A.P.I.E sur une surface plate.", bg=color).pack()
    Label(use_Frame, text="Il est recommandé de ne pas utiliser le V.I.A.P.I.E sous la pluie.", bg=color).pack()
    Label(use_Frame, text="Il est recommandé de ne pas utiliser le V.I.A.P.I.E sur la route.", bg=color).pack()
    Label(use_Frame, text="Il est recommandé de ne pas marcher sur le V.I.A.P.I.E.", bg=color).pack()
    Label(use_Frame, text="Il est recommandé de ne pas rouler sur le V.I.A.P.I.E.", bg=color).pack()
    Label(use_Frame, text="Il est recommandé de ne pas alourdir le V.I.A.P.I.E.", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()
    Label(use_Frame, text="", bg=color).pack()

# ===========================================
# ------------ PROGRAMME PRINCIPAL ----------
# ===========================================

def MainProgram():
    global Main, BluetoothData, Sonar
    global radar
    global distance, temperature, humidity, position, presence, situation
    global state, obstacle, scale_value
    
    Main = Tk()
    Main.title("PROGRAMME V.I.A.P.I.E")
    Main.geometry("1100x500") #Maximum 1300x700
    Main.resizable(width=False, height=False)

    menubar = Menu(Main)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="À propos du VIAPIE", command=about)
    menu1.add_separator()
    menu1.add_command(label="Créateurs", command=creators)
    menu1.add_command(label="But du projet", command=project)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=Main.destroy)
    menu1.add_separator()
    menu1.add_command(label="Fermer la session", command=session)
    menubar.add_cascade(label="V.I.A.P.I.E", menu=menu1)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label="Notice d'utilisation", command=use)
    menubar.add_cascade(label="Aide", menu=menu3)

    Main.config(menu=menubar)

    situation = StringVar()
    situation.set("...")

    message_box = LabelFrame(Main, text="SITUATION", bg=color, padx=20, pady=20)
    message_box.pack(side=BOTTOM, fill=X)

    Label(message_box, textvariable=situation, bg=color).pack()

    radar_frame = LabelFrame(Main, text="RADAR", bg=color, padx=20, pady=20)
    radar_frame.pack(side=LEFT, fill=Y)

    radar = Canvas(radar_frame, height=310, width=620, bg="light grey")
    radar.pack(side = LEFT)

    radar.create_arc(10,10,610,610, start = 0, extent = 180, fill="light grey", width=2)
    radar.create_arc(85,85,535,535, start = 0, extent = 180, fill="light grey", width=2)
    radar.create_arc(160,160,460,460, start = 0, extent = 180, fill="light grey", width=2)
    radar.create_arc(235,235,385,385, start = 0, extent = 180, fill="light grey", width=2)

    radar.create_line(310,310,310+310*math.cos(math.radians(45)), 310-310*math.sin(math.radians(45)), width=2)
    radar.create_line(310,310,310+310*math.cos(math.radians(90)), 310-310*math.sin(math.radians(90)), width=2)
    radar.create_line(310,310,310+310*math.cos(math.radians(135)), 310-310*math.sin(math.radians(135)), width=2)

    obstacle = radar.create_rectangle(310, 310, 310, 310, fill=color)

    state = IntVar()

    command_frame = LabelFrame(Main, text="COMMANDES", bg=color, padx=20, pady=20)
    command_frame.pack(side=BOTTOM, fill=X)

    mode_frame = LabelFrame(command_frame, text="MODES", bg=color, padx=20, pady=20)
    mode_frame.pack(side=LEFT, fill=Y)

    Radiobutton(mode_frame, text="Automatique", bg=color, height=2, width=12, variable=state, value=0, command=mode).grid(row=0, column=1)
    Radiobutton(mode_frame, text="Manuel", bg=color, height=2, width=12, variable=state, value=1, command=mode).grid(row=1, column=1)

    manuel_mode = LabelFrame(command_frame, text="COMMANDES MANUELLES", bg=color, padx=20, pady=20)
    manuel_mode.pack(side=LEFT, fill=Y)

    Button(manuel_mode, text="Arret", command=arret).grid(row=1, column=2)
    Button(manuel_mode, text="Avant", command=avant).grid(row=0, column=2)
    Button(manuel_mode, text="Arriere", command=arriere).grid(row=2, column=2)
    Button(manuel_mode, text="Droite", command=droite).grid(row=1, column=3)
    Button(manuel_mode, text="Gauche", command=gauche).grid(row=1, column=1)

    scale_frame = LabelFrame(Main, text="ECHELLE", bg=color, padx=20, pady=20)
    scale_frame.pack(side=LEFT, fill=Y)

    scale_value = DoubleVar()
    scale_value.set(0.150)

    Radiobutton(scale_frame, text="4m", bg=color, height=2, width=10, variable=scale_value, value=0.075, command=Sonar).grid(row=0, column=1)
    Radiobutton(scale_frame, text="2m", bg=color, height=2, width=10, variable=scale_value, value=0.150, command=Sonar).grid(row=1, column=1)
    Radiobutton(scale_frame, text="1m", bg=color, height=2, width=10, variable=scale_value, value=0.300, command=Sonar).grid(row=2, column=1)

    donnee_frame = LabelFrame(Main, text="DONNEES", bg=color, padx=25, pady=23)
    donnee_frame.pack(side=TOP, fill=Y)

    distance, temperature, humidity, position = IntVar(), DoubleVar(), DoubleVar(), IntVar()
    presence, vehicule = StringVar(), StringVar()

    distance.set(1024)
    temperature.set(24.00)
    humidity.set(64.00)
    presence.set("...")

    Label(donnee_frame, text="Distance : ", bg=color, padx=10, pady=10).grid(row=0, column=1)
    Label(donnee_frame, textvariable=distance, bg=color, padx=10, pady=10).grid(row=0, column=2)
    Label(donnee_frame, text="mm", bg=color, padx=10, pady=10).grid(row=0, column=3)
    Label(donnee_frame, text="Température : ", bg=color, padx=10, pady=10).grid(row=1, column=1)
    Label(donnee_frame, textvariable=temperature, bg=color, padx=10, pady=10).grid(row=1, column=2)
    Label(donnee_frame, text="°C", bg=color, padx=20, pady=10).grid(row=1, column=3)
    Label(donnee_frame, text="Humidité : ", bg=color, padx=10, pady=10).grid(row=2, column=1)
    Label(donnee_frame, textvariable=humidity, bg=color, padx=10, pady=10).grid(row=2, column=2)
    Label(donnee_frame, text="%", bg=color, padx=10, pady=10).grid(row=2, column=3)
    Label(donnee_frame, text="Présence détectée : ", bg=color, padx=10, pady=10).grid(row=3, column=1)
    Label(donnee_frame, textvariable=presence, bg=color, padx=10, pady=10).grid(row=3, column=2)

    BluetoothData()
    Sonar()

    Main.mainloop()

security()
