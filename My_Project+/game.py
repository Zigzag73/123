import pygame as pg
import random as r
import math
import sys
pg.mixer.pre_init(44100,-16,1,512)
pg.init()

#змінні:
FPS = 60
aspect_ratio = 1.8
screen_info = (((pg.display.Info()).current_h)*aspect_ratio,(pg.display.Info()).current_h)
x_update = 0
y_update = 0
wave_number = 0
wave_number2 = 0
wave_number3 = 1
zombi_kill = 0
center_screen = [screen_info[0]//2,screen_info[1]//2]
h1 = True

speed_player = 5
x = -100 
y = -100
fon1 = pg.transform.scale(pg.image.load("fon1.png"),(5000,5000))
#вікно:
screen = pg.display.set_mode(screen_info,pg.FULLSCREEN)
pg.display.set_caption("My Game")
virtual_screen = pg.Surface(screen_info)

clock = pg.time.Clock()#FPS

helicopter = pg.transform.scale(pg.image.load("helicopter.png"),(720,320))
x_h = 10000
y_h = 2500
h = pg.mixer.Sound("helicopter_sound.ogg")
s = pg.mixer.Sound("recharge_sound.ogg")
pg.mixer.music.load("step_sound.ogg")

# хітбокси
class Area:
    def __init__(self, screen, x, y, w, h,color = (100,100,0)):
        self.rec = pg.Rect(x, y, w, h)
        
        self.color =color
        self.screen = screen
    
    def draw_hitbox(self):
        pg.draw.rect(self.screen, self.color, self.rec)
    
    def set_text(self, text):
        f = pg.font.Font(None, 30)
        self.text = f.render(str(text), True, (255,255,255))
        self.screen.blit(self.text , (self.rec.x , self.rec.y))
    
    def set_text2(self, x, y, text, size_font = 50 ,color = (255,255,255)):
        f = pg.font.Font(None, size_font)
        self.text = f.render(text, True, color)
        self.screen.blit(self.text , ( x, y))

class Menu:
    def __init__(self,display,font = None,type = 30,color_text = (255,255,255)):
        self.text = []
        self.text_rect = []
        self.font = pg.font.Font(font, type)
        self.color_text = color_text
        self.display = display
        self.nomber_menu = -1
    
    def create_button(self,text = "", rect = (0,0,0,0)):
        text1 = self.font.render(text, True, self.color_text)
        rec = pg.Rect(rect)
        rec2 = text1.get_rect()
        self.text.append(text1)
        self.text_rect.append(pg.Rect(rec.x,rec.y,rec2.w,rec2.h))  
    
    def create_button2(self,pictures, rect = (0,0,0,0)):
        text1 = pg.transform.scale(pictures,(rect[2],rect[3]))
        rec = pg.Rect(rect)
        self.text.append(text1)
        self.text_rect.append(pg.Rect(rec.x,rec.y,rec.w,rec.h))  
        
    def select(self):
        x,y= pg.mouse.get_pos()
        for i in range(len(self.text)):
            if pg.Rect.collidepoint(self.text_rect[i],(x,y))  :
                self.nomber_menu = i
                return i
            
    def draw_menu (self,color_rec = (-1,-1,-1)):
        for i in range(len(self.text)):
            if self.nomber_menu != -1 :
                
                pg.draw.rect(self.display,color_rec,self.text_rect[self.nomber_menu])
            self.nomber_menu = -1 
            self.display.blit(self.text[i] , (self.text_rect[i].x , self.text_rect[i].y))
            
class Interface(Area):         
    def __init__(self,screen,x,y,w,h,herro,image_HP,image_inventory):
        super().__init__(screen,x,y,w,h)
        self.herro = herro
        self.image_hp = pg.transform.scale(pg.image.load(image_HP),(screen_info[0]//10,screen_info[1]//8))
        self.inventory = pg.transform.scale(pg.image.load(image_inventory),(screen_info[0]//6,screen_info[1]//8))
        self.inventory.set_alpha(200)
        
    def draw(self):
        x,y = self.image_hp.get_size()
        x1,y1 = self.inventory.get_size()
        self.screen.blit(self.image_hp,(screen_info[0]-x,0))
        self.set_text2(screen_info[0]-(x-(x//3)),30,str(int(self.herro.health)),60,(100,0,0))
        self.screen.blit(self.inventory,(screen_info[0]-x-x1,0))
        if len(self.herro.inventory) >0:
            self.screen.blit(pg.transform.scale(self.herro.inventory[self.herro.selected_subject].image_drop,(x1-30,y1-30)),(screen_info[0]-x-x1+15,0+15))
        self.set_text2(screen_info[0]//2,30,"Хвиля: "+str(wave_number),60,(0,0,0))
      
class Note(Area):      
        def __init__(self, screen, x, y, w, h, text, note_image):
            super().__init__(screen, x, y, w, h, color=(100, 100, 0))
            self.image = pg.transform.scale(pg.image.load(note_image),(w,h))
            self.text1 = text
    
        def  draw(self):
            self.screen.blit(self.image,(self.rec.x,self.rec.y))
        
        def update(self):
            posx,posy = pg.mouse.get_pos()
            self.rec.x += x_update
            self.rec.y += y_update
            self.draw()
            if self.rec.collidepoint(posx,posy):
                self.set_text2(self.rec.x+self.rec.h,self.rec.y,self.text1,30,(0,0,0))
            
          
class Herro(Area):
    def __init__(self,screen,x,y,w,h,pictures_herro):
        super().__init__(screen,x,y,w,h)
        self.original_image = pg.transform.scale(pg.image.load(pictures_herro),(w,h))
        self.image = self.original_image
        self.inventory = [] 
        self.selected_subject = 0
        self.health = 50
    
    def draw(self):
        
        self.screen.blit(self.image,(self.rec.x,self.rec.y))
   
         
         
    def rotate_mouse(self):
        directon = pg.mouse.get_pos() - pg.math.Vector2(self.rec.x + self.rec.w//2,self.rec.y + self.rec.h//2)
        angle = directon.as_polar()
        self.image = pg.transform.rotate(self.original_image,-angle[1]-90)
        
        self.rec = self.image.get_rect(center = self.rec.center)
       
    def rotate(self,goal):
        directon = (goal.rec.x,goal.rec.y) - pg.math.Vector2(self.rec.x + self.rec.w//2,self.rec.y + self.rec.h//2)
        angle = directon.as_polar()
        self.image = pg.transform.rotate(self.original_image,-angle[1]-90)
        self.rec = self.image.get_rect(center = self.rec.center)       

    def drop(self):       
        if len(self.inventory) != 0 :
            self.inventory[self.selected_subject].picked_upp = False
            self.inventory[self.selected_subject].rec.x = self.rec.x
            self.inventory[self.selected_subject].rec.y = self.rec.y-70
            
            weapon.append(self.inventory[self.selected_subject])
            self.inventory.remove(self.inventory[self.selected_subject])
            self.selected_subject -= 1
        #self.inventory.remove(self.selected_subject)
        
       
       
# зброя            
class Gun(Area):
    def __init__(self, screen, name,x, y, w, h,pictures_gun,pictures_drop_gun,ganer,max_magazine,speed_recharge,
                 size_bullet_x,size_bullet_y,speed_bullet,rapid_bullet,damage,pictures_bullet,sound):
        super().__init__(screen,x,y,w,h)
        self.bullet = [Bullet(screen,screen_info[0]//2,screen_info[1]//2,size_bullet_x,size_bullet_y,speed_bullet,rapid_bullet,damage,pictures_bullet,self)]
        self.original_image = pg.transform.scale(pg.image.load(pictures_gun),(w,h))
        self.image = self.original_image
        self.image_drop = pg.image.load(pictures_drop_gun)
        self.sound = pg.mixer.Sound(sound)
        
        self.speed_recharge = speed_recharge
        self.max_magazine = max_magazine
        self.magazine = self.max_magazine
        self.magazine_ = self.magazine
        self.name = name
        self.ganer = ganer
        self.picked_upp = False
        
    def draw(self):
        self.screen.blit(self.image,(self.rec.x,self.rec.y)) 
    
    def fire(self):
        if self.magazine <= self.max_magazine and self.magazine != 0 :
            if self.bullet[0].fire() :
                self.magazine -= 1
                self.sound.play()
            if self.magazine == 0 :
                self.magazine_ = 0
                
        else:
            self.magazine_ += self.speed_recharge
            if self.magazine_ >= self.max_magazine:
                self.magazine = self.max_magazine              
                s.play()     
                
    #def recharge(self):   
        
    def rotate_mouse(self):
        directon = pg.mouse.get_pos() - pg.math.Vector2(self.rec.x + self.rec.w//2,self.rec.y + self.rec.h//2)
        angle = directon.as_polar()
        self.image = pg.transform.rotate(self.original_image,-angle[1]-90)
        
        self.rec = self.image.get_rect(center = self.ganer.rec.center) 
    def picked_up(self):
        self.rec.x = self.ganer.rec.x
        self.rec.y = self.ganer.rec.y
        self.fire()
        self.rotate_mouse()
    def spawn_gun(self):
        if self.picked_upp != True:    
            self.rec.x += x_update
            self.rec.y += y_update
            self.screen.blit(self.image_drop,(self.rec.x,self.rec.y))
            if len(self.ganer.inventory) < 2: 
                if self.ganer.rec.colliderect(self.rec) :
                    s.play()
                    self.rec.x = self.ganer.rec.x
                    self.rec.y = self.ganer.rec.y
                    self.ganer.inventory.append(self) 
                    self.picked_upp = True
                    return True
        #else:
            #self.rotate_mouse()
            #self.fire()
            #self.draw()

    
                     
             
         
    def update(self):
        self.rotate_mouse()
        self.fire()  
        self.draw()                
        

# клас куль
class Bullet(Area):
    def __init__(self, screen, x, y, w, h,speed,rapid_fire ,damage,pictures_bullet,gan):
        super().__init__(screen,x,y,w,h)
        self.original_bullet = pg.transform.scale(pg.image.load(pictures_bullet),(w,h))
        self.image_bullet = self.original_bullet
        
        self.damage = damage
        self.speed = speed
        self.pos_mouse = pg.Rect(screen_info[0]//2,screen_info[1]//2,10,10)
        
        self.ganer = gan
        self.rapid_fire = rapid_fire
        self.f = False
       
        
    def draw(self):
        self.screen.blit(self.image_bullet,(self.rec.x,self.rec.y)) 
           
    def fire(self):   
        s = self.speed
        mouse_down = pg.mouse.get_pressed()
        
        if mouse_down[0]  :#>= 10:
            self.f = True

        if self.f == True  : 
            if self.rec.x == self.ganer.rec.centerx and self.rec.y == self.ganer.rec.centery:
                #scatter = [r.randint(-self.scatter1,self.scatter1),r.randint(-self.scatter1,self.scatter1)]
                self.pos_mouse.x,self.pos_mouse.y = pg.mouse.get_pos()
                #self.pos_mouse.x += scatter[0]
                #self.pos_mouse.y += scatter[1]
                self.rec.x=self.ganer.rec.centerx
                self.rec.y=self.ganer.rec.centery
                
                directon = pg.mouse.get_pos() - pg.math.Vector2(self.rec.x + self.rec.w//2,self.rec.y + self.rec.h//2)
                angle = directon.as_polar()
                self.image_bullet = pg.transform.rotate(self.original_bullet,-angle[1]-90)
                self.rec = self.image_bullet.get_rect(center = self.rec.center)
                
            distanse1 = math.sqrt((self.rec.x-self.pos_mouse[0])**2
                                  + (self.rec.y-self.pos_mouse[1])**2)
            if self.rec.colliderect(self.pos_mouse) != True:#distanse1 != 0:
                if distanse1 < self.speed/2:
                    s = 1
                self.rec.x += s*(self.pos_mouse[0]-self.rec.x)/distanse1
                self.rec.y += s*(self.pos_mouse[1]-self.rec.y)/distanse1
                
                self.draw()    
            else :
                self.pos_mouse.x,self.pos_mouse.y = pg.mouse.get_pos()
                self.rec.x=self.ganer.rec.centerx
                self.rec.y=self.ganer.rec.centery
                self.f = False
                return True
            for i in range(len(zombis)):
                if self.rec.colliderect(zombis[i].rec):
                    zombis[i].health -= self.damage
                    self.pos_mouse.x,self.pos_mouse.y = pg.mouse.get_pos()
                    self.rec.x=self.ganer.rec.centerx
                    self.rec.y=self.ganer.rec.centery
                    self.f = False
                    return True

        
# клас монстрів
class Monsters(Area):
    def __init__(self, screen, x, y, w, h, pictures, speed,health,color=(100, 100, 0)):
        super().__init__(screen, x, y, w, h, color)
        self.original_image = pg.transform.scale(pg.image.load(pictures),(w,h))
        self.image = self.original_image
        self.speed = speed
        self.health = health
    
    def draw(self):
        self.screen.blit(self.image,(self.rec.x,self.rec.y))    
    def attack_target(self,target, damage = 0.1, radius_attack = 500):
        s = self.speed
        distanse1 = math.sqrt((self.rec.x-target.rec.x)**2
                            + (self.rec.y-target.rec.y)**2)
        if distanse1 < radius_attack:    
            if self.rec.colliderect(target.rec) != True:  #distanse1 != 0:
                self.rec.x += s*(target.rec.x-self.rec.x)/distanse1
                self.rec.y += s*(target.rec.y-self.rec.y)/distanse1
            else:
                target.health -= damage
        
        directon = (target.rec.x,target.rec.y) - pg.math.Vector2(self.rec.x + self.rec.w//2,self.rec.y + self.rec.h//2)
        angle = directon.as_polar()
        
        self.image = pg.transform.rotate(self.original_image,-angle[1]-90)
        self.rec = self.image.get_rect(center = self.rec.center)
        
        self.draw() 
        #self.time_out+=1   
    
 
        
class Ground_cover(Area):
    def __init__(self,screen,x,y,w,h,pictures):
        super().__init__(screen,x,y,w,h)
        self.image = pg.transform.scale(pg.image.load(pictures),(self.rec.w,self.rec.h))
    
    def draw(self):
        self.screen.blit(self.image,(self.rec.x,self.rec.y))
        
    def update(self):
        self.rec.x += x_update
        self.rec.y += y_update
        self.draw()
class Ground_cover_big(Ground_cover):
    def __init__(self, screen, x, y, w, h, pictures):
        super().__init__(screen, x, y, w, h, pictures)
        self.pictures = pg.transform.scale(pg.image.load(pictures),(w,h))
        self.pictures.set_alpha(100)
        
    def update(self):
        self.rec.x += x_update
        self.rec.y += y_update
        if player.rec.colliderect(self.rec) :  
           
           self.screen.blit(self.pictures,(self.rec.x,self.rec.y))
        else:
           
           self.screen.blit(self.image,(self.rec.x,self.rec.y))
class Usable(Area):
    def __init__(self, screen, x, y, w, h, image, properties):
        super().__init__(screen, x, y, w, h, color=(100, 100, 0))
        self.image = pg.transform.scale(pg.image.load(image),(self.rec.w,self.rec.h))
        self.properties = properties
       
    def draw(self):
        self.rec.x += x_update
        self.rec.y += y_update
        self.screen.blit(self.image,(self.rec.x,self.rec.y))
    
   
        
    
            
        
    
    
    
    
    
    
player = Herro(virtual_screen,screen_info[0]//2,screen_info[1]//2,32,55,"player/player.png")
player_interface = Interface(virtual_screen,0,0,0,0,player,"HP.png","the_cell.png")






loot = []
ground_cover = []
ground_big = []
zombis = []
for i in range(20):
    ground_cover.append(Ground_cover(virtual_screen,r.randint(-100,2000),r.randint(-100,2000),20,20,"weed.png"))
for i in range(10):    
    ground_big.append(Ground_cover_big(virtual_screen,r.randint(1000,4500),r.randint(1000,4500),100,100,"tree.png"))
for i in range(3):
    zombis.append(Monsters(virtual_screen,r.randint(-100,1000),r.randint(-100,1000),50,50,
                           "monsters/zombis/zombi/zombi1.png",1,10))  
weapon = [Gun(virtual_screen,"pistol",r.randint(100,1000),r.randint(100,1000),32,55,"player/Gun/pistol/pistol.png",
             "player/Gun/pistol/pistol_drop.png",player,10,0.1,5,10,10,20,2,"bullet.png","fire.ogg"),
          Gun(virtual_screen,"akm",ground_big[-1].rec.centerx,ground_big[-1].rec.centery,32,55,"player/Gun/akm/akm.png",
             "player/Gun/akm/akm_drop.png",player,30,0.5,10,20,25,1,4,"bullet.png","fire3.ogg"),
          Gun(virtual_screen,"r15",r.randint(2400,2500),r.randint(2400,2600),32,55,"player/Gun/r15/r15.png",
             "player/Gun/r15/r15_drop.png",player,30,0.5,8,16,30,0.5,3,"bullet.png","fire2.ogg")    ]

for i in range(2):
    loot.append(Usable(virtual_screen,r.randint(2400,2500),r.randint(2400,2600),30,30,"first_aid_kit.png",50))
    

ground_cover.append(Note(virtual_screen,player.rec.x+100,player.rec.y+100,20,20,"Знайдіть вертолітний майданчик","note.png"))
ground_cover.append(Note(virtual_screen,2500,2600,20,20,"Відбийте орду зомбі","note.png"))    


def update_player():
    player.rotate_mouse()
    #pistol.rotate_mouse()
   
    if len(player.inventory) > 0:
        player.inventory[player.selected_subject].update()
    #pistol.bullet.fire()
    player.draw()
    player_interface.draw()
    
    if player.health > 100:
        player.health -= 0.05
    if player.health<=0:
        pg.quit()
        sys.exit()
    
def update_loot():
    for i,e in enumerate(weapon):
        if e.spawn_gun() :
            weapon.remove(e)
    
    for i,e in enumerate(loot):
        if player.rec.colliderect(e.rec) :
            player.health += e.properties
            loot.remove(e)
        e.draw()    
    
def update_ground_cover():
    for i in range(len(ground_cover)):
        ground_cover[i].update()
def update_ground_big():
    for i in range(len(ground_big)):
        ground_big[i].update()
def update_monsters():
    global zombi_kill,wave_number,wave_number2
    for i,e in enumerate(zombis):#промальовка монстрів
        e.rec.x += x_update
        e.rec.y += y_update
        
        e.attack_target(player,0.1,1000)   
        #e.draw_hitbox()
        e.draw()
        if len(player.inventory) == 0:
            player.selected_subject = 0
        if len(player.inventory) >0:  
            if player.inventory[player.selected_subject].bullet[0].rec.colliderect(e.rec):
                e.health -=player.inventory[player.selected_subject].bullet[0].damage
        if e.health <=0:
            zombi_kill +=1
            zombis.remove(e)
def spawn_monster(nombers):            
    for i in range(nombers): 
        a = r.randint(1,4)
        if a == 1:
            x = r.randint(1500,1700)
            y = r.randint(800,1000)
        if a == 2:
            x = r.randint(-200,0)
            y = r.randint(-200,0)
        if a == 3:
            x = r.randint(1500,1700)
            y = r.randint(-200,0)
        if a == 4:
            x = r.randint(-200,0)
            y = r.randint(800,1000)
        b = r.randint(1,2)   
        if b == 1:
            zombis.append(Monsters(virtual_screen,x,y,50,50,"monsters/zombis/zombi/zombi1.png",1,10)) 
        else:
            zombis.append(Monsters(virtual_screen,x,y,26,32,"monsters/zombis/speed_zombi/speed_zombi1.png",3,5)) 
    return False

def menu1():
    menu1 = Menu(virtual_screen,"1-blackmoor-let-plain103.ttf",100)  
    menu1.create_button("Грати",(100,100,300,100)) 
    menu1.create_button("Вихiд",(100,250,600,100)) 
 
    runing1 = True
    while runing1 :
        a = menu1.select()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                runing1 = not runing1
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if (a == 0) :
                    runing1 = False
                    print("i i i  ха")
                    game_start()
                if (a == 1):
                    runing1 = False
                    pg.quit()
                    sys.exit()
                
        virtual_screen.fill((0,50,0,0.5))
        #virtual_screen.blit(menu_bd,(0,0))
        #virtual_screen.blit(icon,(0,0))
        
        menu1.draw_menu((100,100,0))
        screen.blit(virtual_screen,(0,0)) 
        pg.display.update()
        clock.tick(FPS)
    
def game_start():
    global x,y,x_update,y_update,wave_number,wave_number2,wave_number3 ,h1,h ,x_h,y_h,helicopter 
    
    running = True
    while running:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:# Вихід на крестик
                running = False
                pg.quit()
                sys.exit()
  
                
            if event.type == pg.KEYDOWN:# Натискання клавіш
                pg.mixer.music.play()
                if event.key == pg.K_ESCAPE:#  Вихід на ESCAPE
                    running = False
                    menu1()
                    #pg.quit()
                    #sys.exit()
                # перміщення світу навколо гравця
                if event.key == pg.K_w or event.key == pg.K_UP:
                    y_update = speed_player
                    
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    y_update = -speed_player
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    x_update = -speed_player
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    x_update = speed_player
                #викинути предмет:
                if event.key == pg.K_g:
                    player.drop()
            if event.type == pg.KEYUP:
                pg.mixer.music.stop()
                if event.key == pg.K_w:
                    y_update = 0
                if event.key == pg.K_s:
                    y_update = 0
                if event.key == pg.K_d:
                    x_update = 0
                if event.key == pg.K_a:
                    x_update = 0
               
                
                if event.key == pg.K_1:
                    player.selected_subject = 0
                elif event.key == pg.K_2:
                    if len(player.inventory) >=2:
                        player.selected_subject = 1    
                elif event.key == pg.K_3:
                    if len(player.inventory) >=3:
                        player.selected_subject = 2  
                elif event.key == pg.K_4:
                    if len(player.inventory) >=4:
                        player.selected_subject = 3  

        virtual_screen.fill((0,50,0))        
        
        virtual_screen.blit(fon1,(x,y))
        if x >= center_screen[0] :
            if x_update > 0:
                x_update = 0
        elif x+5000 <= center_screen[0]:
            if x_update < 0:
                x_update = 0
        if y >= center_screen[1] :
            if y_update > 0:
                y_update = 0
        elif y+5000 <= center_screen[1]:
            if y_update < 0:
                y_update = 0
        
        x_h += x_update
        y_h += y_update
        
        x += x_update
        y += y_update
        update_ground_cover()
        update_monsters()
        update_loot()
        update_player()
        update_ground_big()
        pos = pg.mouse.get_pos()
        if ground_cover[-1].rec.collidepoint(pos):
            if wave_number <= 1 and wave_number2 == 0:    
                wave_number =1
                spawn_monster(wave_number)
                wave_number2 = 1
        elif zombi_kill >= wave_number3 and wave_number2 == wave_number3 and wave_number3 != 10 :
            wave_number =wave_number3+1 
            spawn_monster(wave_number)
            wave_number2 = wave_number3+1
            wave_number3 +=1
        elif  len(zombis) <=3 and wave_number3 == 10 :
           
            player.set_text2(500,500,"Перемога",100,(100,0,0))
            virtual_screen.blit(helicopter,(x_h,y_h))
            if x_h >= ground_cover[-1].rec.x-500:
                x_h -= 10
               
           
            if h1 ==True    :
                h.play()
                h1 = False
            
      
   
        screen.blit(virtual_screen,(0,0))    
        clock.tick(FPS)
        pg.display.update()

menu1()
#game_start()


