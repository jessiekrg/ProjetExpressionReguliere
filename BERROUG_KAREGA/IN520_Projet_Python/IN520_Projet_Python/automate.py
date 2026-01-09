import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""
    
    #je déclare l'automate 
    a = automate() 
    a.n = a1.n + a2.n
    a.final = []

    for etat_final in a2.final :
        a.final.append(etat_final +  a1.n)

    for (etat,lettre), destination in a1.transition.items():
        a.ajoute_transition(etat,lettre,destination) 
    
    for etat_final_a1 in a1.final:
        a.ajoute_transition(etat_final_a1,"E", [a1.n] ) #avec le décalage [a1.n] correspond à l'etat initial de a2

    for (etat,lettre), destination in a2.transition.items():
        etat_decale = etat + a1.n

        destination_decale = []
        for d in destination:
            destination_decale.append(d + a1.n)
        
        a.ajoute_transition(etat_decale,lettre,destination_decale) 

    return a


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 

    a = automate()
    a.n = a1.n + a2.n
    a.final = []

    # on crée un nouvel état initial en 0 = tous les anciens états sont décalés de +1.

    for etat_final in a1.final :
        a.final.append(etat_final + 1)

    for etat_final in a2.final :
        a.final.append(etat_final + 1 + a1.n) # on décale la numérotation des états final de a2

    # ε-transitions depuis le nouvel état initial
    a.ajoute_transition(0, "E", [1])
    a.ajoute_transition(0, "E", [1 + a1.n])

    for (etat,lettre), destination in a1.transition.items():
        etat = etat + 1

        destination_decale = []
        for d in destination:
            destination_decale.append(d + 1)

        a.ajoute_transition(etat,lettre,destination) 
    
    for (etat,lettre), destination in a2.transition.items():
        etat_decale = etat + a1.n

        destination_decale = []
        for d in destination:
            destination_decale.append(d + a1.n)
        
        a.ajoute_transition(etat_decale,lettre,destination_decale) 
    
    return a


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 

    a1 = automate()

    #j'ajoute le nouvel etat initial et un nouveau etat final en rallongeant le le nb d'etats 
    a1.n = a.n + 2

    a1.final = [a1.n - 1] #dernier etat c'est l'etat final ici 

    #je decale tous les etats de 1 ducoup pour l'ajout de l'etat initial et ensuite je dois decaler les transition 
    for (etat,lettre), destination in a.transition.items():

        etat_a1 = etat + 1

        dest_a1 = []
        for d in destination:
            dest_a1.append(d+1)

        a1.ajoute_transition(etat_a1, lettre , dest_a1)

    #j'ajoute la transition epsilion de l'état initial qui vers l'etat fi de a et trans e du nouvel etat initial vers etat f
    a1.ajoute_transition(0,"E", a1.final )
    a1.ajoute_transition(0,"E", [1] ) #ici

    for etat_final_a in a.final:
        af = etat_final_a + 1
        a1.ajoute_transition(af, "E", a1.final)
        a1.ajoute_transition(af, "E", [1]) #pas 0 parce sinon on peut boucler infinement sur des transion epsilon pass ouf quoi 


    return a1 #je crois pas que je dois retourner le meme  a du coup j'ai changé en a1 but idk 


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        


def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """
    a_E = supression_epsilon_transitions(a)
    a_det = automate()
    a_traiter = [frozenset({0})]  # utiliser frozenset pour pouvoir comparer et stocker
    etats_vus = {frozenset({0})}

    while a_traiter:
        etat = a_traiter.pop(0)
        S_a = set()  #ensemble des états atteignables avec 'a'
        S_b = set()  # on utilise des set pour ne pas avoir des doublon 
        S_c = set() 
        for (q,lettre), destination in a_E.transition.items():
            if q in etat: # Un etat peut être composé de plusieurs état
                if lettre == 'a':
                    S_a.update(destination) # on .update et pas .add cardestination est une liste
                if lettre == 'b':
                    S_b.update(destination)
                if lettre == 'c':
                    S_c.update(destination)
        # Ajout des transitions
        a_det.ajoute_transition(etat,'a',list(S_a)) #la focntion attend à ce que dest doit une liste
        a_det.ajoute_transition(etat,'b',list(S_b)) 
        a_det.ajoute_transition(etat,'c',list(S_c)) 

        # Rajouter les nouveaux ensemble dans a_traiter
        for nouvel_etat in [S_a, S_b, S_c]:
            if nouvel_etat and frozenset(nouvel_etat) not in etats_vus:
                etats_vus.add(frozenset(nouvel_etat))
                a_traiter.append(frozenset(nouvel_etat))
        
    # Definir état finaux          
    a_det.final =[]
    for etat in etats_vus:
        if any(q in a_E.final for q in etat): # any renvoie TRUE si on moins un des q est final
            a_det.final.append(etat)
    
    return a_det

    # prof a mis return a  idk 




    
    
def completion(a):  #j'attends que tu fais pour faire lui je pense idk
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    
    #copie de l'automate a + ajout de l'etat poubelle
    a1 = automate()
    a1.n = a.n
    a1.final = a.final
    la_poubelle = a.n #a.n c'est juste la valeur du prochain etat dispo si la poubelle est necessaire 

    #copie des transitions d'origine 
    for (etat, lettre), destination in a.transition.items() :
        a1.ajoute_transition(etat, lettre , destination)

    for etat in range(a1.n):
        for lettre in a1.alphabet:
            if (etat,lettre) not in a1.transition:
                a1.ajoute_transition(etat,lettre, [la_poubelle])
    
    if [la_poubelle] in a1.transition.values():
        a1.n = a1.n + 1 #ajout de l'etat poubelle si il est utilisé au moins 
        for lettre in a1.alphabet:
            a1.ajoute_transition(la_poubelle, lettre, [la_poubelle])

    #pour tous les etats , pour chaquqe symbole de a1  si une transition manque on ajoute une transition vers un etat poubelle


    return a1


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part    
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    a1_min = minimisation(a1)
    a2_min = minimisation(a2)

    # Cas de base
    if a1_min.n != a2_min.n: 
        return False
    if set(a1_min.final) != set(a2_min.final): # set pour que l'odre n'a plus d'importance
        return False
    
    e_1 = a1_min.initial
    e_2 = a2_min.initial

    a_traiter = [(e_1,e_2)]
    etats_vus = []
    while a_traiter:
        (q1,q2) =  a_traiter.pop(0)
        if q1 in a1_min.final and q2 not in a2_min.final:
            return False
        if q2 in a2_min.final and q1 not in a1_min.final:
            return False
        
        for lettre in ['a','b','c']:
            dest1 = a1_min.transition.get((q1, lettre), [])
            dest2 = a2_min.transition.get((q2, lettre), [])
            
            if len(dest1) != len(dest2):
                return False
        
            for s1, s2 in zip(dest1, dest2): #premier état du dest1 correspond au premier du dest2
                if (s1,s2) not in etats_vus:
                    etats_vus.append((s1,s2))
                    a_traiter.append((s1,s2))

    return True



# TESTS
# à écrire
# --- TEST RAPIDE ---
if __name__ == "__main__":

# Automates
    a = automate("a")
    b = automate("b")
    epsilon = automate("E")

# Test : Concaténation (a.b) 
    t1 = concatenation(a, b)
    t2 = concatenation(a, epsilon)


    t3 = supression_epsilon_transitions(t2)
    #print(t1,t2,t3)


# Test : Etoile

    e1 = etoile(a)                 
    e2 = etoile(epsilon)           
    e3 = etoile(union(a, b))
    #print(e1,e2,e3)

# Test : Completion  

    c1 = completion(b)  
    print(b,c1)

    

# Test : Union (a|b)
    


# Test : Suppression des Epsilon 
# Test : Déterminisation 
