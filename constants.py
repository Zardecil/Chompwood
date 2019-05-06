import libtcodpy as tcod
import random
from objects import Tile

screenWidth = 100
screenHeight = 80

mapWidth = 1000
mapHeight = 1000

cameraPositionx = mapWidth//2
cameraPositiony = mapHeight//2

FPS = 20

font = "arial10x10.png"
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font, font_flags)
tilesize = 10
background_desirable = 10
window = "Slimewood"
fullscreen = False
tcod.console_init_root(screenWidth,screenHeight,window,fullscreen)

con = tcod.console_new(mapWidth,mapHeight)
textLayer = tcod.console_new(screenWidth,screenHeight)

game_state = "playing"

obelisk_number = 15
currentLevel = 0
zMax = 10
zMin = -10
zLevel = {}
objects = {}
print("Generating Map...")
for i in range(zMin,zMax + 1):
    if i < 0:
        biome = "Cave"
    else:
        biome = None
    zLevel[i] = [[Tile(False,None) for y in range(mapHeight)] for x in range(mapWidth)]
    objects[i] = []
forestColorDict = {
    True:tcod.Color(34,121,17),
    False:tcod.Color(52,184,25),
    }
desertColorDict = {
    False:tcod.Color(184,171,25),
    True:tcod.Color(121,81,17),
    }
mountainColorDict = {
    False:tcod.Color(105,105,105),
    True:tcod.Color(69,69,69),
    }
swampColorDict = {
    True:tcod.Color(25,54,184),
    False:tcod.Color(52,184,25),
    }
NoneDict = {
    True:tcod.black,
    False:tcod.black,
    }
obeliskColorDict = {
    True:tcod.Color(46,41,58),
    False:tcod.Color(61,53,75),
    }
caveDict = {
    True:tcod.Color(41,21,7),
    False:tcod.Color(71,31,17),
    }
biomeDir = {
    "Desert":desertColorDict,
    "Forest":forestColorDict,
    "Mountain":mountainColorDict,
    "Swamp":swampColorDict,
    None:NoneDict,
    "Obelisk":obeliskColorDict,
    "Cave":caveDict,
    }

currentMap = zLevel[currentLevel]
currentObjects = objects[currentLevel]
