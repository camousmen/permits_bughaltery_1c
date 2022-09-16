
from copy import copy
from tkinter import END, StringVar, Tk, Frame, BOTH, Listbox, Scrollbar
from tkinter.ttk import Frame, Button, Style, Label, Entry
import tkinter as tk
import csv, pickle


partner_list = []
name_list = [x for x in range(0, 100)]
partners_names_rel_list = []

# для тестов будем загружать из файла csv
def load_partners_from_csv():
    with open("partner_list.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        for row in file_reader:
            partner_list.append([row[0], row[1]])

# сохранение и загрузка списка партнеров и связанных лиц
def save_partners_names_rel_to_pickle():
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(partners_names_rel_list, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error picking object:", ex)

def load_partners_names_rel_from_pickle():
    try:
        with open("data.pickle", "rb") as f:
            partners_names_rel_list = pickle.load(f)
    except Exception as ex:
        print("Error unpuck:", ex)


# собственно сам класс главного окна приложения
class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Center window")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.initUI()
    
    def centerWindow(self):
        w = 600
        h = 350

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    def initUI(self):
        self.parent.title("Печать разрешений")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Exit", command=self.quit)
        quitButton.place(x=400, y=300)

        label1 = Label(self, text="Контрагент")
        label2 = Label(self, text="Через кого")
        label3 = Label(self, text="Сумма")

        label1.place(x=20, y=20)
        label2.place(x=350, y=20)
        label3.place(x=500, y=20)

        # фильтрация по спискам при изменении полей ввода
        p_sv = StringVar(self)
        n_sv = StringVar(self)

        # два поля для фильтрации списков
        vcmd_p = (self.register(self.partner_do_validation), '%P')
        vcmd_n = (self.register(self.name_do_validation), '%P')
        find_partner_entry = Entry(self, width=20, textvariable=p_sv, validate="key", validatecommand=vcmd_p, font=16)
        find_name_entry = Entry(self, width=10, textvariable=n_sv, validate="key", validatecommand=vcmd_n, font=16)
        summ_entry = Entry(self, width=10)

        find_partner_entry.place(x=20, y=40)
        find_name_entry.place(x=350, y=40)
        summ_entry.place(x=500, y=40)

        # кнопка добавления нового лица
        add_name_button = tk.Button(self, text="+", command=self.click_add_name_button, width="3", height="1")
        add_name_button.place(x=450, y=40)

        # списки с контрагентами и лицами
        self.partner_listbox = Listbox(self, width=45)
        self.name_listbox = Listbox(self)

        for el in partner_list:
            self.partner_listbox.insert(END, f"{el[0]}/{el[1]}")

        for el in name_list:
            self.name_listbox.insert(END, el)

        self.partner_listbox.place(x=20, y=70)
        self.name_listbox.place(x=350, y=70)

        # скроллбары для списков
        plbox_scrollbar = Scrollbar(self, orient="vertical")
        plbox_scrollbar.config(command=self.partner_listbox.yview)
        plbox_scrollbar.pack(side="right", fill="y")

        nlbox_scrollbar = Scrollbar(self, orient="vertical")
        nlbox_scrollbar.config(command=self.name_listbox.yview)
        nlbox_scrollbar.pack(side="right", fill="y")
    
    def click_add_name_button(self):
        print("add")

    # методы для динамического поиска в контрагентах и именах
    def partner_do_validation(self, new_value):
        print(len(new_value))
        if len(new_value) != 0:
            if len(new_value) < 2:
                self.partner_listbox.delete(0, END)
                for el in partner_list:
                    self.partner_listbox.insert(END, f"{el[0]}/{el[1]}")
            elif len(new_value) > 2:
                self.partner_listbox.delete(0, END)
                for el in partner_list:
                    buf_el = el[0].lower()
                    new_value = new_value.lower()
                    if buf_el.find(new_value) != -1:
                        self.partner_listbox.insert(END, el[0])


        return True

    def name_do_validation(self, new_value):
        print(new_value)
        return True

def main():
    root = Tk()
    load_partners_names_rel_from_pickle()
    load_partners_from_csv()
    ex = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()