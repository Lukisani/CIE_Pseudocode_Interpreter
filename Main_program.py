import Commands as c

def main(lines, vars):
  LinesSkip = 0
  proc_endline = 0
  # print(vars)
  # Loops through every line in textfile
  for l in range(len(lines)):
    # Value of l starts from 0
    # print(l, proc_endline)
    if LinesSkip == 0:
      commandline = lines[l]
      command = c.extractcmd(commandline)
      
      # Calls for appropriate command handling
      if command == "OUTPUT":
          c.OUTPUT(commandline, vars)

      if command == "INPUT":
        c.INPUT(commandline, vars)

      if command == "DECLARE":
        c.DECLARE(commandline, vars)
      
      found = False
      if command == "IF":
        LinesSkip = c.IF(commandline, vars, l, lines)

      if command == "FOR":
        LinesSkip = c.ForLoop(commandline, vars, l, lines)

      if command == "WHILE":
        LinesSkip = c.WHILE(commandline, vars, l, lines)

      if command == "REPEAT":
        LinesSkip = c.REPEAT(commandline, vars, l, lines)

      if command == "PROCEDURE":
        try:
          proc_endline = lines.index("ENDPROCEDURE")
        except ValueError:
          proc_endline = lines.index("ENDPROCEDURE\n")
        LinesSkip = proc_endline - l
        c.DEF_PROCEDURE(commandline, lines, l, proc_endline)
      if command == "CALL":
        c.CALL(commandline)
        LinesSkip = 1

      # Checks if line is array assignment
      if "] <-" in lines[l]:
        
        arrayname = ""
        for i in lines[l]:
          if i == "[":
            break
          arrayname += i
        
        
        valfromvar = False
        arr_or_var = ""
        arrind = 0
        # Checks if array is valid
        for i in range(len(vars)):
          if vars[i][0] == arrayname:
            found = True
            arrind = i
            arr_or_var = "v" if len(vars[i]) == 2 else "a"
                 
        arraychangeindex = ""
        indfound = False
        print(arrind)

        # Finds the index within array we aim to change
        for i in range(len(lines[l])):
          #print(lines[l][i])
          if lines[l][i-1] == "[":
            indfound = True
          if lines[l][i] == "]":
            indfound = False
          if indfound:
            arraychangeindex += lines[l][i]

        # Pseudocode starts from one
        try:
          arraychangeindex = int(arraychangeindex) - 1
        except ValueError:
          valfromvar = True
          for v in vars:
            if v[0] == arraychangeindex:
              try:
                arraychangeindex = v[1] - 1
              except ValueError: print("Invalid data type")
        #print([arraychangeindex, arr_or_var])
        # Finds the value to put into array
        if arr_or_var == "a":
          if arraychangeindex > vars[arrind][2]:
            print("Invalid Index")
            #print(arrind)
          else:
            valfound = False
            arrval = ""
            for i in range(len(lines[l])):
              if valfound:
                arrval += lines[l][i]
              if lines[l][i] == " " and lines[l][i-1] == "-":
                valfound = True
            for i in range(len(vars)):
              if vars[i][0] == arrval.rstrip():
                arrval = vars[i][1]
            #print(arrval)
        else:
          valfound = False
          arrval = ""
          for i in range(len(lines[l])):
            if valfound:
              arrval += lines[l][i]
            if lines[l][i] == " " and lines[l][i-1] == "-":
              valfound = True
          for i in range(len(vars)):
            if vars[i][0] == arrval.rstrip():
              arrval = vars[i][1]
              #print("variable found")
              
          print([arrind,arraychangeindex])
        if arr_or_var == "a": 
            vars[arrind][1][arraychangeindex]
        else: 
            print("Cannot edit characters within string")

      # Checks if the line is variable assignment
      if command == "" and found == False:
        exists = False
        index = 0
        varName = c.extractVarName(commandline)

        try:
          val = c.extractVarVal(commandline).splitlines()[0]
        except AttributeError or IndexError:
          val = c.extractVarVal(commandline)

        for v in range(len(vars)):
          if vars[v][0] == varName: 
            exists = True
            index = v

        if exists:
          try:
            if '"' in val:
              vars[index][1] = val[1:-1]
          except TypeError:
            try: vars[index][1] = int(val)
            except ValueError: print("Entered value is not a string")
        else: print("Variable does not exist")

    else:
      LinesSkip -= 1
      #print(vars)