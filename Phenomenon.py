#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os
import pyttsx
from random import randint


class Phenomene():
#On définit ici une classe Phenomene, dont toutes les classes suivantes vont hériter.
#On donne alors des encouragements généraux, qui s'adaptent à n'importe quel phénomène.
    def __init__(self):

        self.GeneralEncouragements = ["Tres bien", " De plus en plus", "Exactement comme cela", "Tout a fait, sans aucun effort conscient"]
        self.discours = ""


    def launch(self):
    #Méthode qui doit lire le discours de chacun des phénomènes.
    #On définit une voix qui parle à un rythme de 150 mots/minute.
        engine = pyttsx.init()
        engine.setProperty("rate", 150)
        engine.say(self.discours)
        engine.runAndWait()




    def encouragement(self):
    #Méthode qui va choisir un encouragement au hasard parmi la liste donnée et qui va le prononcer.
    #De la mêle façon on définit une voix artificielle qui parle à un rythme de 150 mots/minute.
        index = randint(0, (len(self.GeneralEncouragements)-1))

        engine = pyttsx.init()
        engine.setProperty("rate", 150)
        engine.say(self.GeneralEncouragements[index])
        engine.runAndWait()










class Calibration(Phenomene):
#Instructions de calibration
    def __init__(self):

        Phenomene.__init__(self)

        self.discours = "Placez la paume de vote main sur le rectangle vert et appuez sur echap pour calibrer la couleur de votre peau."








#Premier bloc de la seance: le discours prehypnotique.
class Instructions(Phenomene):

    def __init__(self):

        Phenomene.__init__(self)

        self.discours = "Bonjour, je suis Leonie, une voix artificielle. Je suis la pour que tu rentres en etat d'hypnose a ton propre rythme. Comme je suis un etre artificel, mes propres projections et etats d'ames ne generont pas ton entree progressive dans cet etat."









#Premier bloc de la seance: le discours prehypnotique.
class Head(Phenomene):

    def __init__(self):

        Phenomene.__init__(self)

        self.discours = "Ta tete va tourner"















class Hand(Phenomene):
#Phénomène hypnotique: lévitation de main.
    def __init__(self):

        Phenomene.__init__(self)

        self.discours = "Tu vas pouvoir prendre plaisir a observer la facon dont ta main va monter tout seule, a observer toutes les sensations sucites par ce mouvement"





class End(Phenomene):
#Fin de la séance.
    def __init__(self):

        Phenomene.__init__(self)

        self.discours = "Fin des instructions, le programme va se fermer. Au revoir"