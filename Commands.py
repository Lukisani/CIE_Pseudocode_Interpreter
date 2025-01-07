# Commands defined so far: OUTPUT, INPUT, DECLARE, IF
# To be defined: WHILE, FOR, REPEAT UNTIL

def extractcmd(cmd):
    # Reads command based on uppercase, stops after first space
    # Stores commands in variable command
    command = ""
    for c in cmd:
        if c.isupper():
            command += c
        if c == " ":
            break
    return command


def extractVarName(cmd):
    # Variable assignment, returns name of variable being assigned
    varName = ""
    for c in cmd:
        varName += c
        if c == " ":
            break
    return varName.rstrip()


def extractVarVal(cmd):
    # Variable assignment, returns value of variable being assigned
    # Find value based on its position in statement
    val = False
    var = ""
    index = 0
    for c in range(len(cmd)):
        if cmd[c - 1] == " " and cmd[c - 2] == "-" and cmd[c - 3] == "<":
            val = True
            index = c
        if val:
            var += cmd[c]

    try:
        var = int(var)
    except ValueError:
        var = var

    return var


def DECLARE(cmd, vars):
    index = 0
    for i in range(len(cmd)):
        if cmd[i] == " " and cmd[i + 1] == ":":
            index = i
    varName = cmd[8:index]
    type = cmd[index + 3]
    if type == "A":
        length = ""
        islen = False
        for i in range(len(cmd)):
            if cmd[i - 1] == "[":
                islen = True
            if cmd[i] == "]":
                islen = False
            if islen:
                length += cmd[i]

        length = int(length)
        vars.append([varName, [0 for i in range(length)], length])
        # print(vars)
    else:
        vars.append([varName, ""])


def conditions(condition, vars):
  # Used for any functions with conditions...
  # Returns result of boolean expressions

  isTrueOrFalse = False
  # Identifies variable used in expression
  var = ""
  varval = ""
  found = False
  for i in condition:
      if i == " ":
          break
      else:
          var += i

  # Finds variable in vars (2d array) and extracts its value and stores in varval
  for v in vars:
      if v[0] == var:
          found = True
          varval = str(v[1])
  if not found:
      print("Invalid Variable")
  else:
      # Finds operator in statement
      op = condition[len(var) + 1:len(var) + 3]
      ops = ["=", ">", "<"]
      comp = ""
      isint = False
      found1 = False
      for a in range(len(condition)):
          if found1:
              comp += condition[a]
          if condition[a] == " " and condition[a - 1] in ops:
              found1 = True

      comp = comp.rstrip()

      try:
          comp = int(comp)
          isint = True
      except ValueError:
          comp = comp

      # print([op,comp,isint])
      # print(vars)

      if isint:
          if op == "> ":
              isTrueOrFalse = (int(varval) > comp)
          elif op == "< ":
              isTrueOrFalse = (int(varval) < comp)
          elif op == "= ":
              isTrueOrFalse = (int(varval) == comp)
          elif op == "<>":
              isTrueOrFalse = (int(varval) != comp)
          else:
              print("Invalid Operator")
              isTrueOrFalse = False
      else:
          compv = ""
          for v in vars:
              if v[0] == comp:
                  compv = v[1]
          if op == "> ":
              isTrueOrFalse = (int(varval) > compv)
          elif op == "< ":
              isTrueOrFalse = (int(varval) < compv)
          elif op == "= ":
              print(compv)
              isTrueOrFalse = (varval == compv)
          elif op == "<>":
              isTrueOrFalse = (int(varval) != compv)
          else:
              print("Invalid Operator")
              isTrueOrFalse = False
  return isTrueOrFalse
  

def IF(cmd, vars, ifStart, textfile):
    import Main_program as gae
    condition = cmd[3:-5]
    # -5 because of ' THEN'
    IsIfTrueOrFalse = conditions(condition, vars)
  
    # Finds end of if statement
    endIfIndex = ifStart
    EndIfFound = False
    while not EndIfFound and endIfIndex < len(textfile):
        if textfile[endIfIndex][:5].lower() == 'endif':
            EndIfFound = True
        else:
            endIfIndex += 1
    # Reads number of spaces indent is made of
    if IsIfTrueOrFalse:
        indent = 0
        while textfile[ifStart + 1][indent] == ' ':
            indent += 1
        # Copies all lines in loop for recursive function
        ifCode = []
        for i in range(ifStart + 1, endIfIndex):
            ifCode.append(textfile[i][indent:])
        gae.main(ifCode, vars)
    return endIfIndex - ifStart


def OUTPUT(cmd, vars):
    cmd = cmd.splitlines()[0]
    lastchar = 0
    if cmd[7] == '"' or cmd[7] == "'" and cmd[-1] == '"' or cmd[-1] == "'":
        print(cmd[8:-1])
    else:
        found = False
        varname = cmd[7:]
        concvarname = ""
        if "[" in varname:
            delete = False
            for i in range(len(varname)):
                if varname[i] == "[" and delete == False:
                    lastchar = i
                    delete = True
            concvarname = varname[:lastchar]
        # print(varname)
        v_index = 0
        for v in range(len(vars)):
            if vars[v][0] == varname or vars[v][0] == concvarname:
                found = True
                v_index = v
        if not found:
            print("Invalid Variable:", varname, 'not defined')
        else:
            if "[" and "]" in cmd:
                index = ""
                isindex = False
                for i in range(len(varname)):
                    if isindex:
                        index += varname[i]
                    if varname[i] == "]":
                        isindex = False
                    if varname[i] == "[":
                        isindex = True
                index = index[:-1]
                try:
                    print(vars[v_index][1][int(index)])
                except ValueError:
                    for a in range(len(vars)):
                        if vars[a][0] == index:
                            found = True
                    if found:
                        value = int(vars[a][1])
                        print(vars[v_index][1][value])
                    else:
                        print("Invalid variable for concactenation")
                except IndexError:
                    print("Index out of range")
            else:
                print(vars[v_index][1])


def INPUT(cmd, vars):
    # Prompts user for input to assign to variable requested for input

    varInput = cmd[6:]
    varInput = varInput.splitlines()[0]
    # print([varInput])
    for v in range(len(vars)):
        if vars[v][0] == varInput:
            varValue = input()
            vars[v][1] = varValue
        else:
            print('Error, variable not defined')


def ForLoop(cmd, vars, loopStart, textfile):
    import Main_program as gae
    # Firstly finds for loop variable and assigns value
    var = ''
    varNameIndex = 4
    while cmd[varNameIndex] != ' ':
        var += cmd[varNameIndex]
        varNameIndex += 1

    varIndex = 0
    varFound = False
    # Gets position of var in vars
    while not varFound and varIndex < len(vars):
        if vars[varIndex][0] == var:
            varFound = True
        varIndex += 1
    varIndex -= 1

    # for with <- is 8 characters
    startValueIndex = 8 + len(var)
    # Finds starting value of loop variable
    startValue = ''
    while cmd[startValueIndex] != ' ':
        startValue += cmd[startValueIndex]
        startValueIndex += 1
    startValue = int(startValue)
    # Finds end value of loop variable
    endValueIndex = 12 + len(var) + len(str(startValue))
    endValue = cmd[endValueIndex:]
    endValue = int(endValue)
    # Finds end of loop
    NextIndexPosition = loopStart
    EndOfLoopfound = False
    while not EndOfLoopfound and NextIndexPosition < len(textfile):
        if textfile[NextIndexPosition][:4].lower() == 'next':
            EndOfLoopfound = True
        else:
            NextIndexPosition += 1
    # print('start of loop:', loopStart)
    # print('end of loop:', NextIndexPosition)
    # Reads number of spaces indent is made of
    indent = 0
    while textfile[loopStart + 1][indent] == ' ':
        indent += 1
    # Copies all lines in loop for recursive function
    loop = []
    for i in range(loopStart + 1, NextIndexPosition):
        loop.append(textfile[i][indent:])
    # The actual loop
    for i in range(startValue, endValue + 1):
        vars[varIndex][1] = i
        gae.main(loop, vars)
    return NextIndexPosition - loopStart


def WHILE(cmd, vars, loopStart, textfile):
  import Main_program as gae
  condition = cmd[6:-3]
  # -3 because of ' DO'
  isWhileTrueOrFalse = conditions(condition, vars)
  
  # Finds end of loop
  EndWhilePosition = loopStart
  EndOfLoopfound = False
  while not EndOfLoopfound and EndWhilePosition < len(textfile):
    if textfile[EndWhilePosition][:8].lower() == 'endwhile':
      EndOfLoopfound = True
    else:
      EndWhilePosition += 1
  
  # Reads number of spaces indent is made of
  indent = 0
  while textfile[loopStart + 1][indent] == ' ':
      indent += 1
  
  # Copies all lines in loop for recursive function
  loop = []
  for i in range(loopStart + 1, EndWhilePosition):
    loop.append(textfile[i][indent:])
    
  # The actual loop
  while isWhileTrueOrFalse:
    gae.main(loop, vars)
    isWhileTrueOrFalse = conditions(condition, vars)
  return EndWhilePosition - loopStart


def REPEAT(cmd, vars, loopStart, textfile):
  import Main_program as gae

  #Finds end of loop
  UntilPosition = loopStart
  EndOfLoopfound = False
  while not EndOfLoopfound and UntilPosition < len(textfile):
    if textfile[UntilPosition][:5].lower() == 'until':
      EndOfLoopfound = True
    else:
      UntilPosition += 1
  
  # Reads number of spaces indent is made of
  indent = 0
  while textfile[loopStart + 1][indent] == ' ':
      indent += 1
  
  # Copies all lines in loop for recursive function
  loop = []
  for i in range(loopStart + 1, UntilPosition):
    loop.append(textfile[i][indent:])
  
  # Executes loop once first, then repeats while condition is true
  gae.main(loop, vars)
  isRepeatUntilTrue = textfile[UntilPosition][6:]
  while isRepeatUntilTrue:
    gae.main(loop, vars)
    isRepeatUntilTrue = textfile[UntilPosition][6:]
  return UntilPosition - loopStart

def DEF_PROCEDURE(cmd, lines, start, end):
  proc_name = cmd[10:-3] + ".txt"
  # Reads number of spaces indent is made of
  indent = 0
  while lines[start + 1][indent] == ' ':
      indent += 1
  f = open(proc_name, "x")
  
  for l in range(start+1, end-1):
    f.write(lines[l][indent:])

def CALL(cmd):
  import Main_program as mp
  from main import vars
  proc_name = cmd[5:-2] + ".txt"
  proc_file = open(proc_name, "r")
  proclines = proc_file.readlines()
  mp.main(proclines, vars)
  #print(vars)