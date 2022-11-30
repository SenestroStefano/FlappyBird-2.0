from __modules__ import *
import globals as G
import classes


def init():
   global background, bird, tubes
   global gameover_sound, jump_sound, record_sound, wtf_boom
   
   py.mixer.music.load("sounds/background_music.wav")
   py.mixer.music.play(-1)
   
   bird = classes.Bird((80, 60))

   tubes = []
   
   G.Score = 0
   G.flag_beat_record = True
   with open('score.txt', 'r') as f:
      f_contest = f.readlines()
      G.Record = int(f_contest[1])
   f.close()
   
   
   space = 0
   posx = (G.width / G.Num_tubes) + space
   for i in range(G.Num_tubes):
      tube = classes.Tube( G.width + posx * i )
      tubes.append(tube)

   background = classes.Background()
   
   #sounds
   gameover_sound = py.mixer.Sound("sounds/ulose.wav")
   jump_sound = py.mixer.Sound("sounds/jump.wav")
   record_sound = py.mixer.Sound("sounds/newRecord.wav")
   wtf_boom = py.mixer.Sound("sounds/Boom.wav")
   
   gameover_sound.set_volume(10)


def quit():
   py.quit()
   sys.exit()
   

def set_text(string, coordx, coordy, fontSize):
   font = py.font.Font('freesansbold.ttf', fontSize)
   text = font.render(string, True, (255, 255, 255))
   textRect = (coordx, coordy)
   return (text, textRect)
   

def gameOver():
   if not G.GameOver:
      bird.addForce(6)
      py.mixer.music.stop()
      wtf_boom.play()
      wtf_boom.fadeout(5000)
      gameover_sound.play()
   
   G.GameOver = True

def comands():
   for event in py.event.get():
         
         if event.type == py.QUIT:
            quit()
            
         if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
               quit()
               
            if event.key == py.K_SPACE:
               if not G.GameOver:
                  bird.addForce(8)
                  bird.StartFase = False
               
               if G.GameOver:
                  G.GameOver = not G.GameOver
                  wtf_boom.stop()
                  start()
               
            if event.key == py.K_d:
               G.Debug = not G.Debug

def update():
   py.display.flip()
   G.clock.tick(G.FPS)
   
   
def render():
   G.screen.fill("#4ec0ca")
   
   
   G.delta_time = time.time() - G.last_time
   G.delta_time *= G.clock.get_fps()
   G.last_time = time.time()
   
   background.update()
   background.Render(1)
   
   for tube in tubes:
      if not bird.StartFase:
         tube.update()
      
      for j in range(2):
         cond = not (bird.mesh[1] < G.height and bird.mesh[1] + bird.mesh[3] > 0)
         if G.Collisions and (bird.mesh.colliderect(tube.mesh[j]) or bird.mesh.colliderect(background.mesh) or cond):
            gameOver()
      
      if bird.mesh.colliderect(tube.score_area) and tube.flag_score:
         G.Score += 1
         tube.flag_score = False
         
         if G.Score > G.Record:
            
            with open('score.txt', 'w') as f:
               f.write("Record:\n")
               f.write(str(G.Score))
            f.close()
            
            if G.flag_beat_record:
               record_sound.play()
               G.flag_beat_record = False

   background.Render(0)
   
   score = set_text(str(G.Score), G.width/2, 40*int(G.MoltScreen), 30*int(G.MoltScreen))
   record = set_text(("Record: "+str(G.Record)), 20*int(G.MoltScreen), 10*int(G.MoltScreen), 10*int(G.MoltScreen))

   G.screen.blit(score[0], score[1])
   G.screen.blit(record[0], record[1])

   if bird.StartFase:
      bird.preUpdate()
   else:
      bird.update()
      
   if G.GameOver:
      bird.RenderDied()
      background.Render(2)
      
def mainloop():   
   while True:
      comands()
      
      render()
      update()
   
def start():
   init()
   mainloop()
   
if __name__ == "__main__":
   start()