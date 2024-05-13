

def printPoint(font, points, screen):
    text_x = 10
    text_y = 10
    
    fontPoint = font.render(f"Points: {points}", True ,(255,255,255))
    screen.blit(fontPoint,(text_x,text_y))