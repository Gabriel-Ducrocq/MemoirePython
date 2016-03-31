#!/usr/bin/env python
#-*- coding: utf-8 -*-


import sys
import numpy as np
import Tkinter as tk
import hashlib
import pickle
import os.path
import tkMessageBox
import cv2
from Seance import Seance



class User:
#Pour chaque utilisateur qui s'inscrit, un objet User est créé. Cet objet contient les informations requises: nom, prénom, mot de passe.
    def __init__(self, prenom, nom, password):

        self.prenom = prenom
        self.nom = nom
        self.password = password


    def get_prenom(self):

        return (self.prenom)


    def get_nom(self):

        return(self.nom)


    def get_password(self):

        return(self.password)








#Fenetre de départ, deux options: creer un compte ou se logger pour commencer.
class Init:

    def __init__(self, master, second):

        self.master = master
        self.second = second
        self.frame = tk.Frame(self.master)
        self.start = tk.Button(self.frame,  text = 'Commencer', width = 25, command = self.second.affiche3)
        self.subscribe = tk.Button(self.frame, text = "Créer un compte", width = 25, command = self.second.affiche2)

        self.start.place(x = 20, y = 20)
        self.start.pack()
        self.subscribe.pack()
        self.frame.pack()




    def __del__(self):

        self.frame.destroy()









#Fenetre qui permet de creer un compte: un pseudo, un password et une confirmation de password.
#Creer le compte emmene directement vers le menu pour commencer.
class Inscription:

    def __init__(self, master, cadre):

        self.cadre = cadre
        self.master = master
        self.frame = tk.Frame(self.master)
        self.pres = tk.Label(self.frame, text = 'Créer un compte', width = 25)

        vNom = tk.StringVar()
        self.nom = tk.Entry(self.frame, textvariable = vNom)
        vNom.set("Nom")


        vPrenom = tk.StringVar()
        self.prenom = tk.Entry(self.frame, textvariable = vPrenom)
        vPrenom.set("Prénom")


        vPassword1 = tk.StringVar()
        self.password1 = tk.Entry(self.frame, textvariable = vPassword1, show = "*")
        vPassword1.set("Mot de passe")


        vPassword2 = tk.StringVar()
        self.password2 = tk.Entry(self.frame, textvariable = vPassword2, show = "*")
        vPassword2.set("Confirmez mot de passe")


        self.confirmer = tk.Button(self.frame, text = "Créer", command = self.creer_compte)


        self.noMatch = tk.Label(self.frame, text = "Les mots de passe ne matchent pas !")
        self.AlreadyExist = tk.Label(self.frame, text = "Ce compte existe déjà !")

        self.pres.pack()
        self.nom.pack()
        self.prenom.pack()
        self.password1.pack()
        self.password2.pack()
        self.confirmer.pack()
        self.frame.pack()


    def creer_compte(self):
        #Méthode qui crée le fichier contenant les informations que l'utilisateur a rentré.
        #Le mot de passe est crypté par l'algorithme de hashage sha1, puis converti en chaîne de caractères.

        if(self.password1.get() == self.password2.get()):

            prenom = self.prenom.get()
            nom = self.nom.get()

            password = (hashlib.sha1(self.password1.get().encode(encoding = "UTF-8"))).hexdigest()
            user = User(prenom, nom, password)

            chemin = "data/account/"+nom+prenom
            if os.path.isfile(chemin) == False :

                with open(chemin, "wb") as fichier:
                    mon_pickler = pickle.Pickler(fichier)
                    mon_pickler.dump(user)

                fichier.close()

                tkMessageBox.showinfo('Création', "Compte créé !")
                self.cadre.affiche1()

            else:

                self.AlreadyExist.pack()

        else:

            self.noMatch.pack()




    def __del__(self):

        self.frame.destroy()




#Fenetre qui s'affiche avant de debuter la session.
class FenetreStart:


    def __init__(self, master, cadre):

        self.cadre = cadre
        self.master = master
        self.frame = tk.Frame(self.master)



        vNom = tk.StringVar()
        self.Nom = tk.Entry(self.frame, textvariable = vNom)
        vNom.set("Nom")


        vPrenom = tk.StringVar()
        self.Prenom = tk.Entry(self.frame, textvariable = vPrenom)
        vPrenom.set("Prénom")


        vPassword = tk.StringVar()
        self.Password = tk.Entry(self.frame, textvariable = vPassword, show = "*")
        vPassword.set("Mot de passe")

        self.start = tk.Button(self.frame, text = "Commencer", command = self.begin)

        self.PwdUnknown = tk.Label(self.frame, text = "Ce n'est pas le bon mot de passe !")
        self.DoesntExist = tk.Label(self.frame, text = "Ce compte n'existe pas !")

        self.Nom.pack()
        self.Prenom.pack()
        self.Password.pack()

        self.start.pack()
        self.frame.pack()


    def begin(self):

    #Si on trouve le compte.
        chemin = "data/account/"+self.Nom.get()+self.Prenom.get()

        if os.path.exists(chemin):
            with open(chemin, "rb") as f:
                mon_depickler = pickle.Unpickler(f)
                user = mon_depickler.load()


            prenom = user.get_prenom()
            nom = user.get_nom()
            pwd = user.get_password()

            #Si le mot de passe entré matche avec le mot de passe du compte, on commence la séance.
            if pwd == (hashlib.sha1(self.Password.get().encode(encoding = "UTF-8"))).hexdigest():
                seance = Seance(self.Prenom.get(), self.Nom.get())
                seance.start()

            else:
                self.PwdUnknown.pack()


        else:
            self.DoesntExist.pack()



    def __del__(self):

        self.frame.destroy()





#Classe qui s'occupera des allers et retours entre les fenêtres.
class Cadre:

    def __init__(self, root):

        self.root = root
        self.f1 = Init(self.root, self)



    def affiche1(self):

        self.f3 = FenetreStart(self.root, self)
        self.f2.__del__()

    def affiche2(self):

        self.f1.__del__()
        self.f2 = Inscription(self.root, self)


    def affiche3(self):

        self.f3 = FenetreStart(self.root, self)
        self.f1.__del__()







