#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # ATTENTION: test_tp modifie la valeur de END

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

############
# Question 0: 
#récupération des fichiers source

############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    '''
    vérifie si le caractère est un chiffre non nul et que
    la longueur de la chaîne est inférieure à 1
    '''
    assert (len(char) <= 1)
    # RMQ: on n'utilise pas 1 <= int(char) <= 9 car cela échoue sur la chaîne vide
    return '1' <= char <= '9'

def digit(char):
    '''
    vérifie si le caractère est un chiffre, et que 
    la longueur de la chaîne est inférieure à 1
    '''
    assert (len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur

#integer
def integer_Q2():
    init_char()
    return integer_Q2_state_0()

def integer_Q2_state_0():
    '''
    q0
    '''
    ch = next_char()
    if nonzerodigit(ch):
        return integer_Q2_state_2()
    elif ch == '0':
        return integer_Q2_state_1()
    else:
        return False

def integer_Q2_state_1():
    '''
    q1
    '''
    ch = next_char()
    if digit(ch) and not(nonzerodigit(ch)):
        #on a un 0
        return integer_Q2_state_1()
    elif ch == END:
        return True
    else: 
        return False

def integer_Q2_state_2():
    '''
    q2
    '''
    ch = next_char()
    if digit(ch):
        return integer_Q2_state_2()
    elif ch == END:
        return True
    else: 
        return False

#pointfloat
def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

def pointfloat_Q2_state_0():
    '''
    q0
    '''
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch == '.':
        return pointfloat_Q2_state_1()
    else: 
        return False

def pointfloat_Q2_state_1():
    '''
    q1
    '''
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    else: 
        return False

def pointfloat_Q2_state_2():
    '''
    q2
    '''
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch == '.':
        return pointfloat_Q2_state_3()
    else: 
        return False
    
def pointfloat_Q2_state_3():
    '''
    q3
    '''
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    elif ch == END: 
        return True
    else:
        return False

############
# Question 3 : 
#tests ok pour integer et pointfloat sans valeur

############
# Question 4 : 
#L'idée est de multiplier la valeur par 10 et d'ajouter la valeur du chiffre rencontré


############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0

def integer():
    global int_value
    int_value = 0
    init_char()
    return integer_state_0()

def integer_state_0():
    global int_value
    ch = next_char()
    if nonzerodigit(ch):
        # on a un chiffre non nul
        int_value = int(ch)
        return integer_state_2()
    elif digit(ch) and not(nonzerodigit(ch)):
        # on a un 0
        return integer_state_1()
    else:
        return False, None

def integer_state_1():
    global int_value
    ch = next_char()
    if digit(ch) and not(nonzerodigit(ch)):
        # on a un 0
        return integer_state_1()
    elif ch == END:
        return True, int_value
    else:
        return False, None

def integer_state_2():
    global int_value
    ch = next_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return integer_state_2()
    elif ch == END:
        return True, int_value
    else:
        return False, None

############
# Question 6 : 
#tests ok pour integer avec valeur


############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0.
    exp_value = 0
    return pointfloat_state_0()


def pointfloat_state_0():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        # on a un chiffre non nul
        int_value = int(ch)
        return pointfloat_state_2()
    elif ch == '.':
        # on a un une virgule (donc un zero virtuel)
        exp_value = -1
        return pointfloat_state_1()
    else:
        return False, None
    
def pointfloat_state_1():
    '''
    q1: cas ou on a déjà recontré une virgule
    '''
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value += int(ch) * 10 ** exp_value
        exp_value -= 1
        return pointfloat_state_3()
    else:
        return False, None

def pointfloat_state_2():
    '''
    q2: cas où on a déjà recontré un entier
    '''
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return pointfloat_state_2()
    elif ch == '.':
        exp_value = -1
        return pointfloat_state_3()
    else:
        return False, None

def pointfloat_state_3():
    '''
    q3: on a forcément rencontré un chiffre après la virgule, 
    ou juste une virgule
    '''
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value += int(ch) * 10 ** exp_value
        exp_value -= 1
        return pointfloat_state_3()
    elif ch == END:
        return True, int_value
    else:
        return False, None


############
# Question 8 : exponent, exponentfloat et number


#EXPONENT
#il faut tout d'abord écrire l'automate sur une feuille de papier, 
#puis le rendre déterministe et complet, et enfin l'implémenter

    
# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value = 0

def exponent():
    '''
    automate pour les exposants
    '''
    init_char()
    global exp_value
    global sign_value
    sign_value = 1
    exp_value = 0
    return exponent_state_0()

def exponent_state_0():
    ch = next_char()
    if ch == 'e' or ch == 'E':
        return exponent_state_1()
    else:
        return sink_state()

def exponent_state_1():
    global sign_value
    global exp_value
    ch = next_char()
    if ch == '+':
        sign_value = 1
        return exponent_state_2()
    elif ch == '-':
        sign_value = -1
        return exponent_state_2()
    elif digit(ch):
        exp_value = int(ch)
        return exponent_state_3()
    else:
        return sink_state()

def exponent_state_2():
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = sign_value * int(ch)
        return exponent_state_3()
    else:
        return sink_state()

def exponent_state_3():
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = exp_value * 10 + sign_value * int(ch)
        return exponent_state_3()
    elif ch == END:
        return True, exp_value
    else:
        return sink_state()

def sink_state():
    '''
    Etat puits commun à tous les automates
    '''
    return False, None

#EXPONENT FLOAT
#il faut tout d'abord écrire l'automate sur une feuille de papier,
#puis le rendre déterministe et complet, et enfin l'implémenter

def exponentfloat():
    '''
    automate pour les nombres à virgule avec exposants
    '''
    init_char()
    global int_value
    global exp_value
    global sign_value
    sign_value = 1
    int_value = 0.
    exp_value = 0
    return exponentfloat_state_0()

def exponentfloat_state_0():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int(ch)
        return exponentfloat_state_1()
    elif ch == '.':
        exp_value = -1
        return exponentfloat_state_2()
    else:
        return sink_state()
    
def exponentfloat_state_1():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return exponentfloat_state_1()
    elif ch == '.':
        exp_value =- 1
        return exponentfloat_state_4()
    elif ch == 'e' or ch == 'E':
        exp_value = 0
        return exponentfloat_state_3()
    else:
        return sink_state()

def exponentfloat_state_2():
    global int_value
    global exp_value 
    ch = next_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        return exponentfloat_state_4()
    else:
        return sink_state()

def exponentfloat_state_3():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if ch == '+':
        sign_value = 1
        return exponentfloat_state_5()
    elif ch == '-':
        sign_value = -1
        return exponentfloat_state_5()
    elif digit(ch):
        exp_value = int(ch)
        return exponentfloat_state_6()
    else:
        return sink_state()

def exponentfloat_state_4():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        return exponentfloat_state_4()
    elif ch == 'e' or ch == 'E':
        exp_value = 0
        return exponentfloat_state_3()
    elif ch == END:
        return True, int_value
    else:
        return sink_state()

def exponentfloat_state_5():
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = sign_value * int(ch)
        return exponentfloat_state_6()
    else:
        return sink_state()

def exponentfloat_state_6():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        exp_value = exp_value * 10 + sign_value * int(ch)
        return exponentfloat_state_6()
    elif ch == END:
        return True, int_value * 10 ** exp_value
    else:
        return sink_state()

#NUMBER
def number():
    '''
    automate pour tous les nombres
    '''
    init_char()
    global int_value
    global exp_value
    global sign_value
    sign_value = 1
    int_value = 0.
    exp_value = 0
    return number_state_0()

def number_state_0():
    '''
    q0 Number
    '''
    global int_value 
    global exp_value
    ch = next_char()
    if nonzerodigit(ch):
        int_value = int(ch)
        return number_state_2()
    elif ch == '0':
        int_value = 0
        return number_state_1()
    elif ch == '.':
        exp_value = -1
        return number_state_3()
    else: 
        return sink_state()

def number_state_1():
    '''
    q1 Number
    '''
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if nonzerodigit(ch):
        int_value = int(ch)
        return number_state_5()
    elif ch == '0':
        return number_state_1()
    elif ch == '.':
        exp_value = -1
        return number_state_4()
    elif ch == 'E' or ch == 'e':
        exp_value = 0
        sign_value = 1
        return number_state_6()
    elif ch == END or ch == ' ':
        return True, int_value 
    else: 
        return sink_state()

def number_state_2(): 
    '''
    q2 Number
    '''
    global int_value 
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        int_value = int_value * 10 +int(ch)
        return number_state_2()
    elif ch == '.':
        exp_value = -1
        return number_state_4()
    elif ch == 'E' or ch == 'e':
        exp_value = 0
        sign_value = 1
        return number_state_6()
    elif ch == END or ch == ' ':
        return True, int_value 
    else:
        return sink_state()

def number_state_3():
    '''
    q3 Number
    '''
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        return number_state_4()
    else: 
        return sink_state()

def number_state_4():
    '''
    q4 Number
    '''
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        return number_state_4()
    elif ch == 'E' or ch=='e':
        exp_value = 0
        sign_value = 1
        return number_state_6()
    elif ch == END or ch == ' ':
        return True, int_value
    else: 
        return sink_state

def number_state_5():
    '''
    q5 Number
    '''
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return number_state_5()
    elif ch == '.':
        exp_value = -1
        return number_state_4()
    elif ch == 'E' or ch == "e":
        exp_value = 0
        return number_state_6()
    else:
        return sink_state()

def number_state_6():
    '''
    q6 Number
    '''
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = int(ch)
        return number_state_8()
    elif ch == '+':
        sign_value = 1
        return number_state_7()
    elif ch == '-':
        sign_value = -1
        return number_state_7()
    else:
        return sink_state()

def number_state_7():
    '''
    q7 Number
    '''
    global exp_value
    ch = next_char()
    if digit(ch):
        exp_value = sign_value * int(ch)
        return number_state_8()
    else:
        return sink_state()

def number_state_8():
    '''
    q8 Number
    '''
    global exp_value
    global int_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = exp_value * 10 + sign_value * int(ch)
        return number_state_8()
    elif ch == END or ch == ' ':
        return True, int_value * 10 ** exp_value
    else:
        return sink_state()

########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))

############
# Question 9 : 
# Langage hors contexte car les règles sont de la forme A -> aBc, avec A et B des 
# symboles non terminaux et a, c des symboles terminaux
# Langage régulier ? A DEMONTRER



############
# Question 10 : eval_exp

def eval_exp():
    '''
    évaluer une expression en notation préfixe
    '''
    ch = next_char()

    #cas récursifs
    if ch == '-': 
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 - n2
    
    elif ch == '*':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 * n2
    
    elif ch == '/':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 / n2
    
    elif ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2    
    else: 
        return number()[1]


############
# Question 11: 
# TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
# l'espace entre '+' et '11' est interprété comme un mot

# Après ajout de "ch == ' '" dans l'automate number, le programme fonctionne
# mais le résultat n'est pas le bon (15 pour + 12 13, ne fonctionne pas quand le
# second terme n'a qu'un seul chiffre)
# EXPLICATIONS: le programme ne prend pas en compte les espaces, il interpète
# le premier 1 de 13 comme étant vide (consommé dans le else) et le second comme 
# étant un chiffre sur le 12 cela ne pose pas de problème car il y a un espace 
# entre + et 12

############
# Question 12 : eval_exp corrigé
# Il faut que l'espace après un nombre ne soit pas consommé, ce qui permet à
# eval_exp de le consommer dans le else

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''


def number_v2():
    '''
    automate pour tous les nombres
    qui implémente les corrections mentionnées précédemment
    si on accepte le mot avec un espace, on ne consomme pas 
    le caractère de fin du mot
    '''
    init_char()
    global int_value
    global exp_value
    global sign_value
    sign_value = 1
    int_value = 0.
    exp_value = 0
    return number_state_0_v2()

def number_state_0_v2():
    '''
    q0 Number
    '''
    global int_value 
    global exp_value
    ch = peek_char()
    consume_char()
    if nonzerodigit(ch):
        int_value = int(ch)
        return number_state_2_v2()
    elif ch == '0':
        int_value = 0
        return number_state_1_v2()
    elif ch == '.':
        exp_value = -1
        return number_state_3_v2()
    else: 
        return sink_state()

def number_state_1_v2():
    '''
    q1 Number
    '''
    global int_value
    global exp_value
    global sign_value
    ch = peek_char()
    if nonzerodigit(ch):
        int_value = int(ch)
        consume_char()
        return number_state_5_v2()
    elif ch == '0':
        consume_char()
        return number_state_1_v2()
    elif ch == '.':
        exp_value = -1
        consume_char()
        return number_state_4_v2()
    elif ch == 'E' or ch == 'e':
        exp_value = 0
        sign_value = 1
        consume_char()
        return number_state_6_v2()
    elif ch == ' ':
        return True, int_value 
    elif ch == END: 
        consume_char()
        return True, int_value 
    else: 
        consume_char()
        return sink_state()

def number_state_2_v2(): 
    '''
    q2 Number
    '''
    global int_value 
    global exp_value
    global sign_value
    ch = peek_char()
    if digit(ch):
        int_value = int_value * 10 +int(ch)
        consume_char()
        return number_state_2_v2()
    elif ch == '.':
        exp_value = -1
        consume_char()
        return number_state_4_v2()
    elif ch == 'E' or ch == 'e':
        exp_value = 0
        sign_value = 1
        consume_char()
        return number_state_6_v2()
    elif ch == ' ':
        return True, int_value 
    elif ch == END: 
        consume_char()
        return True, int_value 
    else:
        consume_char()
        return sink_state()

def number_state_3_v2():
    '''
    q3 Number
    '''
    global int_value
    global exp_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        return number_state_4_v2()
    else: 
        return sink_state()

def number_state_4_v2():
    '''
    q4 Number
    '''
    global int_value
    global exp_value
    global sign_value
    ch = peek_char()
    if digit(ch):
        int_value = int_value + int(ch) * 10 ** exp_value
        exp_value -= 1
        consume_char()
        return number_state_4_v2()
    elif ch == 'E' or ch=='e':
        exp_value = 0
        sign_value = 1
        consume_char()
        return number_state_6_v2()
    elif ch == ' ':
        return True, int_value 
    elif ch == END: 
        consume_char()
        return True, int_value 
    else: 
        consume_char()
        return sink_state()

def number_state_5_v2():
    '''
    q5 Number
    '''
    global int_value
    global exp_value
    ch = peek_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        consume_char()
        return number_state_5_v2()
    elif ch == '.':
        exp_value = -1
        consume_char()
        return number_state_4_v2()
    elif ch == 'E' or ch == "e":
        exp_value = 0
        consume_char()
        return number_state_6_v2()
    else:
        consume_char()
        return sink_state()

def number_state_6_v2():
    '''
    q6 Number
    '''
    global exp_value
    global sign_value
    ch = peek_char()
    if digit(ch):
        exp_value = int(ch)
        consume_char()
        return number_state_8_v2()
    elif ch == '+':
        sign_value = 1
        consume_char()
        return number_state_7_v2()
    elif ch == '-':
        sign_value = -1
        consume_char()
        return number_state_7_v2()
    else:
        consume_char()
        return sink_state()

def number_state_7_v2():
    '''
    q7 Number
    '''
    global exp_value
    ch = peek_char()
    if digit(ch):
        exp_value = sign_value * int(ch)
        consume_char()
        return number_state_8_v2()
    else:
        consume_char()
        return sink_state()

def number_state_8_v2():
    '''
    q8 Number
    '''
    global exp_value
    global int_value
    global sign_value
    ch = peek_char()
    if digit(ch):
        exp_value = exp_value * 10 + sign_value * int(ch)
        consume_char()
        return number_state_8_v2()
    elif ch == ' ':
        return True, int_value 
    elif ch == END: 
        consume_char()
        return True, int_value * 10 ** exp_value 
    else:
        consume_char()
        return sink_state()


def eval_exp_v2():
    '''
    évaluer une expression en notation préfixe
    '''
    ch = peek_char()
    #cas récursifs
    if ch == '-': 
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        print(n1, n2)
        return n1 - n2
    
    elif ch == '*':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        print(n1, n2)
        return n1 * n2
    
    elif ch == '/':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        print(n1, n2)

        return n1 / n2
    
    elif ch == '+':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        print(n1, n2)
        return n1 + n2

    #cas de base: espace
    elif ch == ' ':
        consume_char()
        prochain_ch = peek_char()
        if digit(prochain_ch) or prochain_ch == '.': 
            return number_v2()[1]
        elif prochain_ch in operator:
            return eval_exp_v2()
        else: 
            raise ValueError('Expression incorrecte')
    
    else: 
        raise ValueError('Expression incorrecte')



############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    print("@ATTENTION: FA_lex à finir !") # LIGNE A SUPPRIMER


############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0



def FA_Lex_w_token():
    print("@ATTENTION: FA_lex_w_token à finir !") # LIGNE A SUPPRIMER



# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        #ok = integer() # changer ici pour tester un autre automate sans valeur
        # ok, val = number_v2() # changer ici pour tester un autre automate avec valeur
        ok, val = True, eval_exp_v2() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
