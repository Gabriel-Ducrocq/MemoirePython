#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Phenomenon
import time
import numpy as np
import threads



class Seance:
#Lorsque l'utilisateur a commencé la session, un objet Seance est créé, contenant son nom et son prénom.
#Deux threads sont également définis: un pour le traitement d'image et un autre pour la voix artificielle.
    def __init__(self, prenom, nom):

        self.prenom = prenom
        self.nom = nom


        self.instructions1 = Phenomenon.Head()
        self.instructions2 = Phenomenon.Hand()

        self.listPheno = [self.instructions1, self.instructions2]

        self.vision = threads.Vision()
        self.voice = threads.Voice(self.listPheno, self.vision)



    def getVision(self):
        return(self.vision)


    def getVoice(self):
        return(self.voice)



    def start(self):
    #Lorsque que la séance débute, les deux threads sont lancés.
        self.vision.start()
        self.voice.start()

















