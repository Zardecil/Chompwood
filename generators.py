from constants import *
from objects import Tile, Rect, Object
import time
def odds(percentage):
    probability = random.randint(0,100)
    if probability<percentage:
        return True
    else:
        return False

def makeMap3():
    global Map
    #Create the list to store the coordinates of stuff that still needs filling.
    toFill = []
    #Seed the map with 50 of each biome
    for i in range(0,50):
        for Land in ["Forest","Swamp","Mountain","Desert"]:
            x = random.randint(0,mapWidth) - 1
            y = random.randint(0,mapHeight) - 1
            zLevel[0][x][y].biome = Land
            toFill.append([x,y])
    #while there are still tiles to fill
    while len(toFill) != 0:
        #Grab the first one on the list(and remove it from the list)
        place = toFill.pop(0)
        for i in range(-1,2,2):
            #Look at surrounding tiles, check if they have no assigned biome, 
            #and if no biome set that tile's biome to be the parent tile's biome. Then add it back to the toFill list.
            if zLevel[0][place[0]][place[1]].biome != None:
                if zLevel[0][(place[0] + i)%mapWidth][place[1]].biome == None:
                    toFill.append([(place[0] + i)%mapWidth,place[1]])
                    zLevel[0][(place[0] + i)%mapWidth][place[1]].biome = zLevel[0][place[0]][place[1]].biome
                if zLevel[0][place[0]][(place[1] + i)%mapHeight].biome == None:
                    toFill.append([place[0],(place[1] + i)%mapHeight])
                    zLevel[0][place[0]][(place[1] + i)%mapHeight].biome = zLevel[0][place[0]][place[1]].biome

def forestGen():
    start_time = time.time()
    print("Generating Forest. . .")
    global Map
    
    def check(x,y,dx,dy):
        try:
            if tempMap[x + dx][y + dy].blocked:
                return False
            else:
                return True
        except IndexError:
            return True
    tempMap = zLevel[0]
    endTempMap = zLevel[0]
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            endTempMap[x][y].biome = zLevel[0][x][y].biome
            if tempMap[x][y].biome == "Forest":
                tempMap[x][y].blocked = odds(42)
                    
    
    iterations = 10
    
    for i in range(0,iterations):
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                if tempMap[x][y].biome == "Forest":
                    deadTiles = 0
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if check(x,y,dx,dy):
                                deadTiles += 1
                    if deadTiles <= 4:
                        endTempMap[x][y].blocked = True
                        endTempMap[x][y].block_sight = True
                    elif deadTiles >= 6:
                        endTempMap[x][y].blocked = False
                        endTempMap[x][y].block_sight = False
            
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                endTempMap[x][y].blocked = tempMap[x][y].blocked
                
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if endTempMap[x][y].biome == "Forest":
                zLevel[0][x][y].blocked = endTempMap[x][y].blocked
    print("Done.")
    print("--- %s seconds ---" % (time.time() - start_time))

def desertGen():
    print("Generating Desert. . .")
    global Map
    def check(x,y,dx,dy):
        try:
            if tempMap[x + dx][y + dy].blocked:
                return True
            else:
                return False
        except IndexError:
            return True
            
    tempMap = zLevel[0]
    endTempMap = zLevel[0]
    iterations = 20
    
    for i in range(0,iterations):
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                isWall = 0
                endTempMap[x][y].biome = zLevel[0][x][y].biome
                if tempMap[x][y].biome == "Desert":
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if check(x,y,dx,dy):
                                isWall = 1
                    if isWall == 1:
                        endTempMap[x][y].blocked = odds(20)
                    else:
                        endTempMap[x][y].blocked = odds(1)
                    
            
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                endTempMap[x][y].blocked = tempMap[x][y].blocked
                
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if endTempMap[x][y].biome == "Desert":
                zLevel[0][x][y].blocked = endTempMap[x][y].blocked
    print("Done.")

def mountainGen():
    print("Generating Mountains. . .")
    def check(x,y,dx,dy):
        try:
            if readMap[x + dx][y + dy].blocked:
                return True
            else:
                return False
        except IndexError:
            return True
    readMap = zLevel[0]
    writeMap = zLevel[0]
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if readMap[x][y].biome == "Mountain":
                readMap[x][y].blocked = odds(60)
                    
    iterations = 4
    for i in range(0,iterations):
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                if readMap[x][y].biome == "Mountain":
                    floorTiles = 0
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if check(x,y,dx,dy):
                                floorTiles += 1
                    if floorTiles <= 4:
                        writeMap[x][y].blocked = False #floor
                    elif floorTiles >= 6:
                        writeMap[x][y].blocked = True #wall
            
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                if writeMap[x][y].biome == "Mountain":
                     readMap[x][y].blocked = writeMap[x][y].blocked
                
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if readMap[x][y].biome == "Mountain":
                zLevel[0][x][y].blocked = readMap[x][y].blocked
    print("Done.")

def swampGen():
    print("Generating Swamps. . .")
    global Map
    def check(x,y,dx,dy):
        try:
            if readMap[x + dx][y + dy].blocked:
                return True
            else:
                return False
        except IndexError:
            return True
    readMap = zLevel[0]
    writeMap = zLevel[0]
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if readMap[x][y].biome == "Swamp":
                readMap[x][y].blocked = odds(60)
                    
    iterations = 4
    for i in range(0,iterations):
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                if readMap[x][y].biome == "Swamp":
                    floorTiles = 0
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if check(x,y,dx,dy):
                                floorTiles += 1
                    if floorTiles <= 4:
                        writeMap[x][y].blocked = False #floor
                    elif floorTiles >= 6:
                        writeMap[x][y].blocked = True #wall
            
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                if writeMap[x][y].biome == "Swamp":
                     readMap[x][y].blocked = writeMap[x][y].blocked
                
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            if readMap[x][y].biome == "Swamp":
                zLevel[0][x][y].blocked = not readMap[x][y].blocked
    print("Done.")
    
def caveGen(layer):
    print("Generating Caves...")
    
    def check(x,y,dx,dy):
        try:
            if tempMap[x + dx][y + dy].blocked:
                return False
            else:
                return True
        except IndexError:
            return True
    tempMap = zLevel[layer]
    endTempMap = zLevel[layer]
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            endTempMap[x][y].biome = "Cave"
            tempMap[x][y].blocked = odds(42)
                    
    
    iterations = 10
    
    for i in range(0,iterations):
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                    deadTiles = 0
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if check(x,y,dx,dy):
                                deadTiles += 1
                    if deadTiles <= 4:
                        endTempMap[x][y].blocked = True
                        endTempMap[x][y].block_sight = True
                    elif deadTiles >= 6:
                        endTempMap[x][y].blocked = False
                        endTempMap[x][y].block_sight = False
            
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                endTempMap[x][y].blocked = tempMap[x][y].blocked
                
    for x in range(0,mapWidth):
        for y in range(0,mapHeight):
            zLevel[layer][x][y].blocked = endTempMap[x][y].blocked
def slimespawnergen(minx,miny,maxx,maxy):
    spawningSlime = Object(tcod.blue, "S", random.randint(minx,maxx),random.randint(miny,maxy))
    objects[0].append(spawningSlime)
