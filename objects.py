import libtcodpy as tcod
import constants,random
class Object:
    def __init__(self,color,char,x,y):
        self.x = x
        self.y = y
        self.color = color
        self.char = char
    
    def move(self,dx,dy,Map): 
        if not Map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy
    
    def draw(self):
        tcod.console_set_default_foreground(constants.con, tcod.white)
        tcod.console_put_char(constants.con, self.x, self.y, self.char, tcod.BKGND_NONE)
    
    def clear(self):
        tcod.console_put_char(constants.con,self.x,self.y,' ',tcod.BKGND_NONE)
class Rect:
    # a rectangle on the map. used to characterize a room.
 
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.center_x = (self.x1 + self.x2) // 2
        self.center_y = (self.y1 + self.y2) // 2
    def center(self):
        return (self.center_x, self.center_y)
 
    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
class Tile:
    def __init__(self,blocked,biome = None,block_sight=None):
        self.blocked = blocked
        self.biome = biome
        self.color = tcod.black
        self.flags = []
        
        #how claimed a tile is.
        self.markLevel = 0
        
        #helps run the AI, by default the tile is no more enticing to an entity then the next. Changable to create more desirable tiles(entities will flock to them)
        self.desirable = constants.background_desirable
        
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

class Obelisk:
    def __init__(self,width,height,x,y,ID):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height
        self.floors = random.randint(4,7)
        self.maps = [[[Tile(True,biome = "Obelisk") for y in range(self.height)] for x in range(self.width)] for z in range(self.floors)]

        self.buffer = 2
    
    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x <= other.x2 and self.x2 >= other.x and
                self.y <= other.y2 and self.y2 >= other.y)
                
    def floorgen(self):
        global upstairs

        def create_room(room):
            # go through the tiles in the rectangle and make them passable
            for x in range(room.x1 + 1, room.x2):
                for y in range(room.y1 + 1, room.y2):
                    Map1[x][y].blocked = False
                    Map1[x][y].block_sight = False
     
     
        def create_h_tunnel(x1, x2, y):
            # horizontal tunnel. min() and max() are used in case x1>x2
            for x in range(min(x1, x2), max(x1, x2) + 1):
                Map1[x][y].blocked = False
                Map1[x][y].block_sight = False


        def create_v_tunnel(y1, y2, x):
            # vertical tunnel
            for y in range(min(y1, y2), max(y1, y2) + 1):
                Map1[x][y].blocked = False
                Map1[x][y].block_sight = False
        iteration = 0
        for Map1 in self.maps:
            rooms = []
            num_rooms = 0
            for r in range(30):
                # random width and height
                w = tcod.random_get_int(0, 5, 20)
                h = tcod.random_get_int(0, 5, 20)
                # random position without going out of the boundaries of the map
                x = tcod.random_get_int(0, 0, self.width - w - 1)
                y = tcod.random_get_int(0, 0, self.height - h - 1)
         
                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)
         
                # run through the other rooms and see if they intersect with this one
                failed = False
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        failed = True
                        break
         
                if not failed:
                    # this means there are no intersections, so this room is valid
                    # "paint" it to the map's tiles
                    create_room(new_room)
         
                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()
         
                    
                    # connect it to the previous room with a tunnel
                    if num_rooms != 0:
                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    elif iteration == 0:
                        (prev_x,prev_y) = (random.choice([0,len(Map1) - 1]),new_y)
                        for x4 in range(-1,self.width + 1):
                            for y4 in range(-1,self.height + 1):
                                constants.zLevel[0][x4 + self.x][y4 + self.y].biome = "Obelisk"
                                constants.zLevel[0][x4 + self.x][y4 + self.y].blocked = False
                                constants.zLevel[0][x4 + self.x][y4 + self.y].block_sight = False 
                    else:
                        room = Rect(x2,y2,w2,h2)
                        create_room(room)
                        (prev_x,prev_y) = room.center()
                        rooms.append(room)
                        downstairs = Object(tcod.gray,">",prev_x + self.x,prev_y + self.y)
                        constants.objects[iteration].append(downstairs)
                    # draw a coin (random number that is either 0 or 1)
                    if tcod.random_get_int(0, 0, 1) == 1:
                        # first move horizontally, then vertically
                        create_h_tunnel(prev_x, new_x, prev_y)
                        create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        create_v_tunnel(prev_y, new_y, prev_x)
                        create_h_tunnel(prev_x, new_x, new_y)
                        
                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
                    w2 = w
                    h2 = h
                    x2 = x
                    y2 = y
            if iteration != self.floors - 1:
                upstairs = Object(tcod.gray,"<",new_x + self.x,new_y + self.y)
                constants.objects[iteration].append(upstairs)
            for x5 in range(0,self.width):
                for y5 in range(0,self.height):
                    constants.zLevel[iteration][x5 + self.x][y5 + self.y] = self.maps[iteration][x5][y5]
            iteration += 1
