
import pygame
import os
import random

pygame.init()

pygame.mixer.music.set_volume(0.06)
musica_de_fundo = pygame.mixer.music.load(os.path.join("musicas","The Long Ryders - Run Dusty Run.mp3"))
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound(os.path.join("musicas","smw_lost_a_life.wav"))
barulho_colisao.set_volume(2)


pygame.display.set_caption(" Projetos de jogos Digitais")

screen_H = 700
screen_W = 500

# Imagens
canvas = pygame.display.set_mode((screen_H, screen_W))

CORRIDA =[pygame.image.load(os.path.join("Imagens\Baixo", "1.png")),
          pygame.image.load(os.path.join("Imagens\Baixo", "2.png")),
          pygame.image.load(os.path.join("Imagens\Baixo", "3.png")),]

BAIXO = [pygame.image.load(os.path.join("Imagens\Baixo", "BaixoDuck1.png")),
         pygame.image.load(os.path.join("Imagens\Baixo", "BaixoDuck1.png"))]

NUVEM = pygame.image.load(os.path.join("Imagens\Outras", "Nuvem.png"))

OBSTACULO1 = [pygame.image.load(os.path.join("Imagens\Obstaculos", "Obstaculo1.png")),
                  pygame.image.load(os.path.join(
                      "Imagens\Obstaculos", "Obstaculo2.png")),
                  pygame.image.load(os.path.join("Imagens\Obstaculos", "Obstaculo3.png"))]

OBSTACULOS = [pygame.image.load(os.path.join("Imagens\Obstaculos", "Obstaculos1.png")),
                  pygame.image.load(os.path.join("Imagens\Obstaculos", "Obstaculos2.png")),
                  pygame.image.load(os.path.join("Imagens\Obstaculos", "Obstaculos3.png"))]

OBSTACULOB = [pygame.image.load(os.path.join("Imagens\Obstaculos2", "Obstaculob1.png")),
                 pygame.image.load(os.path.join("Imagens\Obstaculos2", "Obstaculob2.png"))]

ROAD = pygame.image.load(os.path.join("Imagens\Outras", "Track.png"))

START = pygame.image.load(os.path.join("Imagens\Outras", "Start.png"))
         
EXIT = pygame.image.load(os.path.join("Imagens\Outras", "exit.png"))

EXIT_btn_restart = pygame.image.load(os.path.join("Imagens\Outras", "exitbtn.png"))

RESET = pygame.image.load(os.path.join("Imagens\Outras", "Reset.png"))

GAME_OVER = pygame.image.load(os.path.join("Imagens\Outras", "GameOver.png"))

white = (255,255,255)
black = (0,0,0)



#=================================================== Jogador ========================================
class player:     # Classe Jogador 
    pos_x = 15
    pos_y = 330

    def __init__(self):
        # image
        self.run_img = CORRIDA
        self.baixo_img = BAIXO 
        self.jump = False
        self.run = True
        self.baixo = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.baixo_rect = self.image.get_rect()
        
        self.do_baixo = 30
        self.do_jump = 7
        self.jump_vel = 7

        self.baixo_rect.x = player.pos_x
        self.baixo_rect.y = player.pos_y
        
    def update(self, keys):
        if self.run:
            self.run_act()
        if self.jump:
            self.jump_act()
            
        if self.baixo:
            self.baixo_act()    

        if self.step_index >= 10:
            self.step_index = 0


        if keys[pygame.K_SPACE] and not self.jump:
            self.run = False
            self.jump = True
            self.baixo = False
        elif keys[pygame.K_DOWN] and not self.jump:
            self.run = False
            self.jump = False
            self.baixo = True
        elif not self.jump or self.baixo:
            self.run = True
            self.jump = False
            self.baixo = False

    def run_act(self):
        global game_speed
        self.image = self.run_img[self.step_index // 5]
        self.baixo_rect = self.image.get_rect()
        self.baixo_rect.x = player.pos_x
        self.baixo_rect.y = player.pos_y
        self.step_index += int(game_speed/10)

    def jump_act(self):
        if self.jump:
            self.baixo_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.6
        if self.jump_vel < - self.do_jump:
            self.jump = False
            self.jump_vel = self.do_jump


    def baixo_act(self):
        global game_speed
        self.image = self.baixo_img[self.step_index // 5]
        self.baixo_rect = self.image.get_rect()
        self.baixo_rect.x = player.pos_x
        self.baixo_rect.y = player.pos_y + self.do_baixo    
        self.step_index += int(game_speed/10)


    def draw(self, canvas):
        canvas.blit(self.image, self.baixo_rect)

        
#======================================================== Classe de Pontuação ==========================================
class score:
    def __init__(self):
        self.points = -1
        self.count = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def update(self):
        if(self.count % 5 == 0 and self.count > 1):
            self.points += 11
        else:
            self.points += 1
        if (self.count % 10 == 0 and self.count >= 1):
            global game_speed
            game_speed += 1
        self.count += 1

    def draw(self,night=False):
        if (night):
            text = self.font.render("Potuação : " + str(self.points), True, white)
        else : 
            text = self.font.render("Pontuação : " + str(self.points), True, black)
        textRect = text.get_rect()
        textRect.center = (100, 40)
        canvas.blit(text, textRect)

class nuvem:
    def __init__(self):
        self.x = screen_H + random.randint(500, 800)
        self.y = random.randint(50, 100)
        self.image = NUVEM
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < - self.width:
            self.x = screen_W + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

class bg:
    bg_x = 0
    bg_y = 400

    def __init__(self):
        self.image_width = ROAD.get_width()

    def update(self):
        canvas.blit(ROAD, (bg.bg_x, bg.bg_y))
        canvas.blit(ROAD, (self.image_width + bg.bg_x, bg.bg_y))
        if bg.bg_x <= -self.image_width:
            canvas.blit(ROAD, (self.image_width + bg.bg_x, bg.bg_y))
            bg.bg_x = 0
            
        bg.bg_x -= game_speed
        

#================================================ Classe de Obstáculos ============================================
class obstaculo:
    def __init__(self, image, tipe):
        self.image = image
        self.type = tipe
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_W * 2

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            rintangan.pop() 

    def draw(self, canvas):
        canvas.blit(self.image[self.type], self.rect)
        

class obstaculo1(obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350

class obstaculos(obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class obstaculob(obstaculo):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0
        

    def draw(self, canvas):
        if self.index >= 9:
            self.index = 0
        canvas.blit(self.image[self.index//5], self.rect)
        self.index += 1
        


#============================================================= Classe Menu=========================================
class menu:
    def __init__(self):
        self.start_rect = START.get_rect()
        self.start_rect.x = 20
        self.start_rect.y = 40

        self.exit_rect = EXIT.get_rect()
        self.exit_rect.x = 265
        self.exit_rect.y = 430


    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        run = False
                        return True
                        
                    elif self.exit_rect.collidepoint(event.pos):
                        run = False
                        return False
                        

            canvas.fill((255, 255, 255))
            canvas.blit(START, self.start_rect)
            canvas.blit(EXIT, self.exit_rect)
        
            pygame.display.update()

            
#========================================================Classe start ====================================
class start:
    def __init__(self):
        self.trex = player()
        self.Nuvem = nuvem()
        self.Background = bg()
        self.skor = score()
        self.menu = menu()
        global game_speed, rintangan
        game_speed = 10
        rintangan = []
    
    def run(self):
        self.run = True
        while self.run:
            clock = pygame.time.Clock()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        stop = pause()
                        stop.run()

            keys = pygame.key.get_pressed()

            if (self.skor.points // 10 % 2 == 1):
                canvas.fill(black)
                self.skor.draw(True)
            else : 
                canvas.fill(white)
                self.skor.draw()
            self.trex.draw(canvas)
            self.trex.update(keys)

            if len(rintangan) == 0:
                if random.randint(0, 1) == 1:
                    rintangan.append(obstaculo1(OBSTACULO1))
                    self.skor.update()
                elif random.randint(0, 1) == 1:
                    rintangan.append(obstaculos(OBSTACULOS))
                    self.skor.update()
                elif random.randint(0, 1) == 1:
                    rintangan.append(obstaculob(OBSTACULOB))
                    self.skor.update()
                    
            for i in rintangan:
                i.draw(canvas)
                i.update()
                if self.trex.baixo_rect.colliderect(i.rect):  
                    restart = game_over(self.skor.points)
                    self.run = restart.run()
                    

            self.Background.update()
            self.Nuvem.draw(canvas)
            self.Nuvem.update()
                
            clock.tick(30)
            pygame.display.update()

        pygame.quit()

        


#============================================================  CLasse FIm de JOgo ===================        
class game_over:
    def __init__(self,skor) :
        font = pygame.font.Font('freesansbold.ttf', 20)
        if (skor < 10):
            self.text = font.render("Pontuação do Jogador : " + str(skor), True, (0, 0, 0))
        else:
            self.text = font.render("Pontuação do Jogador : " + str(skor), True, (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (350, 150)
    
        self.restart_rect = RESET.get_rect()
        self.restart_rect.x = 200
        self.restart_rect.y = 370

        self.exit_rect = EXIT_btn_restart.get_rect()
        self.exit_rect.x = 400
        self.exit_rect.y = 375
        self.run()
        

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_rect.collidepoint(event.pos):
                        gameplay = start()
                        gameplay.run()
                        run = False
                        
                    elif self.exit_rect.collidepoint(event.pos):
                        run = False
                        pygame.quit()
            
            barulho_colisao.play()               

            canvas.fill(white)
            canvas.blit(EXIT_btn_restart, self.exit_rect)
            canvas.blit(self.text, self.textRect)
            canvas.blit(GAME_OVER, (170, 200))
            canvas.blit(RESET, self.restart_rect)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    Menu = menu()
    gameplay = start()
    play = Menu.run()
    if play : 
        gameplay.run()
    else :
        pass
