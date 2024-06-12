import winsound
from PIL import Image as Img
import hashlib
from Sections import *
from tkinter import messagebox as mb


class App(Tk):
    """Создает главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.choice = None
        self.title('Work_planner')
        self.geometry('700x600+400+70')
        self.resizable(False, False)
        self.config(bg="#004B87")
        self.my_font = ctk.CTkFont(family='Arial Narrow', size=18, weight='bold')
        img = ctk.CTkImage(light_image=Img.open('rosseti.png'), dark_image=Img.open("rosseti.png"), size=(410, 410))
        ctk.CTkLabel(master=self, image=img, text='').place(x=350, y=300)
        main_menu = ctk.CTkLabel(master=self, width=300, height=400)
        main_menu.grid(row=0, column=0, padx=10, pady=0)
        self.listbox = Listbox(main_menu, bg='#f2f9ff', width=40, height=15, font=self.my_font, fg="#002441")
        self.listbox.grid(row=0, column=0, pady=20, padx=5)
        self.listbox.insert(0, "Технологическое присоединение")
        self.listbox.insert(1, "Дополнительные сервисы")
        self.listbox.insert(2, "Жалобы и обращения")
        self.listbox.insert(3, "Задания")
        self.listbox.insert(END, "Управление")
        self.password_entry_for_registration = ctk.CTkEntry(self, width=200, font=self.my_font)
        self.login_entry_for_registration = ctk.CTkEntry(self, width=200, font=self.my_font)
        self.name_entry_for_registration = ctk.CTkEntry(self, width=200, font=self.my_font)
        self.name = ctk.CTkLabel(self, text='ФИО:', font=self.my_font, fg_color='#004B87', text_color='white')
        self.password_for_registration = ctk.CTkLabel(self, text='Пароль:', font=self.my_font, fg_color='#004B87',
                                                      text_color='white')
        self.login_for_registration = ctk.CTkLabel(self, text='Логин:', font=self.my_font, fg_color='#004B87',
                                                   text_color='white')
        self.password_entry = ctk.CTkEntry(self, width=200, font=self.my_font)
        self.login_entry = ctk.CTkEntry(self, width=200, font=self.my_font)
        self.listbox.bind('<Double-Button-1>', self.show_login)
        self.reg_button = ctk.CTkButton(self, text="Регистрация", font=self.my_font, hover_color='#d2ecfe',
                                        fg_color='white',
                                        text_color='#004B87', corner_radius=13,
                                        command=lambda: self.show_registration())
        self.reg_button.grid(row=1, column=0, padx=20, pady=10, sticky=N)
        self.registration_button = ctk.CTkButton(self, text="Зарегистрироваться", height=30, width=195,
                                                 font=self.my_font,
                                                 hover_color='#d2ecfe', fg_color='white',
                                                 text_color='#004B87', corner_radius=13,
                                                 command=lambda: self.registration(
                                                     self.login_entry_for_registration.get(),
                                                     hashlib.sha256(
                                                         self.password_entry_for_registration.get().encode()).hexdigest(),
                                                     self.name_entry_for_registration.get()))
        self.label_great = ctk.CTkLabel(self, text='Успешно!', text_color='green', font=self.my_font)

    def show_login(self, event):
        """Отображает поле ввода логина и пароля при двойном клике по данным в listbox"""
        self.choice = self.listbox.curselection()[0]
        login = ctk.CTkLabel(self, text='Логин:', font=self.my_font, fg_color='#004B87', text_color='white')
        login.grid(row=0, column=2, pady=20, sticky=N + W)
        self.login_entry.grid(row=0, column=2, padx=70, pady=20, sticky=N + W)
        password = ctk.CTkLabel(self, text='Пароль:', font=self.my_font, fg_color='#004B87', text_color='white')
        password.grid(row=0, column=2, pady=55, sticky=N + W)
        self.password_entry.grid(row=0, column=2, padx=70, pady=55, sticky=N + W)
        enter = ctk.CTkButton(self, text="Войти", font=self.my_font, hover_color='#d2ecfe', fg_color='white',
                              text_color='#004B87', corner_radius=13,
                              command=lambda: self.enter_in_app(self.login_entry.get(), self.password_entry.get()))
        enter.grid(row=0, column=2, padx=20, pady=90, sticky=N)

    def show_registration(self):
        """Показывает поле регистрации при нажатии на соответствующую кнопку"""
        self.init_file()
        self.reg_button.grid_remove()
        self.name.grid(row=1, column=0, pady=20, padx=5, sticky=N + W)
        self.name_entry_for_registration.grid(row=1, column=0, padx=70, pady=20, sticky=N + W)
        self.login_for_registration.grid(row=1, column=0, pady=55, padx=5, sticky=N + W)
        self.login_entry_for_registration.grid(row=1, column=0, padx=70, pady=55, sticky=N + W)
        self.password_for_registration.grid(row=1, column=0, pady=90, padx=5, sticky=N + W)
        self.password_entry_for_registration.grid(row=1, column=0, padx=70, pady=90, sticky=N + W)
        self.registration_button.grid(row=1, column=0, padx=1, pady=125, sticky=N)

    @staticmethod
    def init_file():
        """Создает файл пользователей"""
        if not os.path.exists('users.txt'):
            with open('users.txt', 'w'):
                pass

    def registration(self, login: str, password: str, name: str) -> bool:
        """Добавляет пользователя в файл"""
        if login == '' or password == '':
            mb.showinfo(title="Информация", message="Заполните все поля!")
        else:
            with open('users.txt', 'r') as f:
                users = f.read().splitlines()
            for user in users:
                args = user.split(':')
                if login == args[0]:
                    self.label_great.grid(row=1, column=0, padx=1, pady=160, sticky=N)
                    return False
            with open('users.txt', 'a') as f:
                f.write(f'{login}:{password}:{name}\n')

        winsound.PlaySound('sound.mp3', winsound.SND_ALIAS | winsound.SND_ASYNC)
        self.name.grid_remove()
        self.name_entry_for_registration.grid_remove()
        self.login_for_registration.grid_remove()
        self.login_entry_for_registration.grid_remove()
        self.password_for_registration.grid_remove()
        self.password_entry_for_registration.grid_remove()
        self.registration_button.grid_remove()
        self.name_entry_for_registration.delete(0, END)
        self.login_entry_for_registration.delete(0, END)
        self.password_entry_for_registration.delete(0, END)
        self.reg_button.grid(row=1, column=0, padx=20, pady=10, sticky=N)
        return True

    def get_user(self, login: str, password: str) -> bool:
        """Проверяет логин и пароль пользователя"""
        with open('users.txt', 'r') as f:
            users = f.read().splitlines()
        for user in users:
            args = user.split(':')
            try:
                if login == args[0] and password == args[1]:
                    return True
            except IndexError:
                ctk.CTkLabel(self, text='Неверный логин/пароль', font=self.my_font, text_color='red').grid(
                    row=0, column=2, pady=150, sticky=N + W)
        return False

    def enter_in_app(self, login: str, password: str):
        """Открытие соответствующего модального окна при введении логина,пароля и нажатии кнопки вход"""
        registered_user = self.get_user(login, hashlib.sha256(password.encode()).hexdigest())
        if self.choice == 1 and registered_user is True:
            Section('Сервисы').services()
        elif self.choice == 3 and registered_user is True:
            Section('Задания').tasks()
        elif self.choice == 2 and registered_user is True:
            Section('Обращения').appeals()
        elif self.choice == 0 and registered_user is True:
            Section('тех_прис').tech_conn()
        elif self.choice == 4 and registered_user is True:
            Section('Управление').control()
        else:
            ctk.CTkLabel(self, text='Неверный логин/пароль', font=self.my_font, text_color='red').grid(
                row=0, column=2, pady=150, sticky=N + W)
