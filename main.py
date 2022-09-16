from asyncio.windows_events import NULL
from atexit import register
from gc import callbacks
from tkinter import END, StringVar, Tk, Frame, BOTH, Listbox, Scrollbar
from tkinter.ttk import Frame, Button, Style, Label, Entry


partner_list = [x for x in range(0, 100)]
name_list = [x for x in range(0, 100)]

p_listbox : Listbox
n_listbox : Listbox


# методы для динамического поиска в контрагентах и именах
def partner_do_validation(new_value):
    print(new_value)
    p_listbox.delete()
    return True

def name_do_validation(new_value):
    print(new_value)
    return True


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
        w = 500
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
        label2.place(x=140, y=20)
        label3.place(x=240, y=20)

        # фильтрация по спискам при изменении полей ввода
        p_sv = StringVar(self)
        n_sv = StringVar(self)
        
        # два поля для фильтрации списков
        vcmd_p = (self.register(partner_do_validation), '%P')
        vcmd_n = (self.register(name_do_validation), '%P')
        find_partner_entry = Entry(self, width=15, textvariable=p_sv, validate="key", validatecommand=vcmd_p)
        find_name_entry = Entry(self, width=15, textvariable=n_sv, validate="key", validatecommand=vcmd_n)
        summ_entry = Entry(self, width=15)

        find_partner_entry.place(x=20, y=40)
        find_name_entry.place(x=140, y=40)
        summ_entry.place(x=240, y=40)

        # списки с контрагентами и лицами
        partner_listbox = Listbox(self)
        name_listbox = Listbox(self)

        for el in partner_list:
            partner_listbox.insert(END, el)

        for el in name_list:
            name_listbox.insert(END, el)

        partner_listbox.place(x=20, y=60)
        name_listbox.place(x=140, y=60)

        p_listbox = partner_listbox
        n_listbox = name_listbox
        
        # скроллбары для списков
        plbox_scrollbar = Scrollbar(self, orient="vertical")
        plbox_scrollbar.config(command=partner_listbox.yview)
        plbox_scrollbar.pack(side="right", fill="y")

        nlbox_scrollbar = Scrollbar(self, orient="vertical")
        nlbox_scrollbar.config(command=name_listbox.yview)
        nlbox_scrollbar.pack(side="right", fill="y")


def main():
    root = Tk()
    ex = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()