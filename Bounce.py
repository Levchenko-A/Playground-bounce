from tkinter import *
import time
import random



# ===> Defining the ball and it's behaviour
class Ball:
    def __init__(self, canvas, paddle, color, score):
        self.score = score
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)  # creating a ball of given color
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)  # shuffling initial direction parameter
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()  # getting current canvas height
        self.canvas_width = self.canvas.winfo_width()  # getting current canvas width
        self.hit_bottom = False  # loss condition at the beginning

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True  # loss condition
        if self.hit_paddle(pos) == True:
            self.y = -3
            self.score += 1
            canvas.itemconfig(score_text, text=int(self.score))  # score counter
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    # interaction with paddle
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False


# ===> Defining the paddle and it's behaviour
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.canvas_width = self.canvas.winfo_width()
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2


def start_game(event):
    if event.keysym == 'Return':
        while True:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            if ball.hit_bottom == True:
                time.sleep(0.5)
                game_over = canvas.create_rectangle(150, 100, 350, 200, fill='black', outline='white')
                game_over_text = canvas.create_text(250, 150, text='Game Over', font=('Arial', 20), fill='white')
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

# ===> game window and it`s characteristics
tk = Tk()
score = 0
tk.title('Bounce - Game')  # title of the window
tk.resizable(0, 0)  # fixed size
tk.wm_attributes('-topmost', 1)  # on top of all windows
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
score_rect = canvas.create_polygon(400, 10, 490, 10, 490, 60, 400, 60, 405, 55, 485, 55, 485, 15, 405, 15, 405, 55, 400,
                                   60, fill='red', outline='black')
score_text = canvas.create_text(445, 35, text=int(score), font=("Arial", 15))
tk.update()
paddle = Paddle(canvas, 'magenta')
ball = Ball(canvas, paddle, 'blue', score)
canvas.bind_all("<KeyPress-Return>", start_game)
tk.mainloop()

