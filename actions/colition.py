

import math


def isColition(x_bullet, x_ship, y_bullet, y_ship):
    if x_bullet != 0:
        distance = math.sqrt(math.pow(x_ship - x_bullet,2) + math.pow(y_ship - y_bullet ,2))
        
        if distance < 27 and distance > 24:
            return True
        else: 
            return False
    
def isColitionShip_Enemy(x_ship,x_enemy, y_ship, y_enemy):
    distance = math.sqrt(math.pow(x_enemy - x_ship,2) + math.pow(y_enemy - y_ship,2))
        
    if distance < 27:
        return True
    else: 
        return False