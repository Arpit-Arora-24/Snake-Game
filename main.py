import pygame,sys
from pygame.locals import *
import time
import random
SIZE=40
BACKGROUND_COLOR = (110, 110, 5)
Target=4
Level=1
sleep_time=0.25
running = True
user_name=''


class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE
        self.draw()



class Snake:
    def __init__(self, surface,length):
        self.length=length
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        


    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]




        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play(-1,2.0)
        self.usernameInput()
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('sylfaen', 60)
        l =  font.render("Snake Game",True, (255, 255, 255))
        self.surface.blit(l, (130, 150))
        font = pygame.font.SysFont('sylfaen', 30)
        l_1 =  font.render("Rules for the game are as follows: ",True, (255, 255, 255))
        self.surface.blit(l_1, (130, 250))
        l_2 = font.render("1) Try To achieve the Target Score as specified in each level.",True, (255, 255, 255))
        self.surface.blit(l_2,(130,300))
        l_3 = font.render("2) Try to remain in the boundaries of the field." ,True, (255, 255, 255))
        self.surface.blit(l_3,(130,350))
        l_4 = font.render("3) Going out of the boundaries will make you lose the game!!" ,True, (255, 255, 255))
        self.surface.blit(l_4,(130,400))
        l_5 = font.render("4) To play the game, press Enter!",True, (255, 255, 255))
        self.surface.blit(l_5,(130,450))
        l_6 = font.render("5)To close the game, press Escape!",True, (255, 255, 255))
        self.surface.blit(l_6,(130,500))
        pygame.display.flip()
        
        temp=True
        global running
        while temp:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        temp=False
                        running = False
                    if event.key == K_RETURN:
                        temp=False

                        self.snake = Snake(self.surface,1)
                        self.snake.draw()
                        self.apple = Apple(self.surface)
                        self.apple.draw()
                elif event.type == QUIT:
                    temp = False
                    running = False

    #taking the username input .....  you tube video link from where i have studied this:https://www.youtube.com/watch?v=Rvcyf4HsWiw
    def usernameInput(self):
        global user_name
        input_rect=pygame.Rect(130,335,440,49)
        color_active=pygame.Color('lightskyblue3')
        color_passive=pygame.Color('gray15')
        color=color_passive
        active=False
        font = pygame.font.SysFont('sylfaen', 40)
        temp2 = True
        font_1 = pygame.font.SysFont('sylfaen', 60)
        font_2 = pygame.font.SysFont('sylfaen', 50)
        l =  font_1.render("Welcome To the Snake Game",True, (255, 255, 255))
        l_1 = font_2.render("Please enter your name below" ,True, (255, 255, 255))

        while temp2:
            
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True 
                        color=color_active
                if event.type==KEYDOWN:
                    if active==True:    
                        if event.key==K_RETURN:
                            temp2=False
                            break
                    
                        if event.key==K_BACKSPACE:
                            user_name=user_name[:-1]
                            
                        else:
                            user_name += event.unicode
                if event.type==QUIT:
                    temp2=False
                              
            self.surface.fill((105, 35, 94))
            self.surface.blit(l, (130, 150))
            self.surface.blit(l_1, (130, 250))
            pygame.draw.rect(self.surface,color,input_rect,2)
            name= font.render(user_name,True, (255, 255, 255))
            input_rect.w=max(100,name.get_width())
            self.surface.blit(name,input_rect)
            pygame.display.flip()
                        

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def is_collision(Self,x1,x2,y1,y2):
        if (x1==x2 and y2>=y1 and y2<y1+SIZE) or (x1==x2 and y1>=y2 and y1<y2+SIZE):
            return True

        if (y1==y2 and x1>=x2 and x1<x2+SIZE) or (y1==y2 and x2>=x1 and x2<x1+SIZE):
            return True

        return False

        

    def display_score(self):
        global Target
        global Level
        global sleep_time
        if self.snake.length == Target:
            self.surface.fill(BACKGROUND_COLOR)
            font = pygame.font.SysFont('sylfaen', 40)
            l =  font.render(f"Congratulations {user_name}!!!",True, (255, 255, 255))
            self.surface.blit(l,(30,270))
            l_1 = font.render(f"You have cleared the Level {Level} of the Snake Game!!",True,(255,255,255))
            self.surface.blit(l_1,(30,320))
            l_2 = font.render("To play the next Level, press Enter!",True, (255, 255, 255))
            self.surface.blit(l_2,(30,370))
            l_3 = font.render("To close the game, press Escape!",True, (255, 255, 255))
            self.surface.blit(l_3,(30,420))
            pygame.display.flip()
            Level += 1
            Target =  4 + (Level-1)*3
            sleep_time = 0.25 - (Level-1)*0.03    #decreasing the sleep time will increase the difficulty of the game.
            self.reset()
            pygame.display.flip()
            temp=True
            global running
            while temp:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            temp=False
                        if event.key == K_ESCAPE:
                            temp=False
                            running= False
                    elif event.type == QUIT:
                        temp = False
                        running = False


        font = pygame.font.SysFont('arial',25)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))
        l_1 = font.render(f"Level: {Level}",True,(200,200,200))
        self.surface.blit(l_1,(85,10))
        l_2 = font.render(f"Target Score: {Target}",True,(200,200,200))
        self.surface.blit(l_2,(420,10))
        pygame.display.flip()

    


    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        

         # snake eating apple scenario
        if self.is_collision(self.apple.x,self.snake.x[0],self.apple.y,self.snake.y[0]):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        #snake crossing the boundary
        if self.snake.x[0]==1000 or self.snake.y[0]==800 or self.snake.x[0]<0 or self.snake.y[0]<0:
            sound = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(sound)
            raise "Collision Occured"

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.x[i], self.snake.y[0], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Collision Occured"

        
            



    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()


    def run(self):
        # running = True
        global running
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()
                        

                elif event.type == QUIT:
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(sleep_time)



if __name__ == '__main__':
    game = Game()
    game.run()



    #https://youtu.be/MNewWRtFINc  ---> video to convert .py to .exe
    #https://youtu.be/7xP5FJasXfk  ---> video to convert .exe to setup/installer.