# alright, im gona be honest here, this code your about to see,
# it aint exactly the best, you see, i kinda got burnt out
# making optimisations to my terminal graphics so dont expect
# this to be perfect









import graphics
import getkeys
import random
print("""

just want to say, this uses a terminal graphics system that
i have spent ages making, if you want to use it you can find it
in the 'refactored terminal graphics' project on my profile,
however it may not be finished depending on when you find this
message so just read any notes you see when starting up the
project for info on what parts are finished and what parts need
working on, ps. might make a github repo idk for now it can just
stay in my replit projects since it's still in pretty early
stages (at the time of writing this)
also check out my refactored rpg engine (it also uses this
graphical system) and also has like mod support stuff its pretty
cool

""")
print("warning: having board widths / heights greater than that of your terminal will probably break the renderer\n")
width = int(input("enter board width: "))
height = int(input("enter board height: "))
bombdensity = int(input("enter bomb density (0-100): "))
print("\033c", end="")
window = graphics.window("board",width,height)

#fill in board with bombs
bombs = round(height * width * 30 * bombdensity / 10000)
board = [[0 for x in range(width)] for y in range(height)]
visibleboard = [[10 for x in range(width)] for y in range(height)]
compleate = False

#super crude way of checking if bomb position is valid 
def validBomb(x,y):
  global board
  surounding = 0
  #check above
  try:
    if board[max(y-1,0)][x] < 0:
      surounding+=1
  except:
    pass
  #check below
  try:
    if board[y+1][x] < 0:
      surounding+=1
  except:
    pass
  #check right
  try:
    if board[y][x+1] < 0:
      surounding+=1
  except:
    pass
  #check left
  try:
    if board[y][max(x-1,0)] < 0:
      surounding+=1
  except:
    pass
  #check bottem left
  try:
    if board[y+1][max(x-1,0)] < 0:
      surounding+=1
  except:
    pass
  #check bottem right
  try:
    if board[y+1][x+1] < 0:
      surounding+=1
  except:
    pass
  #check top left
  try:
    if board[max(y-1,0)][max(x-1,0)] < 0:
      surounding+=1
  except:
    pass
  #check top right
  try:
    if board[max(y-1,0)][x+1] < 0:
      surounding+=1
  except:
    pass

  if surounding <= 6 and x <= width >= x and y <= height >= y and board[y][x] >= 0:
    return True
def plotBomb(x,y):
  global board
  board[y][x] = -9
  #top
  if y-1 >= 0:
    board[y-1][x] += 1
    #top left
    if x-1 >= 0: board[y-1][x-1] += 1
    #top right
    if x+1 <= width-1: board[y-1][x+1] += 1
  #bottem
  if y+1 <= height-1:
    board[y+1][x] += 1
    #bottem left
    if x-1 >= 0: board[y+1][x-1] += 1
    #bottem right
    if x+1 <= width-1: board[y+1][x+1] += 1
  #left
  if x-1 >= 0: board[y][x-1] += 1
  #right
  if x+1 <= width-1: board[y][x+1] += 1

#super crude way of ploting the bombs but it still works in like 0.00000004 seconds so idrc for now 
bombs_used=0
while True:
  x = random.randint(0,width-1)
  y = random.randint(0,height-1)
  if validBomb(x,y):
    plotBomb(x,y)
    bombs_used+=1
    if bombs_used >= bombs:
      break
  

#fill in the window with the green checker pattern
step = 0
for y in range(height):
  for x in range(step,width,2):
    window.plot(x,y,[20,190,20])
  step = abs(step-1)
step = 1
for y in range(height):
  for x in range(step,width,2):
    window.plot(x,y,[20,160,20])
  step = abs(step-1)

def updateWindow():
  global visibleboard
  global window
  for _y,y in enumerate(visibleboard):
    for _x,x in enumerate(y):
      if window.pixelMap[_y][_x]["char"] != visibleboard[_y][_x]:
        if x < 0:
          window.plot(_x,_y,[255,100,100],"B ")
        elif x < 10:
          window.plot(_x,_y,[133, 74, 42],str(x)+" ")
        elif x == 12:
          window.plot(_x,_y,[236, 245, 66],"/*")
        elif x == 13:
          window.plot(_x,_y,[100,255,100])
  window.update()

filled = []
def uncoverzeros(x,y):
  def fill(x,y):
    global filled
    global window
    global board
    global visibleboard
    filled.append((x,y))
    visibleboard[y][x] = board[y][x]
    window.plot(x,y,[133, 74, 42],str(board[y][x])+" ")
    window.update()
    window.render()
    isZero = True if board[y][x] == 0 else False
    neighbors = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
    for neighbor in neighbors:
      if neighbor not in filled:
        if 0 <= neighbor[0] <= width-1 and 0 <= neighbor[1] <= height-1:
          if isZero:
            fill(neighbor[0],neighbor[1])
  fill(x,y)

def uncoverArea(x,y):
  global visibleboard
  global board
  global window
  neighbors = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
  for neighbor in neighbors:
    if 0 <= neighbor[0] <= width-1 and 0 <= neighbor[1] <= height-1:
      visibleboard[neighbor[1]][neighbor[0]] = board[neighbor[1]][neighbor[0]]
      updateWindow()
      window.render()
#pre update so first render has some rendtext to draw
window.update()

controlls = """z - flag
x - dig
arrow keys - move cursor
l - leave game"""

running = True
cursorX = width//2
cursorY = height//2
oldX = cursorX
oldY = cursorY
oldColor = window.pixelMap[cursorY][cursorX]["color"]
should_update = False
light_update = False
first_click = True


#super duper jumbled up code with no readability spacing
while running:
  oldX = cursorX
  oldY = cursorY
  if should_update:
    updateWindow()
    should_update = False
    light_update = False
  if light_update and not should_update:
    window.update()
    light_update = False
  window.render()
  print(controlls)
  key = getkeys.getkey()
  if key == '\x1b[A':
    if cursorY > 0: cursorY-=1; light_update = True
  elif key == '\x1b[B':
    if cursorY < height-1: cursorY+=1; light_update = True
  elif key == '\x1b[C':
    if cursorX < width-1: cursorX+=1; light_update = True
  elif key == '\x1b[D':
    if cursorX > 0: cursorX-=1; light_update = True
  elif key == 'x':
    print("\a")
    visibleboard[cursorY][cursorX] = board[cursorY][cursorX]
    if board[cursorY][cursorX] >= 0:
      oldColor = [133, 74, 42]
    else:
      oldColor = [255,100,100]
      if not first_click:
        visibleboard = [[-8 for x in range(width)] for y in range(height)]
        updateWindow()
        window.render()
        print("YOU LOOSE")
        break
    should_update = True
    if board[cursorY][cursorX] == 0:
      uncoverzeros(cursorX,cursorY)
    if first_click:
      uncoverArea(cursorX,cursorY)
      first_click = False
  elif key == 'z':
    should_update = True
    print("\a")
    if visibleboard[cursorY][cursorX] == 10 or visibleboard[cursorY][cursorX] < 0: visibleboard[cursorY][cursorX] = 12
    if board[cursorY][cursorX] < 0: bombs-=1
    if bombs <= 0:
      visibleboard = [[13 for x in range(width)] for y in range(height)]
      updateWindow()
      window.render()
      print("YOU WIN")
      break
    oldColor = [236, 245, 66]
  elif key == "l":
    running = False
    break
  window.pixelMap[oldY][oldX]["color"] = oldColor
  oldColor = window.pixelMap[cursorY][cursorX]["color"]
  window.pixelMap[cursorY][cursorX]["color"] = [255,255,255]
  window.toUpdate[oldY] = True
  window.toUpdate[cursorY] = True
  window.toRender[oldY] = True
  window.toRender[cursorY] = True
  
