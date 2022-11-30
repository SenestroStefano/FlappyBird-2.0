from __modules__ import *
import globals as G

class Bird():
   def __init__(self, pos: tuple = (0, 0)):
      dir = "images/bird/"
      
      self.__div = 1.2 * G.Divider
      
      self.pos = (pos[0] * int(G.MoltScreen) / G.Divider, pos[1] * int(G.MoltScreen) / G.Divider)
      
      self.__image = []
      for i in range(2):
         a = py.image.load(dir + "fly" + str(i) + ".png").convert_alpha()
         a = py.transform.scale(a, (a.get_width() * int(G.MoltScreen) / self.__div, a.get_height() * int(G.MoltScreen) / self.__div))
         self.__image.append(a)
      
      self.__delay = 0
      
      self.__dead = py.image.load(dir + "dead.png").convert_alpha()
      self.__dead = py.transform.scale(self.__dead, (self.__dead.get_width() * int(G.MoltScreen) / self.__div, self.__dead.get_height() * int(G.MoltScreen) / self.__div))
      
      self.__dead = py.transform.rotate(self.__dead, -20)
      
      self.__color = "Green"
      
      self.__fall_force = 0
      self.__right_force = 0
      
      self.__setMesh()
      self.StartFase = True
      
      
      val = 6
      self.__explosion = []
      for i in range(9):
         a = py.image.load("images/explosion/" + "exp" + str(i) + ".png").convert_alpha()
         a = py.transform.scale(a, (a.get_width() * int(G.MoltScreen) * val, a.get_height() * int(G.MoltScreen) * val))
         self.__explosion.append(a)
         
      self.__delay_expl = -8
      
      self.pos_exp = self.mesh
      
   def RenderDied(self):
      self.__updateFall()   
      self.pos = (self.pos[0] + self.__right_force, self.pos[1] + self.__fall_force)
      
      posy = - 60 * int(G.MoltScreen)
      if self.pos[1] >= G.height + posy:
         self.pos = self.pos[0], G.height + posy
         self.__right_force = 0
         
      G.screen.blit(self.__dead, self.pos)
      
      if self.__delay_expl < len(self.__explosion) -1:
         self.__delay_expl += 2 / G.FPS * G.DeltaTime
         
      if self.__delay_expl > 0 and self.__delay_expl < 0.5:
         self.addForce(forceY = 15, forceX = 30)
      
      if self.__delay_expl >= 0:
         G.screen.blit(self.__explosion[int(self.__delay_expl)], (self.pos_exp.centerx - self.__explosion[int(self.__delay_expl)].get_width()/2, self.pos_exp.centery - self.__explosion[int(self.__delay_expl)].get_height()/2)) 
      
   def __setMesh(self):
      
      var = (7.5, 4, 14, 7.5)
      offset = tuple([i *  int(G.MoltScreen) for i in var])

      self.mesh = py.Rect(
                              self.pos[0] + offset[0] / self.__div, 
                              self.pos[1] + offset[1] / self.__div, 
                              self.__image[0].get_width() - offset[2] / self.__div, 
                              self.__image[1].get_height() - offset[3] / self.__div
                           )
      
   def updateDelay(self):
      self.__delay += 2 / G.FPS * G.DeltaTime
      
      if int(self.__delay) > len(self.__image) - 1:
         self.__delay = 0
      
      
   def preUpdate(self):
      self.StartFase = True
      
      posy = 120 * int(G.MoltScreen) / G.Divider
      
      self.__updateFall()
      
      if self.pos[1] > posy + rand.randint(5, 10) * int(G.MoltScreen) / G.Divider:
         self.__fall_force = -rand.randint(5, 15) * int(G.MoltScreen) / G.DeltaTime / G.Divider
      
      self.updateDelay()
      
      self.pos = (self.pos[0], self.pos[1] + self.__fall_force)

      G.screen.blit(self.__image[int(self.__delay)], self.pos)
      
      
   def addForce(self, forceY: int = 0, forceX: int = 0):
      self.__fall_force = -forceY * int(G.MoltScreen) / G. DeltaTime
      self.__right_force = forceX * int(G.MoltScreen) / G. DeltaTime
   
   def __updateFall(self):
      self.__fall_force += G.Bird_Fall * int(G.MoltScreen) / G.DeltaTime
      
      
   def update(self):
      
      self.StartFase = False
      
      if not G.GameOver:
         self.__updateFall()
         
         self.__setMesh()
         self.updateDelay()
         
         self.pos = (self.pos[0], self.pos[1] + self.__fall_force)
         
         G.screen.blit(self.__image[int(self.__delay)], self.pos)
               
         if G.Debug:
            py.draw.rect(G.screen, self.__color, self.mesh, 1 * int(G.MoltScreen),)
      else:
         self.pos_exp = self.mesh
      

class Tube():
   def __init__(self, posx: int = 0):
      dir = "images/"
      
      self.__min_height = 60 * int(G.MoltScreen) / G.Divider
      self.__max_height = 10 * int(G.MoltScreen) / G.Divider
      self.__space = 70 * int(G.MoltScreen) / G.Divider
      
      self.pos = posx * int(G.MoltScreen), 0
      self.__getNewHeight()
      
      a = py.image.load(dir + "tube.png").convert_alpha()
      a = py.transform.scale(a, (a.get_width() * int(G.MoltScreen) / G.Divider, 
                                 a.get_height() * int(G.MoltScreen) / G.Divider))
      b = py.transform.flip(a, False, True)
      
      self.__image = [a, b]
      
      self.__color = "Red"
      self.__setMesh()
      
      self.__speed = -G.Background_speed * int(G.MoltScreen) / G.DeltaTime
      self.flag_score = True
      
   def __getNewHeight(self):
      self.pos = self.pos[0], rand.randint(int(G.height/2 - self.__max_height), int(G.height - self.__min_height))
      
      
   def __setMesh(self):
      
      var = (1, 1, 1, 1)
      offset = tuple([i *  int(G.MoltScreen) for i in var])

      distance = - (self.__space + self.__image[0].get_height())
      
      self.mesh = [py.Rect(
                              self.pos[0] + offset[0],
                              self.pos[1] + offset[1], 
                              self.__image[0].get_width() - offset[2], 
                              self.__image[1].get_height() - offset[3]
                           ),
                     py.Rect(
                              self.pos[0] + offset[0], 
                              self.pos[1] + (offset[1] + distance), 
                              self.__image[0].get_width() - offset[2], 
                              self.__image[1].get_height() - offset[3]
                           )
                     ]
      
      self.score_area = py.Rect(
                              self.pos[0] + self.__image[0].get_width()/4 + offset[0], 
                              self.pos[1] - self.__space,
                              self.__image[0].get_width() / 2, 
                              self.__space
                           )
      
      
   def update(self):
      
      self.__setMesh()
      
      if not G.GameOver:
         self.pos = (self.pos[0] + self.__speed, self.pos[1])
      
      distance = 0
      for tube in self.__image:
         G.screen.blit(tube, (self.pos[0], self.pos[1] + distance))
         distance = - (self.__space + self.__image[1].get_height())
      
      if G.Debug:
         for i in range(2):
            py.draw.rect(G.screen, self.__color, self.mesh[i], 2 * int(G.MoltScreen),)
         py.draw.rect(G.screen, "Blue", self.score_area, 2 * int(G.MoltScreen),)
      
      dist = G.width / G.Num_tubes
      if self.pos[0] < -dist:
         self.__init__(dist * G.Num_tubes)
         self.__getNewHeight()
      
class Background():
   def __init__(self):
      dir = "images/"
      
      VAL1 = 1.8 * G.Divider
      
      a = py.image.load(dir + "background.png").convert()
      self.__background = py.transform.scale(a, (a.get_width() * int(G.MoltScreen) / VAL1, a.get_height() * int(G.MoltScreen) / VAL1))
      
      b = py.image.load(dir + "base.png").convert()
      self.__base = py.transform.scale(b, (b.get_width() * int(G.MoltScreen) / G.Divider, b.get_height() * int(G.MoltScreen) / G.Divider))
      
      c = py.image.load(dir + "gameover.png").convert_alpha()
      self.__gameover = py.transform.scale(c, (c.get_width() * int(G.MoltScreen) / G.Divider, c.get_height() * int(G.MoltScreen) / G.Divider))
      
      
      self.__speed_base = -G.Background_speed * int(G.MoltScreen) / G.DeltaTime
      self.__speed_back = 0.3 * -G.Background_speed * int(G.MoltScreen) / G.DeltaTime
      
      diff = 50 * int(G.MoltScreen) / G.Divider
      
      
      a = diff/2 + self.__base.get_height()/2 - self.__background.get_height()/2 + 12 * int(G.MoltScreen)
      b = G.height - self.__base.get_height() + diff
      
      self.back_pos = (0, a)
      self.base_pos = (0, b)
      
   def update(self):
      
      if not G.GameOver:
         self.back_pos = (self.back_pos[0] + self.__speed_back, self.back_pos[1])
         self.base_pos = (self.base_pos[0] + self.__speed_base, self.base_pos[1])
      
            
      if self.back_pos[0] < - self.__background.get_width()/2:
         self.back_pos = (0, self.back_pos[1])
      
      if self.base_pos[0] < - self.__base.get_width()/4:
         self.base_pos = (0, self.base_pos[1])
      
      self.mesh = py.Rect(self.base_pos[0] + self.__speed_base, self.base_pos[1], self.__base.get_width() * 2, self.__base.get_height())
      
   def Render(self, val):
      if val == 1:
         G.screen.blit(self.__background, self.back_pos)
      elif val == 2:
         G.screen.blit(self.__gameover, (G.width/2 - self.__gameover.get_width()/2,  G.height/2 - self.__gameover.get_height()/2))
      else:
         G.screen.blit(self.__base, self.base_pos)
      
      if G.Debug:
            py.draw.rect(G.screen, "Yellow", self.mesh, 2 * int(G.MoltScreen))