

def bulletShot(image,screen,visible, x, y):
    screen.blit(image,(x+16,y+10))
    visible = True
    return visible