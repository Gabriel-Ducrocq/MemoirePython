#!/usr/bin/env python
#-*- coding: utf-8 -*-

from threading import Thread
import cv2
import image_analysis
import pickle
import time
from random import randint
from Phenomenon import *






class Vision(Thread):
#Ici on définit une classe qui hérite de la classe Thread. La classe Vision s'occuper du traitement de l'image.
#Elle possède deux variable:
#   - state, qui vaut false lorsque l'utilisateur n'a pas passé sa main dans le carré de gauche puis celui de droite.
#   - over, qui vaut false tant que l'utilisateur n'est pas arrivé au bout des instructions de la séance.
    def __init__(self):

        Thread.__init__(self)

        self.state = False
        self.over = False
        self.calibre = False


    def getState(self):

        return(self.state)



    def setState(self, bool):

        self.state = bool



    def getOver(self):

        return(self.over)


    def setOver(self, bool):

        self.over = bool


    def apply_hist_mask(self, frame, hist):
        #Méthode qui détecte la couleur de la peau étant donné un histogramme de couleurs.
        #On commence par convertir l'image RGB en HSV, puis on déterminé les probabilité que chaque pixel appartiennent à de la peau.
        #Enfin nous convoluons l'image en HSV avec un noyau elliptique.
        #Finalement, nous seuillons le résultat obtenu et transformons l'image en noir et blanc.
        #Enfin nous lissons l'image à l'aide d'un noyau gaussien et nous remplaçons les pixels où la couleur de peau n'est pas détectée par des pixels noirs dans l'image initiale.
        #Nous la renvoyons.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0,1], hist, [0,180,0,256], 1)

        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
        cv2.filter2D(dst, -1, disc, dst)



        ret, thresh = cv2.threshold(dst, 100, 255, 0)
        thresh = cv2.merge((thresh,thresh, thresh))

        cv2.GaussianBlur(dst, (3,3), 0, dst)

        res = cv2.bitwise_and(frame, thresh)
        return res





    def draw_final(self, hand_masked):
        #On détecte les contours de la main.
        contours = image_analysis.contours(hand_masked)
        centroid = None
        # Si on contours n'est pas None et s'il y a au moins un contour détecté.
        if contours is not None and len(contours) > 0:
            #On détermine le plus grand contour.
            max_contour = image_analysis.max_contour(contours)
            #On détermine l'enveloppe convexe du plus grand contour.
            hull = image_analysis.hull(max_contour)
            #On trouve le centre de gravité de cette enveloppe convexe.
            centroid = image_analysis.centroid(hull)

        if centroid is not None:
            return (centroid)


        return(None)





    def set_hand_hist(self, frame):
    #Cette méthode calcule l'histogramme de la couleur de peau.
    #On commence par définir les bornes du rectangle, puis on convertit l'image en HSV.
    #Nous ne gardons que la portion d'image figurant dans le rectangle.
    #Finalement, nous claculons l'histogramme et nous le normalisons
        c11 = 150
        c12 = 150
        c21 = 300
        c22 = 300


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        roi = hsv[c11:c21, c12:c22]

        self.hand_hist = cv2.calcHist([roi],[0, 1], None, [180, 256], [0, 180, 0, 256])
    #Les paramètres signifient que cv2.NORM_MINMAX signifie que min(self.hand_hist) = 0 et max(self.hand_hist) = 255
        cv2.normalize(self.hand_hist, self.hand_hist, 0, 255, cv2.NORM_MINMAX)

        return(self.hand_hist)




    def run(self):
    #Cette méthode lance le traitement de l'image.

    #Ici on défini les coins des rectangles qui vont nous servir.
        a11 = 100
        a12 = 300
        a21 = 0
        a22 = 128


        b11 = 600
        b12 = 300
        b21 = 500
        b22 = 128


    #On crée les deux variables qui vont nous servir à savor si l'utilisateur a passé la main dans le rectangle de gauche puis dans celui de droite.
        running1 = True
        running2 = False

    #On tente d'obtenir une image via la webcam.
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False


        while rval:

            c11 = 150
            c12 = 150
            c21 = 300
            c22 = 300

            cv2.rectangle(frame,(c11,c12),(c21,c22),(0, 255, 0),3)
            hand = self.set_hand_hist(frame)
            cv2.imshow("preview", frame)
            rval, frame = vc.read()
            key = cv2.waitKey(20)

            if key == 27:
                self.calibre = True
                break




    #Si on a réussi à obtenir une image et tant qu'on réussi à en obtenir.
        while rval:


    # Si l'utilisateur est parvenu au bout des instructions, on quitte la boucle: le process de traitement d'image s'arrête puisque la séance est terminée.
            if self.over:
                break




    #Ici on défini les couleurs des rectangles: vert si l'utilisateur n'a pas passé sa main dedans, rouge s'il l'a fait.
    #Le rectangle de droite ne devient rouge que si le rectange de gauche l'est avant lui, comme expliqué.
            col1 = (0, 255, 0)
            if not running1:
                    col1 = (0, 0, 255)


            col2 = (0, 255, 0)
            if running2:
                    col2 = (0, 0, 255)


        #On détecte la couleur de peau sur l'image.
            res = self.apply_hist_mask(frame, hand)
        #On obtient le centre de gravité de la main.
            point = self.draw_final(res)


        #Si on a bien obtenu le centre, on dessine un point noir sur l'écran.
        #Si ce point passe dans le rectangle de gauche, on met running1 à False.
        #Si suite au rectangle de gauche il passe dans celui de droite, on met running2 à True.
            if point is not None:
                cv2.circle(frame,point, 10, (0,0,0), -1)

                if point[0] < a11 and point[0] > a21 and point[1] < a12 and point[1] > a22:
                    running1 = False

                if point[0] < b11 and point[0] > b21 and point[1] < b12 and point[1] > b22 and not running1:
                    running2 = True



            #Finalement, si running1 est False et running2 est True, cela signifie que le programme doit passer à l'instruction suivante.
            #On met alors state à True.
                if not running1 and running2:
                    self.state = True
                    running1 = True
                    running2 = False


            #On dessine les rectangles.
            cv2.rectangle(frame,(a21,a22),(a11,a12),col1,3)
            cv2.rectangle(frame,(b21,b22),(b11,b12),col2,3)

            #On renvoie l'image.
            cv2.imshow("preview", frame)

            #On tente d'obtenir une nouvelle image.
            rval, frame = vc.read()
            key = cv2.waitKey(20)
            #Si on tape sur la touche échape, alors le programme s'arrête: aussi bien les instructions que le traitement de l'image.
            if key == 27: # exit on ESC
                self.over = True
                self.state = True
                break



        #Finalement, lorsque la séance est terminée on détruit la fenêtre.
        cv2.destroyWindow("preview")







class Voice(Thread):
#Calsse qui gère les instructions de chaque phénomène hypnotique selon une liste qui lui est donnée en paramètre.
#On lui donne aussi un objet vision, pour que les liens entre le traitement de l'image et la voix artificelle puissent se faire.
    def __init__(self, listPheno, vision):

        Thread.__init__(self)

        self.listPheno = listPheno
        self.viz = vision
        self.calib = Calibration()
        self.inst = Instructions()
        self.end = End()




    def run(self):
    #On commence la suite d'instructions relatives à la liste de phénomènes passés en paramètres.

        while not self.viz.calibre:
            self.calib.launch()
            time.sleep(4)


        self.inst.launch()

        time.sleep(3)
        for i in self.listPheno:
        #Pour chaque phénomène de la liste, on lit ses instructions, puis one regarde la variable state de l'objet vision
        #pour savoir si l'utilisateur les a mises en oeuvre.
            self.viz.setState(False)
            i.launch()
            state = self.viz.getState()


            #Si state = True, on n'entre pas dans la boucle d'encouragements, on passe directement au phénomène suivant.
            #Tant que state = False, on distribue des encouragements avec des pauses de temps aléatoire - entre 0 et 10 secondes.
            #A chaque iteration on regarde la variable state pour savoir si l'utilisateur a finalement réussi.
            while not state:
                duree = randint(0, 10)
                time.sleep(duree)
                i.encouragement()
                state = self.viz.getState()


            #Si la variable Over de l'objet vision est True, cela signifie que la séance est fini - l'utilisateur a appuyé sur echap.
            #On sort donc de la boucle des phénomènes, peu importe où on en était.
            if self.viz.getOver():
                break



        self.end.launch()
        #Finalement, une fois la liste des phénomènes finis, on met la variable à True pour que l'objet Voice puisse savoir
        # que la séance est finie.
        self.viz.setOver(True)

