import Commands as c
from Main_program import main

#---------------------Credits:----------------------#
#--Programmed by Luki puki and Anananananananantha--#
#--------Pseudocode Interpreter v0.1(Alpha)--------#
print("---------------------Credits----------------------\n--Programmed by Luki puki and Anananananananantha--\n--------Pseudocode Interpreter v0.(Alpha)--------\n\n")

filename = "code.txt"
file = open("code.txt", "r")

lines = file.readlines()
file.close()
# General note: Line indexes in text files start from 0
# and newline characters (\n) have a length of 1, not 2

# vars 2D array to store each variable and its value
vars = []
proc_vars = []
# print(lines)

        
main(lines, vars)