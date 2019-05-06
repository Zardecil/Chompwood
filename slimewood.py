from constants import *
from objects import *
from generators import *

def handleKeys():
    global cameraPositionx,cameraPositiony,tilesize
    mouseinfo = tcod.mouse_get_status()
    tileToPixelx = screenWidth*tilesize
    tileToPixely = screenHeight*tilesize
    if 0<=mouseinfo.x<=tileToPixelx//10:
        cameraPositionx -= 1
    elif tileToPixelx-tileToPixelx//10<=mouseinfo.x<=tileToPixelx:
        cameraPositionx += 1
    
    if 0<=mouseinfo.y<tileToPixely//10:
        cameraPositiony -= 1
    elif tileToPixely-tileToPixely//10<=mouseinfo.y<=tileToPixely:
        cameraPositiony += 1
    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_CHAR:
        if key.c == 44:
            ascendordescend("up",player)
        if key.c == 46:
            ascendordescend("down",player)
    elif key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    
    elif key.vk == tcod.KEY_ESCAPE:
        return "exit"
    
    if game_state == "playing":
        if tcod.console_is_key_pressed(tcod.KEY_UP):
            player.move(0,-1,currentMap)
        elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
            player.move(0,1,currentMap)
        elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
            player.move(-1,0,currentMap)
        elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
            player.move(1,0,currentMap)
        else:
            return "didnt-take-turn"

def ascendordescend(upordown,target):
    global currentObjects
    global currentMap
    global currentLevel
    
    if upordown == "up":
        for thing in currentObjects:
            if thing.char == "<":
                if target.x == thing.x and target.y == thing.y:
                    currentObjects.remove(target)
                    currentLevel += 1
                    currentMap = zLevel[currentLevel]
                    currentObjects = objects[currentLevel]
                    currentObjects.append(target)
                    break
        else:
            currentLevel += 1
            currentMap = zLevel[currentLevel]
            currentObjects = objects[currentLevel]
    elif upordown == "down":
        for thing in currentObjects:
            if thing.char == ">":
                if target.x == thing.x and target.y == thing.y:
                    currentObjects.remove(target)
                    currentLevel -= 1
                    currentMap = zLevel[currentLevel]
                    currentObjects = objects[currentLevel]
                    currentObjects.append(target)
                    break
        else:
            currentLevel -= 1
            currentMap = zLevel[currentLevel]
            currentObjects = objects[currentLevel]
def renderAll():
    global textLayer
    for x in range(screenWidth):
        for y in range(screenHeight):
            tcod.console_put_char(0,x,y," ",tcod.BKGND_NONE)
            tcod.console_set_char_background(0,x,y,tcod.black,tcod.BKGND_SET)
            cell = currentMap[(x + cameraPositionx)%mapWidth][(y + cameraPositiony)%mapHeight]
            wall = cell.blocked
            if wall:
                tcod.console_set_char_background(con, x + cameraPositionx, y + cameraPositiony, \
                biomeDir[cell.biome][cell.blocked], tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x + cameraPositionx, y + cameraPositiony, \
                biomeDir[cell.biome][cell.blocked], tcod.BKGND_SET) 
    for thing in currentObjects:
        thing.draw()
    tcod.console_blit(con, cameraPositionx, cameraPositiony, screenWidth, screenHeight, 0, 0, 0)

player = Object(tcod.green,"@",screenWidth//2 + cameraPositionx,screenHeight//2 + cameraPositiony)
objects[0].append(player)
makeMap3()
forestGen()
desertGen()
mountainGen()
swampGen()
for i in range(-10,0):
    caveGen(i)
slimespawnergen(0,0,10,10)
obelisks = []
for i in range(0,3):
    w = random.randint(40,80)
    h = random.randint(40,80)
    x = random.randint(0,mapWidth - w - 1)
    y = random.randint(0,mapHeight - h - 1)
    new = Obelisk(w, h, x, y, i)
         
    # run through the other rooms and see if they intersect with this one
    failed = False
    for other_obelisk in obelisks:
        if new.intersect(other_obelisk):
            failed = True
            break
    obelisks.append(new)
    if not failed:
        new.floorgen()
currentMap = zLevel[currentLevel]
while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    renderAll()
    tcod.console_flush()
    for thing in currentObjects:
        thing.clear()
    player_action = handleKeys()
    if player_action == "exit":
        break
    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for thing in objects:
            if thing != player:
                pass
