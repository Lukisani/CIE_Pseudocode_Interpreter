def originalIF(cmd, vars):
  condition = cmd[3:-5]
  # -5 because of 'THEN'
  var = ""
  varval = ""
  found = False
  for i in condition:
    if i == " ":
      break
    else:
      var += i

  # Finds variable in vars (2d array) and assigns the value of the variable
  for v in vars:
    if v[0] == var:
      found = True
      varval = str(v[1])
  if not found: print("Invalid Variable")
  else:
    op = condition[len(var)+1:len(var)+3]
    ops = ["=", ">", "<"]
    comp = ""
    isint = False
    found1 = False
    for a in range(len(condition)):
      if found1:
        comp += condition[a]
      if condition[a] == " " and condition[a-1] in ops:
        found1 = True

    comp = comp.rstrip()

    try:
      comp = int(comp)
      isint = True
    except ValueError:
      comp = comp

    #print([op,comp,isint])
    #print(vars)

    if isint:
      if op == "> ":
        return (int(varval) > comp)
      elif op == "< ":
        return (int(varval) < comp)
      elif op == "= ":
        return (int(varval) == comp)
      elif op == "<>":
        return (int(varval) != comp)
      else:
        print("Invalid Operator")
        return False
    else:
      compv = ""
      for v in vars:
        if v[0] == comp:
          compv = v[1]
      if op == "> ":
        return (int(varval) > compv)
      elif op == "< ":
        return (int(varval) < compv)
      elif op == "= ":
        print(compv)
        return (varval == compv)
      elif op == "<>":
        return (int(varval) != compv)
      else:
        print("Invalid Operator")
        return False

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
        if cmd[c-1] == " " and cmd[c-2] == "-" and cmd[c-3] == "<":
            val = True
            index = c
        if val:
            var += cmd[c]

    try:
      var = int(var)
    except ValueError:
      var = var

    return var

def OriginalDECLARE(cmd, vars):

  for i in range(len(cmd)):
    if cmd[i] == " " and cmd[i+1] == ":":
      index = i
  varName = cmd[8:index]
  type = cmd[index+3]
  if type == "A":
    length = ""
    islen = False
    for i in range(len(cmd)):
      if cmd[i-1] == "[":
        islen = True
      if cmd[i] == "]":
        islen = False
      if islen:  
        length += cmd[i]

    length = int(length)
    vars.append([varName, [0 for i in range(length)], length])
    #print(vars)
  else:
    vars.append([varName, ""])

def originalOUTPUT(cmd, vars):

    cmd = cmd.splitlines()[0]
    if cmd[7] == '"' or cmd[7] == "'" and cmd[-1] == '"' or cmd[-1] == "'":
      print(cmd[8:-1])
    else:
      found = False
      varname = cmd[7:]
      # print(vars)
      for v in range(len(vars)):
        if vars[v][0] == varname:
          found = True
          print(vars[v][1])
      if not found:
        print("Invalid Variable:", varname, 'not defined')

def originalINPUT(cmd, vars):
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

def secondIF(cmd, vars, ifStart, textfile):
  import Main_program as gae
  condition = cmd[3:-5]
  isTrueOrFalse = False
  # -5 because of 'THEN'
  var = ""
  varval = ""
  found = False
  for i in condition:
    if i == " ":
      break
    else:
      var += i
  
  # Finds variable in vars (2d array) and assigns the value of the variable
  for v in vars:
    if v[0] == var:
      found = True
      varval = str(v[1])
  if not found: print("Invalid Variable")
  else:
    op = condition[len(var)+1:len(var)+3]
    ops = ["=", ">", "<"]
    comp = ""
    isint = False
    found1 = False
    for a in range(len(condition)):
      if found1:
        comp += condition[a]
      if condition[a] == " " and condition[a-1] in ops:
        found1 = True
  
    comp = comp.rstrip()
  
    try:
      comp = int(comp)
      isint = True
    except ValueError:
      comp = comp
  
    #print([op,comp,isint])
    #print(vars)
  
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
  # Finds end of if statement
  endIfIndex = ifStart
  EndIfFound = False
  while not EndIfFound and endIfIndex < len(textfile):
    if textfile[endIfIndex][:5].lower() == 'endif':
      EndIfFound = True
    else:
      endIfIndex += 1
  # Reads number of spaces indent is made of
  if isTrueOrFalse:
    indent = 0
    while textfile[ifStart + 1][indent] == ' ':
      indent += 1
    # Copies all lines in loop for recursive function
    ifCode = []
    for i in range(ifStart + 1, endIfIndex):
      ifCode.append(textfile[i][indent:])
    gae.main(ifCode, vars)
  return endIfIndex - ifStart