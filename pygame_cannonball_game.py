# Imported modules and initialization (add as necessary)
import pygame
pygame.init()
import random
import game_classes as gc # Boat, Cannonball, Mermaid sprites

# Useful constants -- vary these to adjust timing
BOAT_SPEED = 2
BALL_SPEED = 3
BALL_RATE = 2000
MERMAID_RATE = 3000
last_ball_spawn = 0
last_mermaid_spawn = 0

# Clock for limiting speed
FPS = 60
clock = pygame.time.Clock()

# Main surface settings
SURF_WIDTH, SURF_HEIGHT = 800, 600
surface = pygame.display.set_mode((SURF_WIDTH, SURF_HEIGHT))
pygame.display.set_caption("Sailing the Seven Seas")

# Sprite groups for easy collision detection
boat_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
mermaid_group = pygame.sprite.Group()

# Player's boat
boat = gc.Boat(0, 300, speed=BOAT_SPEED)
boat_group.add(boat)

# Background music
pygame.mixer.music.load("happy.ogg")
pygame.mixer.music.play(-1)

# Fonts for displaying score, game over status
font = pygame.freetype.Font("Grobold.ttf")
score_label, score_label_rect = font.render("Score:", "navy", size=48)
score = 0
score_count, score_count_rect = font.render(str(score), "white", size=48)
left_click_time = -float("inf")
game_over, game_over_rect = font.render("GAME OVER", "red", size=100)

# MAIN GAME LOOP
running = True
alive = True
while running:
    
    # Quit the game by clicking the window-manager's exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check if a cannonball was clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for ball in ball_group:
                    # Remove cannonball if clicked
                    if ball.rect.collidepoint(pos):
                        ball_group.remove(ball)
                        score += 1
                        score_count, score_count_rect = font.render(str(score), "white", size=48)
        
        # Check if horn was pressed while mermaid is visible
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                boat.sound.play()
                # Mermaid must be visible to clear the group
                if mermaid_group.sprites():
                    mermaid_group.empty()
                    score += 1
                    score_count, score_count_rect = font.render(str(score), "white", size=48)
    
    if alive:
        # Add a cannonball if enough time has elapsed
        time = pygame.time.get_ticks()
        if time - last_ball_spawn > BALL_RATE:
            last_ball_spawn = time
            ball = gc.Cannonball(0, 0, speed=BALL_SPEED)
            ball.rect.x = random.randint(0, SURF_WIDTH-ball.rect.width)
            ball.sound.play()
            ball_group.add(ball)
        
        # Add a mermaid if one is not already present, and not colliding with boat
        if time - last_mermaid_spawn > MERMAID_RATE:
            last_mermaid_spawn = time
            mermaid = gc.Mermaid(0, 360)
            mermaid.rect.x = random.randint(0, SURF_WIDTH-mermaid.rect.width)
            while pygame.sprite.collide_mask(mermaid, boat):
                mermaid.rect.x = random.randint(0, SURF_WIDTH-mermaid.rect.width)
            mermaid_group.add(mermaid)

        # Redraw the sky, water and sprites
        surface.fill("skyblue")
        boat_group.draw(surface)
        ball_group.draw(surface)
        mermaid_group.draw(surface)
        pygame.draw.rect(surface, "navy", (0, 467, SURF_WIDTH, SURF_HEIGHT - 467))
        surface.blit(score_label, (10, 10))
        surface.blit(score_count, (25 + score_label_rect.width, 10))
        
        # Update all sprite positions
        if boat.rect.x + boat.rect.width >= SURF_WIDTH or boat.rect.x < 0:
            boat_group.update(flip=True)
        else:
            boat_group.update()
        ball_group.update()
        # NOT YET IMPLEMENTED
        #mermaid_group.update()
        
        # Check if boat collides with cannonball or mermaid
        if (pygame.sprite.spritecollideany(boat, ball_group, pygame.sprite.collide_mask) or
            pygame.sprite.spritecollideany(boat, mermaid_group, pygame.sprite.collide_mask)):
            pygame.mixer.music.stop()
            surface.blit(game_over, ((SURF_WIDTH-game_over_rect.width)//2, (SURF_HEIGHT-game_over_rect.height)//2))
            alive = False
    
    # Update display
    pygame.display.update()
    clock.tick(FPS)

# Shut down pygame
pygame.quit()