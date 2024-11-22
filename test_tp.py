#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test des fonctions du TP
"""

import io
import tp
import math

# Prints each test
verbose_test = True

# Stop testing on the first encountered error
stop_on_first_error = False

# Quelles fonctions doivent être testées: True si on teste, False sinon

test_integer_Q2    = False
test_pointfloat_Q2 = False
test_integer       = False
test_pointfloat    = False
test_exponent      = False
test_exponentfloat = False
test_number        = True

# Le caractère de fin est \0, et non \n
tp.END = ''


# DRIVERS de tests avec et sans valeur calculée

def test(input_descr, expr, msg):
    """Perform a test.
       Raise an exception of it fails and stop_on_first_error == True"""
    if stop_on_first_error:
        assert expr, msg
    else:
        if not expr:
            if verbose_test:
                print(input_descr)
            print(msg)
    return

def test_single_wo_val(function_to_test, expected_result, test_input):
    """function_to_test = name of the function to test
       expected_result = True or False or None (where None means tp.Error expected)
       test_input = string in input"""
    input_descr = "@ " + repr(function_to_test) + " on " + repr(test_input) + " expect: " + repr(expected_result)
    if verbose_test:
        print(input_descr)
    tp.INPUT_STREAM = io.StringIO(test_input)
    try:
        found_result = eval(function_to_test+"()")
        test(input_descr, expected_result != None, "an exception is expected instead of normally return " + repr(found_result))
        test(input_descr, expected_result == found_result, "found " + repr(found_result))
    except tp.Error as e:
        test(input_descr, expected_result == None, "unexpected " + repr(e))
    except TypeError as e:
        if not stop_on_first_error:
            print("Type error for " + repr(function_to_test)+"("+test_input+"): " + repr(e))
        else:
            raise e from None
    except Exception as exn:
        if not stop_on_first_error:
            print(input_descr)
            print("ERROR: uncaught exception " + repr(exn))
        else:
            raise exn from None

def test_all_wo_val(function_to_test, expected_result, test_inputs):
    for i in test_inputs:
        tp.consume_char() # resets current_char
        test_single_wo_val(function_to_test, expected_result, i)
    print("@---- ", function_to_test, "=>", expected_result, " PASSED!")
    print()

def test_single(function_to_test, expected_result, test_input):
    """function_to_test = name of the function to test
       expected_result = True or False or None (where None means tp.Error expected)
       test_input = string in input"""
    input_descr = "@ " + repr(function_to_test) + " on " + repr(test_input) + " expect: " +  repr(expected_result)
    if verbose_test:
        print(input_descr)
    if expected_result:
        if function_to_test == "tp.exponent":
            actual_input = float(test_input[1:])
        else:
            actual_input = float(test_input)
        assert math.isfinite(actual_input),\
            ("please remove this irrelevant test ('{0}' is float '{1}' which is not finite)".format(test_input, actual_input))
    tp.INPUT_STREAM = io.StringIO(test_input)
    try:
        ok, result = eval(function_to_test+"()")
        test(input_descr,
             expected_result != None,
             "an exception is expected instead of normally return " + repr((ok, result)))
        if expected_result:
            test(input_descr,
                 ok==True and float(result) == actual_input,
                 "found " + repr((ok, result)))
        else:
            test(input_descr,
                 (not ok) and result == None,
                 "found " + repr((ok, result)))
    except tp.Error as e:
        test(input_descr, expected_result == None, "unexpected " + repr(e))
    except TypeError as e:
        if not stop_on_first_error:
            print("Type error for " + repr(function_to_test)+"("+test_input+"): " + repr(e))
        else:
            raise e from None
    except Exception as exn:
        if not stop_on_first_error:
            print(input_descr)
            print("ERROR: uncaught exception " + repr(exn))
        else:
            raise exn from None

def test_all(function_to_test, expected_result, test_inputs):
    for i in test_inputs:
        tp.consume_char() # resets current_char
        test_single(function_to_test, expected_result, i)
    print("@---- ", function_to_test, "=>", expected_result, " PASSED!")
    print()



# Les tests proprement dits.

# D'abord, sans valeurs
def exec_test_integer_Q2():
    test_all_wo_val("tp.integer_Q2", True, 
                    ["1234567890098700", "203", "0000", 
                     "0", "1","2","3","4","5","6","7","8","9"])
    test_all_wo_val("tp.integer_Q2", False, 
                    ["01","","123e","000e","2.5",".5","0.0","3.", "1e5", "2e+5", "1e-5", "-25"])
    test_all_wo_val("tp.integer_Q2", None, ["a2","0a0","1a0"])

def exec_test_pointfloat_Q2():
    test_all_wo_val("tp.pointfloat_Q2", True, 
                    ["4.", "5.4", ".5", "0123.", ".123", "678.876", 
                     "0.", "000.000", ".0"])
    test_all_wo_val("tp.pointfloat_Q2", False, 
                    ["123", "0", "1", ".", ".123e5", "1.e+5", "2e5", "1.5e+6", "",
                     "-.5"])
    test_all_wo_val("tp.pointfloat_Q2", None, ["1.a2","0.a0","1a."])

# Ensuite, avec valeurs
def exec_test_integer():
    test_all("tp.integer", True, 
             ["1234567890098700", "203", "0000", 
              "0", "1","2","3","4","5","6","7","8","9"])
    test_all("tp.integer", False, 
             ["01","","123e","000e","2.5",".5","0.0","3.", "1e5", "2e+5", "1e-5", "-25"])
    test_all("tp.integer", None, ["a2","0a0","1a0"])

def exec_test_pointfloat():
    test_all("tp.pointfloat", True, 
             ["4.", "5.4", ".5", "0123.", ".123", "678.876", 
              "0.", "000.000", ".0"])
    test_all("tp.pointfloat", False, 
             ["123", "0", "1", ".", ".123e5", "1.e+5", "2e5", "1.5e+6", "", 
              "-.5"])
    test_all("tp.pointfloat", None, ["1.a2","0.a0","1a."])

def exec_test_exponent():
    test_all("tp.exponent", True, 
             ["e5", "e+5", "e-5", "e1234567890098700", "E203", "e+125", "e-3", 
              "E+4","e0","E0", "e+0", "e-0", "E+0", "E-0", "e6", "e-5", 
              "e7","e8","E+9","e-1", "e+4321", "E-67", "E+124", "E+12", 
              "e-98500", "e12", "e-1"])
    test_all("tp.exponent", False, 
             ["", "e", "E", "+", "-", "e+", "e-", "E", "1e5", "1", "2.", 
              "ee5", "e+-5", "E++5", "E-+5", "e+3+"])
    test_all("tp.exponent", None, [ "a2","e+a0","e1a0" ])

def exec_test_exponentfloat():
    test_all("tp.exponentfloat", True, 
             ["1e5", "1e+5", "1e-5", "1234567890098700e-1234567890098700",
               "1234e123", "203E203", "000e+125", "0e-3", "1E+4","2e0","3E0","4e6",
              "5e-5","6e7","7e8","8E+9","9e-1", "4.e+43", "5.4E-67",
              ".5e0", "0123.e-0", ".123E+0", "678.876E-0", "0.e+124",
              "000.000E+12", ".0e-98500"])
    test_all("tp.exponentfloat", False, 
             ["1ee5", "1", "2.", "1e", "e", "+", "-", "1e+-5", "e5", 
              "e+5", "+1e5", "-1e5", "", "1e+"])
    test_all("tp.exponentfloat", None, ["1.a2","0.ae0","1e+a0","1e1a0"])

def exec_test_number():
    test_all("tp.number", True, 
             ["1234567890098700", "203", "0000", 
              "0", "1","2","3","4","5","6","7","8","9",
              "4.", "5.4", ".5", "0123.", ".123", "678.876",
              "0.", "000.000", ".0",
              "1e5", "1e+5", "1e-5", "1234567890098700e-1234567890098700",
              "1234567890098700e123",
              "203E203", "000e+125", "0e-3", "1E+4","2e0","3E0","4e6",
              "5e-5","6e7","7e8","8E+9","9e-1", "4.e+43", "5.4E-67",
              ".5e0", "0123.e-0", ".123E+0", "678.876E-0", "0.e+124",
              "000.000E+12", ".0e-98500"])
    test_all("tp.number", False,
             ["1ee5", "1e-", "2.E+", "1e", "e", "+", "-", "1e+-5", "e5", 
              "e+5", "+1e5", "-1e5", "", "1e+"])
    test_all("tp.number", None, 
             ["a2","0a0","1a0","1.a2","0.a0","1a.","2e+a0","1e1a0"])

# Si ce fichier est lancé directement, on exécute les tests
if __name__ == '__main__':
    if test_integer_Q2:
        exec_test_integer_Q2()
    if test_pointfloat_Q2:
        exec_test_pointfloat_Q2()
    if test_integer:
        exec_test_integer()
    if test_pointfloat:
        exec_test_pointfloat()
    if test_exponent:
        exec_test_exponent()
    if test_exponentfloat:
        exec_test_exponentfloat()
    if test_number:
        exec_test_number()
    print()
    print("@ all tests OK !")
