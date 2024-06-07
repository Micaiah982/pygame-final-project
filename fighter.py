import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, spritesheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(spritesheet, animation_steps)
        self.action = 0 #0: Idle, 1: Run, 2: Jump, 3: Attack1, 4: Attack2, 5: Hit, 6: Death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 100))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True
        self.health = 100
    
    def load_images(self, spritesheet, animation_steps):
        #extract images from spritesheet
        for animation in animation_steps:
            y = 0
            animation_list = []
            temp_image_list = []
            for x in range(animation):
                temp_image = spritesheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_image_list.append(pygame.transform.scale(temp_image, (self.size * self.image_scale, self.size * self.image_scale)))
            y += 1
            animation_list.append(temp_image_list)
        return animation_list
    
    def move(self, screen_width, screen_height, surface, target):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #Keypresses
        key = pygame.key.get_pressed()
        
        #Can only do this if not currently attacking
        if self.attacking == False and self.alive == True:
            #Check player 1 controls
            if self.player == 1:
                #Movement - WASD for Player 1, Arrow Keys for Player 2
                if key[pygame.K_a]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                #Jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #Attack
                if  key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(surface, target)
                    #determine which attack was used
                    if key[pygame.K_q]:
                        self.attack_type = 1
                    if key[pygame.K_e]:
                        self.attack_type = 2
            
            if self.player == 2:
                #Movement - WASD for Player 1, Arrow Keys for Player 2
                if key[pygame.K_j]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_l]:
                    dx = speed
                    self.running = True
                #Jump
                if key[pygame.K_i] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #Attack
                if  key[pygame.K_u] or key[pygame.K_o]:
                    self.attack(surface, target)
                    #determine which attack was used
                    if key[pygame.K_u]:
                        self.attack_type = 1
                    if key[pygame.K_o]:
                        self.attack_type = 2
        
        #Gravity
        self.vel_y += gravity
        dy += self.vel_y

        #Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 113:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 113 - self.rect.bottom
        
        #Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #Apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        #Update player position
        self.rect.x += dx
        self.rect.y += dy
    
    #Handle animation updates
    def update(self):
        #Check what action the player's doing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#6: Death
        elif self.attacking == True:
            if self.hit == True:
                self.update_action(5)#5: Hit
            if self.attack_type == 1:
                self.update_action(3)#3: Attack 1
            elif self.attack_type == 2:
                self.update_action(4)#4: Attack 2
            elif self.jump == True:
                self.update_action(2)#2: Jump
            elif self.running == True:
                self.update_action(1)#1: Run
            else:
                self.update_action(0)#0: Idle
        
        animation_cooldown = 50
        #Update image
        self.image = self.animation_list[self.action][self.frame_index]
        #Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #If the player is dead then end the animation
            #if self.alive == False:
            #    self.frame_index = len(self.animation_list[self.action]) - 1
            self.frame_index = 0
            #Check if an attack was made
            if self.action == 3 or self.action == 4:
                self.attacking = False
                self.attack_cooldown = 50
            #Check if damage was taken
            if self.action == 5:
                self.hit = False
                #If the player was in the middle of an attack, then the attack's stopped
                #self.attacking = False
                #self.attack_cooldown = 20
    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    
    def update_action(self, new_action):
        #Check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        image = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(image, (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))
