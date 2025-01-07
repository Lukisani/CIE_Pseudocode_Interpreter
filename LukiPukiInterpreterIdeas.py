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