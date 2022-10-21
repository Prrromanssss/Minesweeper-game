import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

COLORS = {
    1: '#0078D4',
    2: 'green',
    3: 'red',
    4: '#00008b',
    5: '#964B00',
    6: '#30d5c8',
    7: 'black',
    8: 'white',
}


class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super().__init__(master, height=2, width=2,
                         font='Calibri 25 bold', *args, **kwargs)
        self.x, self.y = x, y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return (f'MyButton({self.x}, {self.y}), number: {self.number}, '
                f'is_mine: {self.is_mine}')

    def __str__(self):
        return (f'MyButton({self.x}, {self.y}), number: {self.number}, '
                f'is_mine: {self.is_mine}')


class MineSweeper:

    window = tk.Tk()
    ROW = 10
    COLUMNS = 7
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True
    FLAGS = MINES

    def __init__(self):

        self.window.title('Сапёр')
        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMNS + 2):
                btn = MyButton(self.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Return>', self.right_click)
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        if self.IS_GAME_OVER:
            return

        cur_btn = event.widget

        # if cur_btn['state'] == 'normal':
        if cur_btn['text'] != '🚩':

            if self.FLAGS == 0:
                showinfo('Недопустимое количество флагов',
                         'Количество флагов не должно превышать количество мин!')
            else:
                # cur_btn['state'] = 'disabled'
                cur_btn['text'] = '🚩'
                self.FLAGS -= 1
        elif cur_btn['text'] == '🚩':
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ''
            self.FLAGS += 1

    def click(self, clicked_button: MyButton):

        if self.IS_GAME_OVER:
            return

        if self.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            self.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', disabledforeground='black', highlightbackground='red')
            clicked_button.is_open = True
            self.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли')
            self.show_rest_mines()
        else:
            color = COLORS.get(clicked_button.count_bomb, 'yellow')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color,
                                      highlightbackground='white')
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = COLORS.get(cur_btn.count_bomb, 'yellow')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color,
                               highlightbackground='white')
            else:
                cur_btn.config(text='', highlightbackground='white')
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if not cur_btn.count_bomb:
                x, y = cur_btn.x, cur_btn.y
                for dx in range(-1, 2):
                    for dy in range(-1, 2):

                        next_btn = self.buttons[x + dx][y + dy]
                        if (not next_btn.is_open and self.is_button_in_field(next_btn)
                                and next_btn not in queue):
                            queue.append(next_btn)

    def show_rest_mines(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn['text'] = '*'

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_FIRST_CLICK = True
        self.IS_GAME_OVER = False

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, self.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, self.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение!')
            return
        self.ROW = int(row.get())
        self.COLUMNS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_window)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)

        count = 1
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count

                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, self.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, self.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def is_button_in_field(self, btn):
        if 1 <= btn.x <= self.ROW and 1 <= btn.y <= self.COLUMNS:
            return True
        return False

    def open_all_buttons(self):
        for i in range(self.ROW + 2):
            for j in range(self.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', disabledforeground='black', highlightbackground='red')
                elif btn.count_bomb in COLORS:
                    color = COLORS.get(btn.count_bomb)
                    btn.config(text=btn.count_bomb, fg=color,
                               highlightbackground='white')

    def count_mines_in_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if btn.is_mine:
                    continue
                for row_dx in range(-1, 2):
                    for col_dy in range(-1, 2):
                        neighbour = self.buttons[i + row_dx][j + col_dy]
                        if neighbour.is_mine:
                            count_bomb += 1
                btn.count_bomb = count_bomb

    def print_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()
        print('-' * 14)

    def get_mines_places(self, exclude_number: int):
        # print(f'exclude number {exclude_number}')
        indexes = list(range(1, self.COLUMNS * self.ROW + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:self.MINES]

    def insert_mines(self, number: int):
        indexes_mines = self.get_mines_places(number)
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in indexes_mines:
                    btn.is_mine = True

    def start(self):
        self.create_widgets()

        # self.open_all_buttons()
        self.window.mainloop()


game = MineSweeper()


if __name__ == '__main__':
    game.start()
