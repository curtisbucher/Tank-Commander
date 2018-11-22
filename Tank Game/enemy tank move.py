def enemy_move(level, time, enemy_tank_object, player_tank_object, bullet_list,game_map):
    """ This function is called after every move the player, tank makes when the
        game is being compiled. It takes the game state, as well as the level,
        the player tank object (in order to get coordinates and rotation)
        and the enemy tank object (in order to get its own variables)as imput,
        and outputs the move that the tank will make. Before this is
        implimented, I must get the timing right with moving the player's tank,
        and the enemies tank so that the tank does not attempt a new move
        before it finished the old one.

        Should the Enemy tank move one space at a time for timing purposes?
    """
    player_x, player_y = player_tank_object.coords
    enemy_x, enemy_y = enemy_tank_object.coords
    
    ## 1: Does nothing
    if(level == 1):
        return("")
    ## 2: Rotates slowely, and shoots if it can hit you
    if(level == 2):
        if(can_hit_player(enemy_tank_object, player_tank_object):
           return("enemy.fire()")
        else:
           return("enemy.turn(1)")
        
    ## 3: Turns 90 degrees every second, otherwise drives. Shoots if it can hit you
    if(level == 3:
	if(time% 1000 == 0):
	    return("enemy.turn(90)")
        elif(can_hit_player(enemy_tank_object, player_tank_object):
            return("enemy.fire()")
	elif(time%100 == 0):
	    return("enemy.move(100)")
        else:
            return("")

def can_hit_player(enemy_tank_object, time, player_tank_object):
    """ This function takes in the enemy tank object and the player tank object
        as input, and uses their coordinates (and possibly there rotation and
        velocity) to see if a bullet can hit them
    """     
    player_x, player_y = player_tank_object.coords
    enemy_x, enemy_y = enemy_tank_object.coords
    ## The radius of the tank's target area in which it will shoot
    bounds = 10
    ## The lower left  coordinate in the target bounding box
    lower_bounds = (enemy_x - bounds, enemy_y - bounds)
    ## The upper right coordinate in the target bounding box
    upper_bounds = (enemy_x + bounds, enemy_y + bounds)

    ## Checking if the player's tank is within the bounding box
    if(lower_bounds[0] < player_x < upper_bounds[0]):
           if(upper_bounds[1] < player_y < lower_bound[1]):
               return(True)
    return(False)
