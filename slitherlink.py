from doctest import testmod
from fltk import *

import os.path
from os import path
# ======================================================================
# ==================== Tache 1 : Structures de donnees =================
# ======================================================================

def est_trace(etat, segment):
	"""Vérifie si segment est tracé dans etat
	>>> est_trace({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((0, 1), (1, 1)))
	False
	>>> est_trace({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((1, 1), (2, 1)))
	True
	>>> est_trace({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((2, 1), (3, 1)))
	False
	"""
	segment = verifier_coord(segment)
	if segment in etat and etat[segment] ==  1:
		return True
	return False

def est_interdit(etat, segment):
	"""Vérifie si segment est interdit dans etat
	>>> est_interdit({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((0, 1), (1, 1)))
	True
	>>> est_interdit({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((1, 1), (2, 1)))
	False
	>>> est_interdit({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((2, 1), (3, 1)))
	False
	"""
	segment = verifier_coord(segment)
	if segment in etat and etat[segment] ==  -1:
		return True
	return False


def est_vierge(etat, segment):
	"""Vérifie si segment est vierge dans etat
	>>> est_vierge({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((0, 1), (1, 1)))
	False
	>>> est_vierge({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((1, 1), (2, 1)))
	False
	>>> est_vierge({((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}, ((2, 1), (3, 1)))
	True
	"""
	segment = verifier_coord(segment)
	if segment not in etat:
		return True
	else:
		return False

# ======================================================================
def verifier_coord(segment):
	"""Ordonne correctement segment (avec le plus petit sommet en premier)
	>>> verifier_coord(((1, 2), (1, 1)))
	((1, 1), (1, 2))
	>>> verifier_coord(((2, 1), (1, 1)))
	((1, 1), (2, 1))
	"""
	if segment[0][0] == segment[1][0]: #x identique
		if segment[0][1] > segment[1][1]:
			return (segment[1], segment[0])
        
	if segment[0][1] == segment[1][1]: #y identique
		if segment[0][0] > segment[1][0]:
			return (segment[1], segment[0])
	return segment

def tracer_segment(etat, segment):
	"""
	- Ajoute le segment tracé dans etat
	- Ajoute 1 au compteur_global 
	"""
	global compteur_global
	segment = verifier_coord(segment)
	etat[segment] = 1
	compteur_global += 1
	dessiner(segment, 1)

def interdire_segment(etat, segment):
	"""
	- Ajoute le segment interdit dans etat
	- Soustrait 1 au compteur_global si le segment était tracé avant d'être modifié
	"""
	global compteur_global
	segment = verifier_coord(segment)
	if segment in etat and etat[segment] == 1:
		compteur_global -= 1
	etat[segment] = -1
	dessiner(segment, -1)

def effacer_segment(etat, segment):
	"""
	- Efface le segment dans etat
	- Soustrait 1 au compteur_global
	"""
	global compteur_global
	segment = verifier_coord(segment)
	if segment in etat and etat[segment] == 1:
		compteur_global -= 1
	del etat[segment]
	my_tag = obtenir_tag(segment)
	efface(my_tag)
	
# ======================================================================

def segments_adjacents(etat, sommet):
	"""Retourne liste des 4 segments adjacents a un sommet
	:param etat: dictionnaire
	:param sommet: tuple (coordonnees)
	"""
	
	lst = []
	a = sommet[0]-1, sommet[1]
	b = sommet[0]+1, sommet[1]
	c = sommet[0], sommet[1]-1
	d = sommet[0], sommet[1]+1
	
	if a[0] >= 0:
		s1 = (a, sommet)
		lst.append(s1)
		
	if b[0] <= len(indices[0]):
		s2 = (sommet, b)
		lst.append(s2)
		
	if c[1] >= 0:
		s3 = (c, sommet)
		lst.append(s3)
		
	if d[1] <= len(indices):
		s4 = (sommet, d)
		lst.append(s4)
	
	return lst

def segments_traces(etat, sommet):
	"""Renvoie la liste des segments tracés adjacents à sommet dans etat
	>>> segments_traces({((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}, (2, 4))
	[((2, 3), (2, 4))]
	>>> segments_traces({((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}, (2, 6))
	[]
	"""
	lst = []
	lst_segments = segments_adjacents(etat, sommet)
	for cle in etat:
		for elt in lst_segments:
			if elt == cle and etat[elt] == 1:
				lst.append(elt)
	return lst
					
def segments_interdits(etat, sommet):
	"""Renvoie la liste des segments interdits adjacents à sommet dans etat
	>>> segments_interdits({((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}, (2, 4))
	[]
	"""
	lst = []
	lst_segments = segments_adjacents(etat, sommet)
	for cle in etat:
		for elt in lst_segments:
			if elt == cle and etat[elt] == -1:
				lst.append(elt)
			else:
				pass
	return lst	

def segments_vierges(etat, sommet):
	"""Renvoie la liste des segments vierges adjacents à sommet dans etat
	>>> segments_vierges({((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}, (2, 4))
	[((1, 4), (2, 4))]
	"""
	lst = []
	lst_segments = segments_adjacents(etat, sommet)
	trace = segments_traces(etat, sommet)
	interdit = segments_interdits(etat, sommet)
	for elt in lst_segments:
		if elt not in trace and elt not in interdit:
			lst.append(elt)
	return lst
	
# ======================================================================

def segments_qui_composent_une_case(etat, case):
	"""Renvoie une liste des coordonées des 4 segments d'une case
	"""
	idx = case[0]
	idy= case[1]
	
	s1 = ((case), (idx, idy+1))
	s2 = ((case), (idx+1, idy))
	s3 = ((idx+1, idy), (idx+1, idy+1))
	s4 = ((idx, idy+1), (idx+1, idy+1))
	lst = []
	lst.append(s1)
	lst.append(s2)
	lst.append(s3)
	lst.append(s4)
	return lst


def statut_case(indices, etat, case):
	"""
	Vérifie le statut d'une case et affiche le nombre de segment de la bonne couleur:
	Retourne le nombre de cases satisfaites 
	"""
	idx = case[0] #idx
	idy = case[1] #idy
	idligne = idy
	idcolonne = idx
	booleen_rouge = False

	indice = indices[idligne][idcolonne]
	case_satisfaite = 0
	if indice == None:
		return 1, booleen_rouge
	else:
		lst = []
		liste_segments_dans_case = segments_qui_composent_une_case(etat, case) # 4 segments
		for segment in liste_segments_dans_case:
			trace = est_trace(etat, segment) # determine si un ou plusieurs segments qui composent une case est deja trace

			if trace == True:  
				lst.append(segment)	

		if len(lst) == int(indice): # case satisfaite
			case_satisfaite =+ 1
			affichage_un_indice(idx, idy, "blue")
			

		elif len(lst) < int(indice): # manque de traits
			affichage_un_indice(idx, idy, "black")
			
		else: # trop de traits
			affichage_un_indice(idx, idy, "red")
			booleen_rouge = True

		return case_satisfaite, booleen_rouge


# ======================================================================
# ==================== Tache 2 : Conditions de victoire ================
# ======================================================================

def indices_satisfaits():
	"""
	Vérifie que chaque indice est satisfait : chaque case contenant un nombre 
	k compris entre 0 et 3 a exactement k côtés tracés. 
	Renvoie True si c'est vérifié (False sinon), booleen_rouge (s'il existe un indice en rouge)
	"""
	booleen_rouge = False
	idy = -1
	nb_cases_satisfaites = 0
	statut = 0
	
	for ligne in range(len(indices)):
		idy += 1
		idx = -1

		for colonne in indices[ligne]:
			idx +=1
			statut, booleen_rouge2 = statut_case(indices, etat, (idx, idy))
			if booleen_rouge2 == True:
				booleen_rouge = True

			if statut != 0 :
				nb_cases_satisfaites += 1

	if nb_cases_satisfaites != len(indices)*len(indices[ligne]) :
		return False, booleen_rouge
	else:
		return True, booleen_rouge


def longueur_boucle(etat, segment):
	"""Renvoie None si le segment n’appartient pas à une boucle,
	et la longueur de la boucle à laquelle il appartient sinon
	"""
	compteur = 0
	depart = segment[0]
	precedent, courant = segment[0], segment[1]
	if est_trace(etat, segment) == True:
		compteur = 1
	while courant != depart:
		lst_seg_traces = segments_traces(etat, courant)
		if len(lst_seg_traces) != 2:
			return None
		else:
			for seg1 in lst_seg_traces:
				if seg1[0] == courant:
					if seg1[1] != precedent:
						precedent = courant
						courant = seg1[1]
						compteur += 1
						break
				else:
					if seg1[0] != precedent:
						precedent = courant
						courant = seg1[0]
						compteur += 1
						break
	return compteur

# ======================================================================
# ==================== Tache 3 : Interface graphique ===================
# ======================================================================

def charger_grille():
	"""Charge la grille de son choix et detecte les eventuelles erreurs 
	- le fichier n'existe pas
	- la taille des lignes est differente
	- presence d'un ou de plusieurs caracteres interdits
	"""
	boucle = True
	while boucle:
		grille = str(input("grille (format .txt) : "))
		non = False  # utiliser pour la presence d'un caractere
		cmpt = 0 # comptage des erreurs
		if os.path.exists(grille) == False:
			print("erreur : le fichier n'existe pas")
			boucle = True
			cmpt += 1
			continue

		lst_available = ["0","1","2","3","_","\n"]
		f = open(grille, 'r')
		lignes = f.readlines()
		lst = []
		taille_ligne = []
		for ligne in lignes:	
			taille_ligne.append(len(ligne))
		result = all(element == taille_ligne[0] for element in taille_ligne)
		if result == False:
			print("erreur : la taille des lignes est differente")
			boucle = True
			cmpt += 1

		for ligne in lignes:
			for car in ligne:
				if car not in lst_available:
					non = True
					boucle = True
					cmpt += 1
		if non == True: print("erreur : presence d'un ou de plusieurs caracteres interdits")

		if cmpt == 0:
			boucle = False
			print("grille valide")

	for ligne in lignes:
		lst0 = []
		for car in ligne:	
			if car != '\n':
				if car == '_':
					car = None
				lst0.append(car)
		lst.append(lst0)
		f.close()

	return lst


def coords_sommets():
	"""Dessine tous les sommets
	"""
	for idligne in range(nb_sommet_verticales):
		for idcolonne in range(nb_sommet_horizontales):
			x, y = (taille_marge + idcolonne * taille_case, taille_marge + idligne * taille_case)
			cercle(x, y, 5, couleur='black', remplissage='black', epaisseur=1, tag='')


def init_affichage_indices(indices):
	"""Affiche les indices dans l'interface graphique
	"""
	for idligne in range(len(indices)):
		idy = idligne
		for idcolonne in range(len(indices[0])): 
			idx = idcolonne
			if indices[idligne][idcolonne] == "0":
				affichage_un_indice(idx, idy, 'blue')
			else:
				affichage_un_indice(idx, idy, 'black')


def affichage_un_indice(idx, idy, color):
	"""Affiche l'indice idx idy de la couleur color
	"""
	x, y = (taille_marge + idx * taille_case + int(taille_case/3), taille_marge + idy * taille_case + int(taille_case/5))
	idligne = idy
	idcolonne = idx
	chaine = indices[idligne ][idcolonne]
	texte(x, y, chaine, couleur= color, ancrage='nw', police='Helvetica', taille=int(taille_case/4), tag='')


def obtenir_segment(evt_x, evt_y):
	"""Verifie si le clic tombe sur le segment et retourne seg (tuple) le segment où a eu lieu le clic
	:param evt_x: abcisse du clic
	:param evt_y: ordonnée du clic
	"""
	#calcul l'indice du sommet
	idx = round((evt_x - taille_marge) / taille_case)
	idy = round((evt_y - taille_marge) / taille_case)
	
	#calcul coords premier sommet
	sommet_x = idx * taille_case + taille_marge
	sommet_y = idy * taille_case + taille_marge
	
	if (sommet_x - ecart) < evt_x and evt_x < (sommet_x + ecart): #horizontal
		if sommet_y < evt_y:
			seg = ((idx, idy), (idx, idy+1))
		else:
			seg = ((idx, idy), (idx, idy-1))
	elif (sommet_y - ecart) < evt_y and evt_y < (sommet_y + ecart): #vertical
		if sommet_x < evt_x:
			seg = ((idx, idy), (idx+1, idy))
		else:
			seg = ((idx, idy), (idx-1, idy))
	else:
		seg = None
	return seg

def obtenir_tag(segment):
	"""Renvoie le tag 
	"""
	x1, y1 = segment[0]
	x2, y2 = segment[1] 
	tag = str(x1) + "_" + str(y1) + "_" + str(x2) + "_" + str(y2)
	return tag

def dessiner(segment, type_trace):
	"""
	- Trace un segment si type_trace = 1
	- Trace une croix si type_trace = -1
	"""
	x1, y1 = segment[0]
	x2, y2 = segment[1] 
	coord_sommet1 = (taille_marge + x1 * taille_case, taille_marge + y1 * taille_case)
	coord_sommet2 = (taille_marge + x2 * taille_case, taille_marge + y2 * taille_case)
	my_tag = obtenir_tag(segment)
	if type_trace == 1: #trace un segment
		ligne(coord_sommet1[0], coord_sommet1[1], coord_sommet2[0], coord_sommet2[1], couleur='black', epaisseur=3, tag=my_tag)
	else: #trace une croix
		if x1 == x2: #cas meme abcisse
			milieu = (coord_sommet1[1] + coord_sommet2[1]) / 2
			coord_milieu = (coord_sommet1[0], milieu)
		else: #cas meme ordonne
			milieu = (coord_sommet1[0] + coord_sommet2[0]) / 2
			coord_milieu = (milieu, coord_sommet1[1])
		a1, a2 = (coord_milieu[0] - ecart/2, coord_milieu[1] - ecart/2), (coord_milieu[0] + ecart/2, coord_milieu[1] - ecart/2)
		b1, b2 = (coord_milieu[0] + ecart/2, coord_milieu[1] + ecart/2), (coord_milieu[0] - ecart/2, coord_milieu[1] + ecart/2)
		ligne(a1[0], a1[1], b1[0], b1[1], couleur='red', epaisseur=3, tag=my_tag)
		ligne(b2[0], b2[1], a2[0], a2[1], couleur='red', epaisseur=3, tag=my_tag)


# ======================================================================
# ==================== Tache 4: Recherche de solutions =================
# ======================================================================

def solveur(etat, sommet):
	"""Vérifie si le jeu admet une solution
	:param etat: dictionnaire
	:param sommet: tuple (coordonnees), sommet de départ 
	"""
	lst1 = segments_traces(etat, sommet) #liste des segments tracés adjacents à sommet
	condition_indices, booleen_rouge = indices_satisfaits()
	
	if len(lst1) == 2: #sommet adjacent à deux segments tracés dans etat
		if condition_indices == True:
 			return True
		else:
 			return False
		
	if len(lst1) > 2: #sommet adjacent à plus de deux segments tracés dans etat
		return False

	lst2 = segments_adjacents(etat, sommet) #les 4 segments adjacents a sommet

	for seg in lst2:
		if seg not in lst1: #chacun des autres segments adjacents à sommet
			tracer_segment(etat, seg)
			condition_indices, booleen_rouge = indices_satisfaits()
			if booleen_rouge == True: #dépasse le nombre de segments autorisés 
				effacer_segment(etat, seg)
				continue
			else: #satisfait 
				sommet2 = seg[1]
				if sommet == sommet2:
					sommet2 = seg[0]
				resultat = solveur(etat, sommet2) #donc appel sur le suivant
				if resultat == True:
					return True
				else:
					effacer_segment(etat, seg)

	return False

def test_solveur():
	"""test pour le solveur
	"""
	for idligne in range(nb_sommet_verticales):
			for idcolonne in range(nb_sommet_verticales):
				sommet = (idligne, idcolonne)
				print("GAME SOLVEUR sommet:", sommet)
				solution = solveur(etat, sommet)
				if solution == True:
					return 
	return False

###### PROGRAMME PRINCIPAL

### INITIALISATION ###
indices = charger_grille() #liste de listes sur les indices de la grille
etat = {} #dictionnaire représentant l'état de la grille
jeu = True
compteur_global = 0 #nombre total de segments tracés
taille_case = 100
taille_marge = taille_case / 2
nb_sommet_horizontales = len(indices[0]) + 1
nb_sommet_verticales = len(indices) + 1
largeur_plateau = taille_marge * 1/2 + taille_case * nb_sommet_horizontales  # largeur de la fenêtre
hauteur_plateau = taille_marge * 2 + taille_case * nb_sommet_verticales  # hauteur de la fenêtre
ecart = 20


### TEST ###
#print(testmod())


### AFFICHAGE #####
cree_fenetre(largeur_plateau, hauteur_plateau)
lst_coords_sommets = coords_sommets()
init_affichage_indices(indices)

# bouton quitter
quitter_x1, quitter_x2 = largeur_plateau - taille_case, largeur_plateau - 10
quitter_y1, quitter_y2 =  hauteur_plateau - taille_case/2, hauteur_plateau - 10
rectangle(quitter_x1, quitter_y1, quitter_x2, quitter_y2, couleur='black', remplissage='black', epaisseur=1, tag='')
texte(quitter_x1, quitter_y1 + 5, "Quitter", couleur='white', ancrage='nw', police='Helvetica', taille=10, tag='')

#bouton solveur
solveur_x1, solveur_x2 =  10, taille_case
solveur_y1, solveur_y2 =  hauteur_plateau - taille_case/2, hauteur_plateau - 10
rectangle(solveur_x1, solveur_y1, solveur_x2, solveur_y2, couleur='black', remplissage='black', epaisseur=1, tag='')
texte(solveur_x1, solveur_y1 + 5, "Solveur", couleur='white', ancrage='nw', police='Helvetica', taille=10, tag='')

while jeu:
	evt = attend_ev()
	evt_type = type_ev(evt) #clic droit ou clic gauche
	evt_x, evt_y = abscisse(evt), ordonnee(evt) #coordonées du clic
	segment = obtenir_segment(evt_x, evt_y) 
	zone_jeu = True

	x_zonejeu = taille_marge + taille_case * len(indices[0]) + ecart
	y_zonejeu = taille_marge + taille_case * len(indices) + ecart

	 # verification si clique n'est pas dans la zone de jeu
	if evt_x < taille_marge - ecart or evt_x > x_zonejeu or \
		evt_y < taille_marge - ecart or evt_y > y_zonejeu:
		zone_jeu = False

	#bouton quitter
	if quitter_x1 <= evt_x <= quitter_x2 and quitter_y1 <= evt_y <= quitter_y2:
		jeu = False

	#bouton solveur
	if solveur_x1 <= evt_x <= solveur_x2 and solveur_y1 <= evt_y <= solveur_y2:
		solution_jeu = test_solveur()
		if solution_jeu == False:
			print("il n'y a pas de solution")
		evt = attend_ev()
		jeu = False


	#clic pour segment 
	if segment != None and zone_jeu:
		if evt_type == 'ClicGauche': 
			seg_vierge = est_vierge(etat, segment)
			if seg_vierge == True:
				tracer_segment(etat, segment)
			else:
				if est_trace(etat, segment) == True:
					effacer_segment(etat, segment)
				else:
					effacer_segment(etat, segment)
					tracer_segment(etat, segment)
			
		elif evt_type == 'ClicDroit':
			seg_vierge = est_vierge(etat, segment)
			if seg_vierge == True:
				interdire_segment(etat, segment)
			else:
				if est_interdit(etat, segment) == True:
					effacer_segment(etat, segment)
				else:
					effacer_segment(etat, segment)
					interdire_segment(etat, segment)

		#print("JEU: segment:", segment)
	else:
		continue

	#1ere condition de victoire (indices satisfaits)
	condition_indices, booleen_rouge = indices_satisfaits()
	#print("bool rouge:", booleen_rouge)
	#print("condition_indices:", condition_indices)
	if condition_indices == False:
		print("Indices non satisfaits")
	else:
		print("Indices tous satisfaits!")
		
	#2eme condition de victoire (forme une seule et unique boucle fermée)
	cpmt = longueur_boucle(etat, segment)
	#print("cpmt:", cpmt, "  compteur_global:", compteur_global)
	if cpmt == compteur_global:
		print("forme une boucle")
		if condition_indices == True:
			print("FELICIATIONS VOUS AVEZ GAGNE")
			attend_clic_gauche()
			jeu = False
	else:
		print("ne forme pas une boucle unique")
		#print("cpmt:", cpmt, ", compteur_global:", compteur_global)

ferme_fenetre()
