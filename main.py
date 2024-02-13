import time
import tkinter as tk
from tkinter import font
import random
import math
import pygame
from threading import Thread
import threading
import webbrowser

# Project MineSweeper
# Author : Rosca Alexandru-David
# Started : 2/7/2024
# Finished : 2/11/2024


sound_on = 1
initial_value = 1
theme = 1
gamemode = 1
terminate_flag = False

pygame.init()
channel = pygame.mixer.Sound('./sounds/music.mp3')

color_dictionary = {
    0: "#bdbdbd",
    1: "#9CE5E3",
    2: "#1e7335",
    3: "#f57f17",
    4: "#e13800",
    5: "#ff0000",
    6: "#ff0000",
    7: "#ff0000",
    8: "#ff0000",
}

random_trivia = {
    "What is the capital of France?": "Paris",
    "What is the largest planet in our solar system?": "Jupiter",
    "What is the chemical symbol for water?": "H2O",
    "Which mammal can fly?": "Bat",
    "What is the currency of Japan?": "Yen",
    "Who painted the Mona Lisa?": "Leonardo da Vinci",
    "What is the tallest mammal on Earth?": "Giraffe",
    "What year did the Titanic sink?": "1912",
    "What is the boiling point of water in Celsius?": "100",
    "What is the capital of Spain?": "Madrid",
    "What is the smallest country in the world?": "Vatican City",
    "What is the chemical symbol for gold?": "Au",
    "Which planet is known as the Red Planet?": "Mars",
    "Which element does 'O' represent on the periodic table?": "Oxygen",
    "What is the main ingredient in guacamole?": "Avocado",
    "What is the chemical symbol for silver?": "Ag",
    "Which animal is known as the 'King of the Jungle'?": "Lion",
    "Who wrote '1984'?": "George Orwell",
    "What is the longest river in the world?": "Nile",
    "What is the freezing point of water in Fahrenheit?": "32",
    "Who painted the ceiling of the Sistine Chapel?": "Michelangelo",
    "What is the chemical symbol for sodium?": "Na",
    "What is the capital of Italy?": "Rome",
    "Which planet is closest to the Sun?": "Mercury",
    "Who wrote 'Hamlet'?": "Shakespeare",
    "What is the largest mammal in the world?": "Blue whale",
    "What is the currency of China?": "Yuan",
    "What is the chemical symbol for iron?": "Fe",
    "What is the tallest mountain in the world?": "Everest",
    "Who painted the 'Mona Lisa'?": "Da Vinci",
    "What is the chemical symbol for carbon?": "C",
    "What is the hottest continent on Earth?": "Africa",
}

theme_number ={
    1: "#44142F",
    2: "#44142F",
    3: "#330f23",
    4: "white",
    5: "black",
    6: "#e6dbd5",
    7: "#1E88E5",
    8: "#563c23",
    9: "#1565C0",
    10: "#FF9800",
    11: "#000000",
    12: "#F57C00"
}


def play_bomb_thread():
    if sound_on == 1:
        pygame.init()
        pygame.mixer.music.load("./sounds/explosion.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()


def restart_sound():
    if sound_on == 1:
        pygame.init()
        pygame.mixer.Sound('./sounds/button.wav').play()


def open_browser():
    restart_sound()
    webbrowser.open_new("https://github.com/NovioAlexandruRosca")


def music_player():
    music_change(initial_value)
    channel.play(loops=-1)


def music_change(value):
    global initial_value

    initial_value = value
    volume = int(value) / 100
    channel.set_volume(volume)

class MinesweeperGrid:
    def __init__(self, root, rows, cols, num_mines, xray, plus10):
        global terminate_flag
        if gamemode == 2 or gamemode == 5:
            terminate_flag = False
            self.time = 100
        elif gamemode == 3:
            self.time = 10
        else:
            self.time = 0

        self.time_y = 10
        self.time_label_y = None
        self.xray = 0
        self.score_label = None
        self.power_ups_label = None
        root.config(cursor='cross')
        self.original_color = None
        self.original_text = None
        self.flags_label = None
        self.update_id = None
        self.time_label = None
        self.root = root
        self.rows = rows
        self.cols = cols
        self.xray1 = int(xray)
        self.plus10 = int(plus10)
        self.num_mines = num_mines
        self.number_of_places_flags = 0
        self.discovered = []
        self.won = 1
        self.score = 0
        self.game_end = 0
        self.time_for_trivia = 0

        self.custom_font_8 = font.Font(family="Retro Gaming", size=8)
        self.custom_font_10 = font.Font(family="Retro Gaming", size=10)
        self.custom_font_12 = font.Font(family="Retro Gaming", size=12)
        self.custom_font_18 = font.Font(family="Retro Gaming", size=18, weight="bold")

        self.root.configure(bg=theme_number[theme])
        self.root.resizable(False, False)

        self.title_frame = tk.Frame(root, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack()
        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()
        self.title_label = tk.Label(self.title_outline_frame, text=f"Minesweeper",
                                    width=math.floor(self.cols * 1.2), font=self.custom_font_18, fg=theme_number[theme + 1])

        if gamemode == 2:
            self.title_label.config(text="Ticking Bomb")
        elif gamemode == 3:
            self.title_label.config(text="Time Attack")
        elif gamemode == 4:
            self.title_label.config(text="Zen Mode")
        elif gamemode == 5:
            self.title_label.config(text="Hell On Earth")

        self.title_label.grid(row=0, column=0, padx=5)

        self.grid_frame = tk.Frame(root, padx=10, bg=theme_number[theme])
        self.grid_frame.pack()
        self.bottom_grid_frame = tk.Frame(root, padx=10, pady=10, bg=theme_number[theme])
        self.bottom_grid_frame.pack()

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.buttons = []
        for i in range(rows):
            button_row = []
            for j in range(cols):
                button = tk.Button(self.grid_frame, text='', font=self.custom_font_8, width=4, height=2)
                button.grid(row=i, column=j, padx=0.5, pady=0.5)
                button.bind('<Button-1>', lambda event, row=i, col=j: self.on_left_click(row, col))
                button.bind('<ButtonPress-2>', lambda event, row=i, col=j: self.on_middle_click(row, col))
                button.bind('<ButtonRelease-2>', lambda event, row=i, col=j: self.on_middle_release(row, col))
                button.bind('<Button-3>', lambda event, row=i, col=j: self.on_right_click(row, col))
                button_row.append(button)
            self.buttons.append(button_row)

        self.root.attributes("-topmost", True)

        self.centering()  # Centers the app in the middle of the screen
        self.place_mines()  # Places mines randomly
        self.place_bomb_number()
        if gamemode != 5:
            self.place_powerup()
        if gamemode == 2:
            self.place_bonus_time()
        self.create_bottom_widgets()
        if gamemode != 4:
            self.update_timer()

    def trivia_question(self, callback):

        question, answer = random.choice(list(random_trivia.items()))

        root = tk.Tk()
        root.title("Trivia")
        TriviaQuestionApp(root, question, answer, callback)

        screen_height = self.root.winfo_screenheight()
        trivia_y = (screen_height - 200) // 2

        root.geometry(f"+{self.root.winfo_x() + self.root.winfo_width()}+{trivia_y}")
        root.mainloop()

    def screen(self):
        layer2 = tk.Frame(self.root, width=250, height=150, bg="black")
        layer2.place(x=(self.root.winfo_width() - 250) // 2, y=(self.root.winfo_height() - 150) // 2)

        layer3 = tk.Frame(layer2, width=240, height=140, padx=39, pady=24, bg=theme_number[theme])
        layer3.place(x=5, y=5)

        status_label = tk.Label(layer3, text='', font=self.custom_font_12)
        status_label.grid(row=0, column=0, padx=27.5, pady=10)

        if self.won == 1:
            status_label.config(text="You Won")
        else:
            status_label.config(text="You Lost")

        if gamemode != 4:
            score_label = tk.Label(layer3, text=f"Score: {self.score}", width=13, font=self.custom_font_12)
            score_label.grid(row=1, column=0, pady=10)
        else:
            score_label = tk.Label(layer3, text=f"Try Again!", width=13, font=self.custom_font_12)
            score_label.grid(row=1, column=0, pady=10)

        self.game_end = 1

    def trivia_callback(self, result):
        if result:
            print("The answer was correct!")
        else:
            self.time_y = 0
            print("The answer was incorrect.")

        self.root.lift()

    def update_timer(self):
        global terminate_flag

        if gamemode == 5 and self.time_for_trivia > 0 and self.time_for_trivia % 15 == 0:
            trivia_thread = threading.Thread(target=self.trivia_question, args=(self.trivia_callback,))
            trivia_thread.start()

        self.time_label.config(text=f"Time: {self.time}")

        if gamemode == 5:
            self.time_label_y.config(text=f"Caution: {self.time_y}")

        if (gamemode == 2 or gamemode == 3 or gamemode == 5) and (self.time == 0 or self.time_y == 0):
            self.game_end = 1
            terminate_flag = True

            if self.won == 1:
                sound_thread = Thread(target=play_bomb_thread)
                sound_thread.start()

            self.won = 0
            self.screen()
            self.root.after_cancel(self.update_id)

            for i in range(self.rows):
                for j in range(self.cols):
                    self.discovered.append((i, j))
                    if self.grid[i][j] == -1:
                        self.buttons[i][j].config(text="💣", bg="#ff007b")
                    elif 0 < self.grid[i][j] <= 8:
                        self.buttons[i][j].config(text=f"{self.grid[i][j]}",
                                                  bg=color_dictionary[self.grid[i][j]])
                    elif self.grid[i][j] == 9:
                        self.buttons[i][j].config(text="⭐",
                                                  bg="#1b6478")

                    elif self.grid[i][j] == 10:
                        self.buttons[i][j].config(text="+10",
                                                  bg="#1b6478")
        else:
            if gamemode == 2 or gamemode == 3 or gamemode == 5:
                self.time -= 1
            else:
                self.time += 1
            if self.time == 1000:
                self.time = 0

            if gamemode == 5:
                self.time_for_trivia += 1
                self.time_y -= 1

            self.update_id = self.root.after(1000, self.update_timer)

    def create_bottom_widgets(self):

        self.flags_label = tk.Label(self.bottom_grid_frame, text=f"Flags: 0/{self.num_mines}",
                                    width=math.floor(self.cols * 1), font=self.custom_font_12)
        self.flags_label.grid(row=0, column=0, padx=5)

        action_button = tk.Button(self.bottom_grid_frame, text="Restart", width=math.floor(self.cols * 1),
                                  font=self.custom_font_12, command=self.restart_minesweeper)
        action_button.grid(row=0, column=1, padx=19)

        if gamemode != 4:
            self.time_label = tk.Label(self.bottom_grid_frame, text="Time: ", width=math.floor(self.cols * 1),
                                       font=self.custom_font_12)
            self.time_label.grid(row=1, column=2, padx=5)

        if gamemode != 5:
            self.power_ups_label = tk.Label(self.bottom_grid_frame, text=f"XRay: {self.xray}",
                                            width=math.floor(self.cols * 1),
                                            font=self.custom_font_12)
            self.power_ups_label.grid(row=0, column=2, padx=5, pady=5)

            self.power_ups_label.bind("<Enter>", self.show_popup)
            self.power_ups_label.bind("<Leave>", self.hide_popup)
        else:
            self.time_label_y = tk.Label(self.bottom_grid_frame, text="Time: ", width=math.floor(self.cols * 1),
                                         font=self.custom_font_12)
            self.time_label_y.grid(row=0, column=2, padx=5, pady=5)

        if gamemode != 4:
            self.score_label = tk.Label(self.bottom_grid_frame, text=f"Score: {self.score}",
                                        width=math.floor(self.cols * 1),
                                        font=self.custom_font_12)
            self.score_label.grid(row=1, column=0, padx=5, pady=5)

        if gamemode != 4:
            back_to_menu = tk.Button(self.bottom_grid_frame, text="Back", width=math.floor(self.cols * 1),
                                     font=self.custom_font_10, command=self.back_menu)
            back_to_menu.grid(row=1, column=1, padx=19)

    def back_menu(self):
        global terminate_flag
        restart_sound()
        if gamemode != 4:
            self.root.after_cancel(self.update_id)
            terminate_flag = True
        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperMenu(root)
        root.mainloop()

    def show_popup(self, event):
        self.title_label.config(text="Use Middle-Click Over Cell", width=math.floor(self.cols * 2.2))

    def hide_popup(self, event):
        if gamemode == 1:
            self.title_label.config(text=f"Minesweeper", width=math.floor(self.cols * 1.2))
        elif gamemode == 2:
            self.title_label.config(text="Ticking Bomb", width=math.floor(self.cols * 1.2))
        elif gamemode == 3:
            self.title_label.config(text="Time Attack", width=math.floor(self.cols * 1.2))
        elif gamemode == 4:
            self.title_label.config(text="Zen Mode", width=math.floor(self.cols * 1.2))
        elif gamemode == 5:
            self.title_label.config(text="Hell On Earth", width=math.floor(self.cols * 1.2))

    def restart_minesweeper(self):
        global terminate_flag
        restart_sound()
        if gamemode != 4:
            self.root.after_cancel(self.update_id)
            terminate_flag = True
        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, rows=self.rows, cols=self.cols, num_mines=self.num_mines, xray=self.xray, plus10=self.plus10)
        root.mainloop()

    def place_mines(self):
        num_mines_placed = 0
        while num_mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] != -1:
                self.grid[row][col] = -1
                num_mines_placed += 1

    def place_powerup(self):
        num_powerup_placed = 0
        while num_powerup_placed < self.xray1:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] == 0:
                self.grid[row][col] = 9
                num_powerup_placed += 1

    def place_bonus_time(self):
        num_bonus_time_placed = 0
        while num_bonus_time_placed < self.plus10:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] == 0:
                # TODO Remove this print
                print(f"{row},{col}")
                self.grid[row][col] = 10
                num_bonus_time_placed += 1

    def bombs_around(self, i, j):
        number_of_bombs_around = 0
        if i > 0 and j > 0 and self.grid[i - 1][j - 1] == -1:
            number_of_bombs_around += 1
        if i > 0 and self.grid[i - 1][j] == -1:
            number_of_bombs_around += 1
        if j > 0 and self.grid[i][j - 1] == -1:
            number_of_bombs_around += 1
        if i > 0 and j < self.cols - 1 and self.grid[i - 1][j + 1] == -1:
            number_of_bombs_around += 1
        if i < self.rows - 1 and j < self.cols - 1 and self.grid[i + 1][j + 1] == -1:
            number_of_bombs_around += 1
        if i < self.rows - 1 and self.grid[i + 1][j] == -1:
            number_of_bombs_around += 1
        if j < self.cols - 1 and self.grid[i][j + 1] == -1:
            number_of_bombs_around += 1
        if i < self.rows - 1 and j > 0 and self.grid[i + 1][j - 1] == -1:
            number_of_bombs_around += 1
        return number_of_bombs_around

    def explore_zeros(self, visited, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if self.grid[row][col] != -1:
            if (row, col) not in self.discovered:
                visited[row][col] = True
                self.discovered.append((row, col))

        if self.buttons[row][col].cget("text") == "🚩":
            self.buttons[row][col].config(text='')

        if self.grid[row][col] == 0 and self.game_end == 0:
            self.score += 30
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]) and not visited[new_row][new_col]:
                    self.explore_zeros(visited, new_row, new_col)
        elif self.grid[row][col] > 0 and self.game_end == 0:
            self.score += 100

    def find_zeros(self, clicked_row, clicked_col):
        visited = [[False] * len(self.grid[0]) for _ in range(len(self.grid))]

        self.explore_zeros(visited, clicked_row, clicked_col)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if visited[i][j]:
                    if 0 < self.grid[i][j] <= 8:
                        self.buttons[i][j].config(text=f"{self.grid[i][j]}",
                                                  bg=color_dictionary[self.grid[i][j]])
                    elif self.grid[i][j] == 0:
                        self.buttons[i][j].config(bg=color_dictionary[0])

                    elif self.grid[i][j] == 9:
                        self.buttons[i][j].config(text="⭐",
                                                  bg="#1b6478")
                        self.xray += 1
                        self.power_ups_label.config(text=f"Xray: {self.xray}")

                    elif self.grid[i][j] == 10:
                        self.buttons[i][j].config(text="+10",
                                                  bg="#1b6478")

                        self.time += 10
                        self.time_label.config(text=f"Time: {self.time}")

    def place_bomb_number(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] != -1:
                    number_of_bombs_around = self.bombs_around(i, j)
                    self.grid[i][j] = number_of_bombs_around

    def centering(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - self.root.winfo_reqwidth()) // 2 - self.root.winfo_reqwidth() // 2
        y_position = (screen_height - self.root.winfo_reqheight()) // 2 - self.root.winfo_reqheight() // 2

        self.root.geometry("+{}+{}".format(x_position, y_position))

    def on_left_click(self, row, col):
        global terminate_flag
        if self.game_end == 0:
            if self.won == 1:
                if sound_on == 1:
                    pygame.init()
                    pygame.mixer.Sound('./sounds/click.wav').play()

            if self.grid[row][col] == -1:

                if self.won == 1:
                    sound_thread = Thread(target=play_bomb_thread)
                    sound_thread.start()

                self.won = 0
                self.screen()
                if gamemode != 4:
                    self.root.after_cancel(self.update_id)
                    terminate_flag = True

                for i in range(self.rows):
                    for j in range(self.cols):
                        if (i, j) not in self.discovered:
                            self.discovered.append((i, j))

                        if self.grid[i][j] == -1:
                            self.buttons[i][j].config(text="💣", bg="#ff007b")
                        elif 0 < self.grid[i][j] <= 8:
                            self.buttons[i][j].config(text=f"{self.grid[i][j]}",
                                                      bg=color_dictionary[self.grid[i][j]])
                        elif self.grid[i][j] == 9:
                            self.buttons[i][j].config(text="⭐",
                                                      bg="#1b6478")
                        elif self.grid[i][j] == 10:
                            self.buttons[i][j].config(text="+10",
                                                      bg="#1b6478")

            elif self.grid[row][col] > 0:

                if (row, col) not in self.discovered:

                    if gamemode == 3:
                        self.time = 10
                        self.time_label.config(text=f"Time: {self.time}")

                    if gamemode == 5:
                        self.time_y = 10
                        self.time_label_y.config(text=f"Caution: {self.time_y}")

                    if self.grid[row][col] <= 8:
                        self.buttons[row][col].config(text=f"{self.grid[row][col]}",
                                                      bg=color_dictionary[self.grid[row][col]])
                    elif self.grid[row][col] == 9:
                        self.buttons[row][col].config(text="⭐",
                                                      bg="#1b6478")
                        self.xray += 1
                        self.power_ups_label.config(text=f"Xray: {self.xray}")

                    elif self.grid[row][col] == 10:
                        self.buttons[row][col].config(text="+10",
                                                      bg="#1b6478")

                        self.time += 10
                        self.time_label.config(text=f"Time: {self.time}")

                    self.discovered.append((row, col))
                    if self.game_end == 0:
                        self.score += 100

            elif self.grid[row][col] == 0:
                if (row, col) not in self.discovered:
                    self.find_zeros(row, col)

                    if gamemode == 3:
                        self.time = 10
                        self.time_label.config(text=f"Time: {self.time}")

                    if gamemode == 5:
                        self.time_y = 10
                        self.time_label_y.config(text=f"Caution: {self.time_y}")

            self.num_of_flags()
            if len(self.discovered) == self.rows * self.cols - self.num_mines:
                if gamemode != 4:
                    self.root.after_cancel(self.update_id)
                if self.time < 30 and self.game_end == 0:
                    self.score += 500
                else:
                    self.score += 100
                self.screen()
        if gamemode != 4:
            self.score_label.config(text=f"Score: {self.score}")
        # TODO: Delete the print
        print(f"{len(self.discovered)}")

    def on_right_click(self, row, col):
        if self.game_end == 0:
            if (row, col) not in self.discovered:

                if self.buttons[row][col].cget("text") == "🚩":
                    if self.won == 1:
                        if sound_on == 1:
                            pygame.init()
                            pygame.mixer.Sound('./sounds/flag.wav').play()

                    self.buttons[row][col].config(text='', bg="#e4e4e4")
                else:
                    if self.number_of_places_flags < self.num_mines:
                        self.buttons[row][col].config(text="🚩", bg="#ff7cc3")
                        if self.won == 1:
                            if sound_on == 1:
                                pygame.init()
                                pygame.mixer.Sound('./sounds/flag.wav').play()

            self.num_of_flags()

    def on_middle_click(self, row, col):
        if self.game_end == 0:
            self.root.config(cursor='target')
            if (row, col) not in self.discovered and self.xray > 0:

                self.xray -= 1
                self.power_ups_label.config(text=f"Xray: {self.xray}")

                if self.grid[row][col] == 0:
                    self.buttons[row][col].config(text='',
                                                  bg="yellow")
                if 9 > self.grid[row][col] > 0:
                    self.buttons[row][col].config(text=f"{self.grid[row][col]}",
                                                  bg="yellow")
                if 9 == self.grid[row][col]:
                    self.buttons[row][col].config(text="⭐",
                                                  bg="#1b6478")
                if self.grid[row][col] == -1:
                    self.buttons[row][col].config(text="💣",
                                                  bg="yellow")

    def on_middle_release(self, row, col):
        if (row, col) not in self.discovered:
            self.buttons[row][col].config(text='',
                                          bg="#e4e4e4")
        self.root.config(cursor='cross')

    def num_of_flags(self):
        number_of_flags = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.buttons[i][j].cget("text") == "🚩":
                    number_of_flags += 1

        self.number_of_places_flags = number_of_flags

        timer_text = f"Flags: {number_of_flags}/{self.num_mines}"

        self.flags_label.config(text=timer_text)


class MinesweeperMenu:
    def __init__(self, root):
        root.config(cursor='tcross')
        self.root = root

        self.custom_font_12 = font.Font(family="Retro Gaming", size=12)
        self.custom_font_19 = font.Font(family="Retro Gaming", size=19, weight="bold")

        self.root.resizable(False, False)

        self.background = tk.Frame(root, bg=theme_number[theme], padx=10, pady=5)
        self.background.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.background, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack(side="top", fill="x")

        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()

        self.title_label = tk.Label(self.title_outline_frame, text=f"Minesweeper",
                                    width=12, font=self.custom_font_19, fg=theme_number[theme+1])
        self.title_label.grid(row=0, column=0, padx=5)

        self.outer_frame = tk.Frame(self.background, bg="black", padx=1, pady=1)
        self.outer_frame.pack(expand=True, fill="both")

        self.inner_frame = tk.Frame(self.outer_frame, bg=theme_number[theme+2], bd=1, relief="solid")
        self.inner_frame.pack(expand=True, fill="both", padx=1, pady=2)

        button_width = 15
        new_game_button = tk.Button(self.inner_frame, text="New Game", font=self.custom_font_12, width=button_width,
                                    command=self.new_game, fg=theme_number[theme+1])
        new_game_button.pack(pady=(10, 5))

        game_modes_button = tk.Button(self.inner_frame, text="Game Modes", font=self.custom_font_12, width=button_width,
                                      command=self.game_modes, fg=theme_number[theme+1])
        game_modes_button.pack(pady=5)

        custom_game_button = tk.Button(self.inner_frame, text="Custom Game", font=self.custom_font_12,
                                       width=button_width, command=self.custom_game, fg=theme_number[theme+1])
        custom_game_button.pack(pady=5)

        settings_button = tk.Button(self.inner_frame, text="Settings", font=self.custom_font_12, width=button_width,
                                    command=self.settings, fg=theme_number[theme+1])
        settings_button.pack(pady=5)

        github_button = tk.Button(self.inner_frame, text="GitHub", font=self.custom_font_12, width=button_width,
                                  command=open_browser, fg=theme_number[theme+1])
        github_button.pack(pady=5)

        exit_button = tk.Button(self.inner_frame, text="Exit", font=self.custom_font_12, command=self.exit,
                                width=button_width, fg=theme_number[theme+1])
        exit_button.pack(pady=(5, 10))

        self.centering()

    def centering(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - self.root.winfo_reqwidth()) // 2 - self.root.winfo_reqwidth() // 2
        y_position = (screen_height - self.root.winfo_reqheight()) // 2 - self.root.winfo_reqheight() // 2

        self.root.geometry("+{}+{}".format(x_position, y_position))

    def settings(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Settings")
        MinesweeperSettings(root)
        root.mainloop()

    def new_game(self):
        global gamemode
        restart_sound()
        self.root.destroy()

        gamemode = 1

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, rows=10, cols=10, num_mines=10, xray=1, plus10=1)
        root.mainloop()

    def game_modes(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Game Modes")
        MinesweeperGameModes(root)
        root.mainloop()

    def custom_game(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Custom Game")
        MinesweeperCustomGame(root)
        root.mainloop()

    def exit(self):
        restart_sound()
        time.sleep(0.1)
        self.root.destroy()


class MinesweeperSettings:
    def __init__(self, root):
        root.config(cursor='tcross')
        self.root = root

        self.custom_font_12 = font.Font(family="Retro Gaming", size=12)
        self.custom_font_19 = font.Font(family="Retro Gaming", size=19, weight="bold")

        self.root.resizable(False, False)

        self.background = tk.Frame(root, bg=theme_number[theme], padx=10, pady=5)
        self.background.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.background, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack(side="top", fill="x")

        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()

        self.title_label = tk.Label(self.title_outline_frame, text=f"Settings",
                                    width=10, font=self.custom_font_19, fg=theme_number[theme+1])
        self.title_label.grid(row=0, column=0, padx=5)

        self.outer_frame = tk.Frame(self.background, bg="black", padx=1, pady=1)
        self.outer_frame.pack(expand=True, fill="both")

        self.inner_frame = tk.Frame(self.outer_frame, bg=theme_number[theme+2], bd=1, relief="solid")
        self.inner_frame.pack(expand=True, fill="both", padx=1, pady=2)

        button_width = 15
        self.effects_button = tk.Button(self.inner_frame, font=self.custom_font_12, width=button_width,
                                        command=self.settings_effects)
        self.effects_button.pack(pady=10)

        if sound_on == 1:
            self.effects_button.config(text=f"Effects On")
        else:
            self.effects_button.config(text=f"Effects Off")

        music_button = tk.Label(self.inner_frame, text="Music", font=self.custom_font_12, width=button_width)
        music_button.pack()

        scale = tk.Scale(self.inner_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=music_change,
                         showvalue=False, sliderrelief="flat", length=180, troughcolor=theme_number[theme+2])
        scale.pack()

        scale.set(initial_value)

        theme_button = tk.Button(self.inner_frame, text="Themes", font=self.custom_font_12,
                                 width=button_width, command=self.theme)
        theme_button.pack(pady=10)

        menu_button = tk.Button(self.inner_frame, text="Back", font=self.custom_font_12, width=button_width,
                                command=self.menu)
        menu_button.pack(pady=(0, 10))

        self.centering()

    def centering(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - self.root.winfo_reqwidth()) // 2 - self.root.winfo_reqwidth() // 2
        y_position = (screen_height - self.root.winfo_reqheight()) // 2 - self.root.winfo_reqheight() // 2

        self.root.geometry("+{}+{}".format(x_position, y_position))

    def menu(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperMenu(root)
        root.mainloop()

    def settings_effects(self):
        global sound_on

        if sound_on == 1:
            sound_on = 0
        else:
            sound_on = 1
            restart_sound()

        if sound_on == 1:
            self.effects_button.config(text=f"Effects On")
        else:
            self.effects_button.config(text=f"Effects Off")

    def theme(self):
        global theme

        restart_sound()
        theme += 3

        if theme == 13:
            theme = 1

        self.root.destroy()

        root = tk.Tk()
        root.title("Settings")
        MinesweeperSettings(root)
        root.mainloop()


class MinesweeperGameModes:
    def __init__(self, root):
        root.config(cursor='tcross')
        self.root = root

        self.custom_font_12 = font.Font(family="Retro Gaming", size=12)
        self.custom_font_19 = font.Font(family="Retro Gaming", size=19, weight="bold")

        self.root.resizable(False, False)

        self.background = tk.Frame(root, bg=theme_number[theme], padx=10, pady=5)
        self.background.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.background, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack(side="top", fill="x")

        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()

        self.title_label = tk.Label(self.title_outline_frame, text=f"Game Modes",
                                    width=10, font=self.custom_font_19, fg=theme_number[theme+1])
        self.title_label.grid(row=0, column=0, padx=5)

        self.outer_frame = tk.Frame(self.background, bg="black", padx=1, pady=1)
        self.outer_frame.pack(expand=True, fill="both")

        self.inner_frame = tk.Frame(self.outer_frame, bg=theme_number[theme+2], bd=1, relief="solid")
        self.inner_frame.pack(expand=True, fill="both", padx=1, pady=2)

        button_width = 15
        self.time_attack = tk.Button(self.inner_frame, text="Ticking Bomb", font=self.custom_font_12,
                                     width=button_width,
                                     command=self.time_attack_mode)
        self.time_attack.pack(pady=(10, 0))

        dont_skip_a_beat = tk.Button(self.inner_frame, text="Time Attack", font=self.custom_font_12, width=button_width,
                                     command=self.dont_skip_a_beat_mode)
        dont_skip_a_beat.pack(pady=10)

        yard_sweeper = tk.Button(self.inner_frame, text="Zen Mode", font=self.custom_font_12,
                                 width=button_width, command=self.yard_sweeper_mode)
        yard_sweeper.pack()

        hell_on_earth = tk.Button(self.inner_frame, text="Hell On Earth", font=self.custom_font_12, width=button_width,
                                  command=self.hell_on_earth_mode)
        hell_on_earth.pack(pady=10)

        menu_button = tk.Button(self.inner_frame, text="Back", font=self.custom_font_12, width=button_width,
                                command=self.menu)
        menu_button.pack(pady=(0, 10))

        self.centering()

    def centering(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - self.root.winfo_reqwidth()) // 2 - self.root.winfo_reqwidth() // 2
        y_position = (screen_height - self.root.winfo_reqheight()) // 2 - self.root.winfo_reqheight() // 2

        self.root.geometry("+{}+{}".format(x_position, y_position))

    def dont_skip_a_beat_mode(self):
        global gamemode
        restart_sound()
        self.root.destroy()

        gamemode = 3

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, 10, 10, 10, 1, 1)
        root.mainloop()

    def time_attack_mode(self):
        global gamemode
        restart_sound()
        self.root.destroy()

        gamemode = 2

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, 10, 10, 10, 1, 1)
        root.mainloop()

    def yard_sweeper_mode(self):
        global gamemode
        restart_sound()
        self.root.destroy()

        gamemode = 4

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, 10, 10, 10, 1, 1)
        root.mainloop()

    def hell_on_earth_mode(self):
        global gamemode
        restart_sound()
        self.root.destroy()

        gamemode = 5

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, 10, 10, 10, 1, 1)
        root.mainloop()

    def menu(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperMenu(root)
        root.mainloop()


class MinesweeperCustomGame:
    def __init__(self, root):
        self.mode_selected = None
        root.config(cursor='tcross')
        self.root = root
        self.root.title("Custom Game")

        self.custom_font_12 = font.Font(family="Retro Gaming", size=12)
        self.custom_font_19 = font.Font(family="Retro Gaming", size=19, weight="bold")

        self.root.resizable(False, False)

        self.background = tk.Frame(root, bg=theme_number[theme], padx=10, pady=5)
        self.background.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.background, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack(side="top", fill="x")

        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()

        self.title_label = tk.Label(self.title_outline_frame, text=f"Custom Game",
                                    width=12, font=self.custom_font_19, fg=theme_number[theme+1])
        self.title_label.grid(row=0, column=0, padx=5)

        self.outer_frame = tk.Frame(self.background, bg="black", padx=1, pady=1)
        self.outer_frame.pack(expand=True, fill="both")

        self.inner_frame = tk.Frame(self.outer_frame, bg=theme_number[theme+2], bd=1, relief="solid")
        self.inner_frame.pack(expand=True, fill="both", padx=1, pady=2)

        button_width = 15

        # Game Mode Buttons
        self.game_modes = ["Classic Game", "Ticking Bomb", "Time Attack", "Zen Mode", "Hell on Earth"]
        self.mode_buttons = []

        for i, mode in enumerate(self.game_modes):
            button = tk.Button(self.inner_frame, text=mode, font=self.custom_font_12, width=button_width,
                               command=lambda mode=mode: self.select_mode(mode), fg=theme_number[theme+1])
            button.grid(row=0, column=i + 1, pady=5, padx=5)
            self.mode_buttons.append(button)

        # Sliders

        lables_width = 15

        self.rows_label = tk.Label(self.inner_frame, text="Number of Rows", font=self.custom_font_12, bg="white",
                                   fg=theme_number[theme+1], width=lables_width)
        self.rows_label.grid(row=1, column=1, padx=(0, 0), pady=5)

        self.cols_label = tk.Label(self.inner_frame, text="Number of Columns", font=self.custom_font_12, bg="white",
                                   fg=theme_number[theme+1], width=lables_width)
        self.cols_label.grid(row=2, column=1, padx=(0, 0), pady=5)

        self.bombs_label = tk.Label(self.inner_frame, text="Number of Bombs", font=self.custom_font_12, bg="white",
                                    fg=theme_number[theme+1], width=lables_width)
        self.bombs_label.grid(row=3, column=1, padx=(0, 0), pady=5)

        #

        self.rows_label_min_max = tk.Label(self.inner_frame, text="⇐ 10 - 20 | 0 - 3 ⇒", font=self.custom_font_12,
                                           bg="white",
                                           fg=theme_number[theme+1], width=lables_width)
        self.rows_label_min_max.grid(row=1, column=3, padx=(0, 0), pady=5)

        self.cols_label_min_max = tk.Label(self.inner_frame, text="⇐ 10 - 20 | 0 - 3 ⇒", font=self.custom_font_12,
                                           bg="white",
                                           fg=theme_number[theme+1], width=lables_width)
        self.cols_label_min_max.grid(row=2, column=3, padx=(0, 0), pady=5)

        self.bombs_label_min_max = tk.Label(self.inner_frame, text="⇐ Min: 10 - Max: 50", font=self.custom_font_12,
                                            bg="white",
                                            fg=theme_number[theme+1], width=lables_width)
        self.bombs_label_min_max.grid(row=3, column=3, padx=(0, 0), pady=5)

        #

        self.rows_scale = tk.Scale(self.inner_frame, from_=10, to=20, orient=tk.HORIZONTAL, showvalue=False,
                                   sliderrelief="flat", length=180, troughcolor=theme_number[theme+2], command=self.rows_change)
        self.rows_scale.grid(row=1, column=2)

        self.cols_scale = tk.Scale(self.inner_frame, from_=10, to=20, orient=tk.HORIZONTAL, showvalue=False,
                                   sliderrelief="flat", length=180, troughcolor=theme_number[theme+2], command=self.cols_change)
        self.cols_scale.grid(row=2, column=2)

        self.bombs_scale = tk.Scale(self.inner_frame, from_=10, to=50, orient=tk.HORIZONTAL, showvalue=False,
                                    sliderrelief="flat", length=180, troughcolor=theme_number[theme+2], command=self.bombs_change)
        self.bombs_scale.grid(row=3, column=2)

        #

        self.rows_value_label = tk.Label(self.inner_frame, text="10", font=self.custom_font_12, bg="white",
                                         fg=theme_number[theme+1], width=2)
        self.rows_value_label.grid(row=1, column=0, padx=1, pady=5)

        self.cols_value_label = tk.Label(self.inner_frame, text="10", font=self.custom_font_12, bg="white",
                                         fg=theme_number[theme+1], width=2)
        self.cols_value_label.grid(row=2, column=0, padx=1, pady=5)

        self.bombs_value_label = tk.Label(self.inner_frame, text="10", font=self.custom_font_12, bg="white",
                                          fg=theme_number[theme+1], width=2)
        self.bombs_value_label.grid(row=3, column=0, padx=1, pady=5)

        # Xrays and +10 sec input boxes

        self.xrays_label = tk.Label(self.inner_frame, text="Number of Xray", font=self.custom_font_12, bg="white",
                                    fg=theme_number[theme+1], width=lables_width)
        self.xrays_label.grid(row=1, column=4, padx=(0, 0), pady=5)

        self.plus_10sec_label = tk.Label(self.inner_frame, text="Number of +10", font=self.custom_font_12,
                                         bg="white", fg=theme_number[theme+1], width=lables_width)
        self.plus_10sec_label.grid(row=2, column=4, padx=(0, 0), pady=5)

        self.xrays_entry = tk.Entry(self.inner_frame, font=self.custom_font_12, width=lables_width, justify="center")
        self.xrays_entry.grid(row=1, column=5, pady=5)

        self.xrays_entry.insert(0, "0")
        self.xrays_entry.bind("<FocusIn>", self.on_xrays_entry_click)
        self.xrays_entry.bind("<FocusOut>", self.on_xrays_entry_leave)

        self.plus_10sec_entry = tk.Entry(self.inner_frame, font=self.custom_font_12, width=lables_width,
                                         justify="center")
        self.plus_10sec_entry.grid(row=2, column=5, pady=5)

        self.plus_10sec_entry.insert(0, "0")
        self.plus_10sec_entry.bind("<FocusIn>", self.on_plus_10sec_entry_click)
        self.plus_10sec_entry.bind("<FocusOut>", self.on_plus_10sec_entry_leave)

        # Start Game Button
        start_game_button = tk.Button(self.inner_frame, text="Start Game", font=self.custom_font_12,
                                      width=button_width, command=self.start_game, fg=theme_number[theme+1])
        start_game_button.grid(row=len(self.game_modes) + 1, column=1, pady=(5, 10))

        # Back Button
        menu_button = tk.Button(self.inner_frame, text="Back", font=self.custom_font_12, width=button_width,
                                fg=theme_number[theme+1], command=self.menu)
        menu_button.grid(row=len(self.game_modes) + 1, column=2, pady=(5, 10))

        self.centering()

    def rows_change(self, value):
        self.rows_value_label.config(text=f"{value}")

    def cols_change(self, value):
        self.cols_value_label.config(text=f"{value}")

    def bombs_change(self, value):
        self.bombs_value_label.config(text=f"{value}")

    def on_xrays_entry_click(self, event):
        if self.xrays_entry.get() == "0":
            self.xrays_entry.delete(0, tk.END)

    def on_xrays_entry_leave(self, event):
        if not self.xrays_entry.get():
            self.xrays_entry.insert(0, "0")
        if int(self.xrays_entry.get()) > 3:
            self.xrays_entry.delete(0, tk.END)
            self.xrays_entry.insert(0, "3")
        if int(self.xrays_entry.get()) < 0:
            self.xrays_entry.delete(0, tk.END)
            self.xrays_entry.insert(0, "0")

    def on_plus_10sec_entry_click(self, event):
        if self.plus_10sec_entry.get() == "0":
            self.plus_10sec_entry.delete(0, tk.END)

    def on_plus_10sec_entry_leave(self, event):
        if not self.plus_10sec_entry.get():
            self.plus_10sec_entry.insert(0, "0")
        if int(self.plus_10sec_entry.get()) > 3:
            self.plus_10sec_entry.delete(0, tk.END)
            self.plus_10sec_entry.insert(0, "3")
        if int(self.plus_10sec_entry.get()) < 0:
            self.plus_10sec_entry.delete(0, tk.END)
            self.plus_10sec_entry.insert(0, "0")

    def centering(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - self.root.winfo_reqwidth()) // 2 - self.root.winfo_reqwidth() // 2
        y_position = (screen_height - self.root.winfo_reqheight()) // 2 - self.root.winfo_reqheight() // 2
        self.root.geometry("+{}+{}".format(x_position - 300, y_position + 50))

    def select_mode(self, mode):

        restart_sound()

        selected_exits = False
        mode_exists = False

        for button in self.mode_buttons:
            if button.cget("text") == "Selected":
                selected_exits = True
            if button.cget("text") == mode:
                mode_exists = True

        if selected_exits and mode_exists is False or selected_exits is False:
            for button in self.mode_buttons:
                if button.cget("text") == mode:
                    self.mode_selected = mode
                    button.config(text="Selected")
                elif button.cget("text") == "Selected":
                    button.config(text=mode)
                    self.mode_selected = None
        else:
            for button in self.mode_buttons:
                if button.cget("text") == "Selected":
                    button.config(text=str(self.mode_selected))
                    self.mode_selected = None

            for button in self.mode_buttons:
                if button.cget("text") == mode:
                    self.mode_selected = mode
                    button.config(text="Selected")

    def start_game(self):

        global gamemode
        restart_sound()

        rows = self.rows_scale.get()
        cols = self.cols_scale.get()
        bombs = self.bombs_scale.get()
        xrays = self.xrays_entry.get()
        plus_10sec = self.plus_10sec_entry.get()

        if self.mode_selected is None:
            this_is_the_mode = "Classic Game"
        else:
            this_is_the_mode = self.mode_selected

        if this_is_the_mode == "Classic Game":
            gamemode = 1
        elif this_is_the_mode == "Ticking Bomb":
            gamemode = 2
        elif this_is_the_mode == "Time Attack":
            gamemode = 3
        elif this_is_the_mode == "Zen Mode":
            gamemode = 4
        elif this_is_the_mode == "Hell on Earth":
            gamemode = 5

        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperGrid(root, rows=rows, cols=cols, num_mines=bombs, xray=xrays, plus10=plus_10sec)
        root.mainloop()

    def menu(self):
        restart_sound()
        self.root.destroy()

        root = tk.Tk()
        root.title("Minesweeper")
        MinesweeperMenu(root)
        root.mainloop()


class TriviaQuestionApp:
    def __init__(self, root, question, correct_answer, callback):
        self.update_id = None
        self.root = root
        self.question = question
        self.correct_answer = correct_answer
        self.callback = callback

        self.root.config(cursor='tcross')

        self.background = tk.Frame(root, bg=theme_number[theme], padx=10, pady=5)
        self.background.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.background, padx=10, pady=15, bg=theme_number[theme])
        self.title_frame.pack(side="top", fill="x")

        self.title_outline_frame = tk.Frame(self.title_frame, pady=4, bg="black")
        self.title_outline_frame.pack()

        self.title_label = tk.Label(self.title_outline_frame, text=f"Hold At Gunpoint",
                                    width=15, font=("Retro Gaming", 14, "bold"), fg=theme_number[theme+1])
        self.title_label.grid(row=0, column=0, padx=5)

        self.outer_frame = tk.Frame(self.background, bg="black", padx=1, pady=1)
        self.outer_frame.pack(expand=True, fill="both")

        self.inner_frame = tk.Frame(self.outer_frame, bg=theme_number[theme+2], bd=1, relief="solid")
        self.inner_frame.pack(expand=True, fill="both", padx=1, pady=2)

        self.label = tk.Label(self.inner_frame, text=self.question, font=("Retro Gaming", 12), fg="white", bg=theme_number[theme+2])
        self.label.pack()

        self.answer_entry = tk.Entry(self.inner_frame, font=("Retro Gaming", 12), justify="center")
        self.answer_entry.pack()

        self.answer_entry.bind('<Return>', self.check_answer)

        self.submit_button = tk.Button(self.inner_frame, text="Submit", font=("Retro Gaming", 12),
                                       command=self.check_answer, bg=theme_number[theme], fg="white")
        self.submit_button.pack()

        self.time_left = 10
        self.timer_label = tk.Label(self.inner_frame, text=f"{self.time_left}", font=("Retro Gaming", 12),
                                    fg="white", bg=theme_number[theme+2])
        self.timer_label.pack()

        self.root.attributes("-topmost", True)

        self.root.protocol("WM_DELETE_WINDOW", self.disable_close)

        self.update_timer()

    def disable_close(self):
        pass

    def check_answer(self, event=None):
        user_answer = self.answer_entry.get()
        if user_answer.lower() == self.correct_answer.lower():
            if not terminate_flag:
                self.callback(1)
        else:
            if not terminate_flag:
                self.callback(0)

        self.root.after_cancel(self.update_id)
        self.root.destroy()

    def update_timer(self):
        global terminate_flag

        if terminate_flag:
            self.root.after_cancel(self.update_id)
            self.root.destroy()

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"{self.time_left}")
            self.update_id = self.root.after(1000, self.update_timer)
        else:
            if not terminate_flag:
                self.callback(0)
            self.root.after_cancel(self.update_id)
            self.root.destroy()


def main():
    # connect_to_database()
    music_player()
    root = tk.Tk()
    root.iconphoto(True, tk.PhotoImage(file="./images/Bomb.png"))
    root.title("Minesweeper")
    MinesweeperMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
