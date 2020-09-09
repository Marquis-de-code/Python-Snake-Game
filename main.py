from tkinter import *
from tkinter import messagebox
from snake import Snake
from food import Food

class Game_Display():
    def __init__(self, rows, columns):
        self.PX_SIZE = 25  # Length in pixels of each row/column
        self.PX_OFFSET = 4  # The number of pixels tkinter is putting me off by for some reason or another
        self.FPS = round(1000/8)  # Number of times the game will update per second

        self.root = Tk()# Sets up the root window
        self.score_frame = Frame(self.root)
        self.score_label = Label(self.score_frame, text='Score: 0')
        self.high_score_label = Label(self.score_frame, text='High-Score: 0')
        self.canvas = Canvas(self.root, width=(columns+1)*self.PX_SIZE,
            height=(rows+1)*self.PX_SIZE, bd=2, relief='solid', bg='black')
        self.score_frame.pack()
        self.score_label.pack(side=LEFT, padx=80)
        self.high_score_label.pack(side=RIGHT, padx=100)
        self.canvas.pack()

    def update_score_label(self, score):
        self.score_label['text'] = 'Score: ' + score

    def update_high_score_label(self, high_score):
        self.high_score_label['text'] = 'High-Score: ' + high_score

    def game_over_window(selkf, snake):
        messagebox.showinfo('You Lost', 'You Lost! \nYour final score was : ' + snake.score())

class Snake_Game():
    def __init__(self):
        self.ROWS = 20  # Number of rows in the game area
        self.COLUMNS = 20  # Number of columns in the game area
        # Initalizes the game's display using tkinter
        self.display = Game_Display(self.ROWS, self.COLUMNS)
        self.display.root.after(0, self.init_game_loop)
        self.display.root.mainloop()

    def init_game_loop(self):
        self.display.canvas.delete('all')
        self.snake = Snake(self.COLUMNS, self.ROWS)
        self.food = Food(self.display.canvas, self.display.PX_OFFSET,
            self.display.PX_SIZE, self.COLUMNS, self.ROWS, self.snake)
        self.display.update_score_label(self.snake.score())
        self.display.update_high_score_label(self.high_score())
        self.display.root.bind('<KeyPress>', self.snake.change_direction)
        self.game_loop(self.snake, self.food)

    def game_over(self):
        self.new_high_score(self.snake.score())
        self.display.game_over_window(self.snake)
        self.init_game_loop()

    # Main game loop that updates the game logic every 1/8th of a second
    def game_loop(self, snake, food):
        self.snake.move()
        if self.snake.crashed_into_wall(self.COLUMNS, self.ROWS) or self.snake.crashed_into_self():
            self.game_over()
        else:
            if self.snake.ate_food(self.food):
                self.food.new_random_location(self.COLUMNS, self.ROWS, self.snake)
                self.display.update_score_label(self.snake.score())
            self.snake.draw(self.display.canvas, self.display.PX_OFFSET, self.display.PX_SIZE)
            self.food.draw(self.display.canvas, self.display.PX_OFFSET, self.display.PX_SIZE)
            self.display.root.after(self.display.FPS, lambda:self.game_loop(snake, food))

    def high_score(self):
        try:
            fhand = open('high-score.txt')
            return fhand.read()
        except:
            return '0'

    def new_high_score(self, score):
        try:
            fhand = open('high-score.txt')
            highscore = int(fhand.read())
            if int(score) > highscore:
                self.update_high_score(score)
        except:
            self.update_high_score(score)

    def update_high_score(self, score):
        fhand = open('high-score.txt', 'w')
        fhand.write(score)
        fhand.close()

    def on_closing(self):
        self.display.root.destroy()
        print('closing')
        exit()
Snake_Game()
