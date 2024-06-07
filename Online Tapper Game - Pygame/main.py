from communication.client import Client
from pygame import *
from time import sleep
import tkinter as tk
from tkinter import messagebox


class Player:
    name = None
    id = 0
    score = 0
    def __init__(self, name, id, window, score):
        self.name = name
        self.id = id
        self.score = score
        if(id==0):
            draw.rect(window,(255,0,0),(150,400-4*self.score,200,4*self.score)) #(x,y,w,h)
        else:
            draw.rect(window,(255,255,0),(650,100,200,200))
    def showscore(self,window):
        text = font.SysFont("timesnewroman",20)
        text = text.render(self.name+" : "+str(self.score),True,(0,255,255))

        surface = text.get_rect()
        surface.center = (250,450) if not self.id else (775,450)
        window.blit(text,surface)

class Game:
    setup = True
    window = None
    WIDTH = 1000
    HEIGHT = 600
    p1,p2 = None, None
    running = True
    scorep1,scorep2 = 0,0
    splash = True
    name = None
    id1,id2 = 0,1
    socket = None

    def __init__(self):
        init()
        self.window = display.set_mode((self.WIDTH,self.HEIGHT))
        display.set_caption("Tapper")
        self.splash()
        self.reg()
        self.run()

    def submit_name(self, name,root):
        self.name = name
        root.after(1000,root.destroy)

    def on_closing(self,root):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
           self.running = False
           root.destroy()


    def reg(self):

        # Create the main window
        root = tk.Tk()
        root.title("Tapper")
        root.geometry("1000x600")
        # Create a label
        instruction_label = tk.Label(root, text="Enter your name:")
        instruction_label.pack(pady=10)
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))

        # Create an entry widget
        name_entry = tk.Entry(root)
        name_entry.pack(pady=5)

        # Create a submit button
        submit_button = tk.Button(root, text="Submit", command=lambda : self.submit_name(name_entry.get(),root),)
        submit_button.pack(pady=5)

        # Create a label for displaying the greeting
        label = tk.Label(root, text="")
        label.pack(pady=10)

        # Run the Tkinter event loop
        root.mainloop()
        
        # code for socket setup 
        self.socket = Client()


    def timer(self):
        for i in range(5):
            self.window.fill((255,255,255))
            text = font.SysFont("timesnewroman",23)
            text = text.render("Starts In :" + str(4-i)+"s",True,(0,255,255))

            surface = text.get_rect()
            surface.center = (500,300)
            self.window.blit(text,surface)
            display.flip()
            sleep(1)
        self.setup = False


    def build(self):
        self.window.fill((255,255,255))
        if self.setup:
            self.timer()
        #creating players
        self.p1 = Player(self.name,self.id1,self.window,self.scorep1)
        self.p2 = Player("Player 2",self.id2,self.window,self.scorep2)
        self.p1.showscore(self.window)
        self.p2.showscore(self.window)
        result = self.check(self.p1,self.p2)
        return result

    def run(self):
        while self.running:
            result = self.build()
            display.flip()

            for e in event.get():
                if e.type == QUIT:
                    self.running = False
                if result:
                    if e.type == KEYDOWN and e.key == K_r:
                        self.restart()
                        break
                    else:
                        continue

                if e.type == KEYDOWN:
                    if e.key == K_d or e.key == K_a:
                        self.scorep1 += 1

    def check(self,p1,p2):
        if(p1.score == 100):
            self.gameover(0)
            return 1
        if(p2.score == 100):
            self.gameover(1)
            return 1
        return False
    
    def gameover(self,id):
        self.window.fill((255,255,255))
        text = font.SysFont("timesnewroman",25)
        text = text.render(f"Player {id+1} won the match. Press any R to restart the Game!",True,(0,255,255))

        surface = text.get_rect()
        surface.center = (500,250)
        self.window.blit(text,surface)
        display.flip()

    def restart(self):
        self.scorep1 = 0
        self.scorep2 = 0
        self.p1 = None
        self.p2 = None
        self.setup = True
    
    def splash(self):
        sp = image.load("splash.jpeg")
        sp = transform.scale(sp, (self.WIDTH,self.HEIGHT))
        self.window.blit(sp,(0,0))
        display.update()
        sleep(5)
Game()
