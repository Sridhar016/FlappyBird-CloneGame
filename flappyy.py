import pygame
from pygame.locals import*
import random
pygame.init()

clock=pygame.time.Clock()
fps=20

screen_height=400
screen_width=400

#game variables
ground_scroll=0
scroll_spedd=4
flying=False
game_over=False
pipe_gap=70
pipe_freq=1500
last_pipe=pygame.time.get_ticks()-pipe_freq
score=0
pass_pipe=False
high_score=0

screen=pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Flappy bird")



#define colours
white = (255,255,255)
black=(0,0,0)
#sprites
bg=pygame.image.load("E:/_python/flappy/images/bg1.png")
ground=pygame.image.load("E:/_python/flappy/images/ground1.png")
button_image=pygame.image.load("E:/_python/flappy/images/restart1.png")
def draw_text(text,font,txt_col,x,y):
    img=font.render(text,True,txt_col)
    screen.blit(img,(x,y))
def reset_game():
    pipe_group.empty()
    flappy.rect.x=47
    flappy.rect.y=int(screen_height/2)
    score=0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(1,4):
            img=pygame.image.load(f"E:/_python/flappy/images/bird{i}.png")
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0    
        self.clicked=False      
    def update(self):
        if flying==True:
            self.vel+=1
            if self.vel>10:
                self.vel=8
            if self.rect.bottom<325:
                self.rect.y+=int(self.vel)
        if game_over==False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
        
            self.counter+=1
            flap_cooldown=5
            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
                self.image=self.images[self.index]    
class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("E:/_python/flappy/images/pipe1.png")
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y+int(pipe_gap/2)]
    def update(self):
        self.rect.x-=scroll_spedd
        if self.rect.right<0:
            self.kill()
class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action
bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()


flappy=Bird(47,int(screen_height/2))
bird_group.add(flappy)

button=Button((screen_width//2)-45,(screen_height//2)-30,button_image)



run=True
while run:
    clock.tick(fps)
    screen.blit(bg,(0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    
    screen.blit(ground,(ground_scroll,325))
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False
    draw_text(str(score),pygame.font.SysFont('Arial', 30),white,int(screen_width/2),17)
    if game_over==True or game_over==False:
        if score>high_score:
            high_score=score
        draw_text("High score:"+str(high_score),pygame.font.SysFont('Arial', 20),black,10,int((screen_height/2)+150))

    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top<0:
        game_over=True
    if flappy.rect.bottom >=325:
        game_over=True
        flying=False
    if game_over==False and flying==True:
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_freq:
            pipe_height=random.randint(-60,60)
            btm_pipe=pipe(screen_width,int(((screen_height+25)/2)+pipe_height),-1)
            top_pipe=pipe(screen_width,int(((screen_height-25)/2)+pipe_height),1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now
        ground_scroll-=scroll_spedd
        if abs(ground_scroll)>10:
            ground_scroll=0
        pipe_group.update()
    if game_over==True:
        if button.draw()==True:
            game_over=False
            score=reset_game()
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            run=False
        if events.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    pygame.display.update()
pygame.quit()