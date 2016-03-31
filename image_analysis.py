#!/usr/bin/env python
#-*- coding: utf-8 -*-


import cv2
import numpy as np



def contours(frame):
	#Conversion en niveaux de gris.
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#Thresholding
	ret,thresh = cv2.threshold(gray, 0, 255, 0)
	#Détection des contours externes. cv2.CHAIN_APPROX_SIMPLE compresse les contours en ne gardant que les points extrêmes des segments.
	_,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return contours





#Fonction qui trouve le plus grand contour parmi la liste donnée - basée sur l'aire.
def max_contour(contours):
	max_i = 0
	max_area = 0

	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_area = area
			max_i = i

	contour = contours[max_i]
	return contour



#On retourne l'enveloppe convexe du contour.
def hull(contour):
	hull = cv2.convexHull(contour)
	return hull




#On trouve le centre de gravité du contour passé à cette fonction.
def centroid(contour):
	moments = cv2.moments(contour)
	if moments['m00'] != 0:
		cx = int(moments['m10']/moments['m00'])
		cy = int(moments['m01']/moments['m00'])
		return (cx,cy)
	else:
		return None






