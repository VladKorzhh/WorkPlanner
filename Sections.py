from Base import *
import customtkinter as ctk
import tkinter.ttk as ttk


class ColorTreeview(ttk.Treeview):
    """Класс добавляет возможность  выделения красным цветом строк таблицы с прошедшей датой"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_configure('red', background='#870007')

    def insert(self, parent_node, index, **kwargs):
        """Назначение тега при добавлении элемента в дерево"""
        item = super().insert(parent_node, index, **kwargs)
        values = kwargs.get('values', None)
        if len(values[11].split('.')) == 3:
            my_dt = dt.datetime.strptime(values[11], '%d.%m.%Y')
            if my_dt < dt.datetime.now():
                super().item(item, tag='red')
        return item


class Section(ctk.CTkToplevel):
    """Класс для создания модальных окон (Обращения, задания, ТехПрис и Сервисы)"""

    def __init__(self, title):
        super().__init__()
        self.my_font = ctk.CTkFont(family='Arial Narrow', size=18, weight='bold')
        self.control_font = ctk.CTkFont(family='Roboto Medium', size=20, weight='bold')
        self.list_of_columns = []
        self.values = []
        self.row = 0
        self.title(title)
        self.geometry('900x600+300+40')
        self.resizable(False, False)
        self.config(bg="#d5d8db")
        self.grab_set()
        self.focus_set()

    def set_combobox(self, txt, list_val, combo_val, row):
        """Создает визуальное отображение combobox для всех модальных окон"""
        if combo_val:
            ctk.CTkLabel(self, text=txt, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').grid(row=row,
                                                                                                           column=1,
                                                                                                           padx=20,
                                                                                                           pady=5,
                                                                                                           sticky=W)
            s = StringVar()
            ctk.CTkComboBox(self, values=combo_val, width=250, variable=s, bg_color='#d5d8db', font=self.my_font).grid(
                row=row, column=2)
            list_val.append(s)
        else:
            ctk.CTkLabel(self, text=txt, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').grid(row=row,
                                                                                                           column=1,
                                                                                                           padx=20,
                                                                                                           pady=5,
                                                                                                           sticky=W)
            s = StringVar()
            ent = ctk.CTkEntry(self, width=250, font=self.my_font, textvariable=s, bg_color='#d5d8db')
            ent.grid(row=row, column=2)
            list_val.append(s)

    def services(self):
        """Создание модального окна сервисов"""
        name_table = 'Сервисы'
        self.list_of_columns = ['№Обращения', 'Тип лица', 'Вид услуги', 'Дата оплаты', 'ФИО', 'Телефон',
                                'Населенный пункт', 'Улица', 'Дом', 'Квартира', 'Фазность ПУ', 'Номер ПУ',
                                'Сумма', 'Дата исполнения', 'Примечание']
        for column in self.list_of_columns:
            match column:
                case 'Примечание':
                    ctk.CTkLabel(self, text=column, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').place(
                        relx=0.51,
                        rely=0.016)
                    text = Text(self, width=35, height=10, font=self.my_font)
                    text.place(relx=0.65, rely=0.016)
                    var = StringVar()
                    var.set('нет')
                    ctk.CTkCheckBox(self, text='СТП', variable=var, onvalue='да', offvalue='нет',
                                    fg_color='#004B87', font=self.my_font, text_color='#004B87',
                                    bg_color='#d5d8db').place(relx=0.65,
                                                              rely=0.42)

                    self.values.append(var)
                case 'Тип лица':
                    Section.set_combobox(self, column, self.values, ['ЮЛ', 'ФЛ'], self.row)
                    self.row += 1
                case 'Вид услуги':
                    Section.set_combobox(self, column, self.values, ['Замена',
                                                                     'Замена МПИ',
                                                                     'Инструментальная проверка',
                                                                     'Присоединение жил проводов',
                                                                     'Переопломбировка',
                                                                     'Иное'], self.row)
                    self.row += 1
                case 'Фазность ПУ':
                    Section.set_combobox(self, column, self.values, ['1Ф', '3Ф', '3Ф ТТ'], self.row)
                    self.row += 1
                case _:
                    Section.set_combobox(self, column, self.values, False, self.row)
                    self.row += 1
        self.list_of_columns.insert(14, 'СТП')
        create_service = ctk.CTkButton(self, text="Создать задание", font=self.my_font, height=40,
                                       bg_color='#d5d8db', fg_color='#004B87', width=80,
                                       command=lambda: Base.add_row_in_table(name_table, self.list_of_columns,
                                                                             self.values, text, self))
        create_service.place(relx=0.82, rely=0.89)

    def tasks(self):
        """Создание модального окна заданий"""
        name_table = 'Задания'
        self.list_of_columns = ['Место прибора', 'Тип лица', 'ФИО', 'Телефон', 'Населенный пункт', 'Улица', 'Дом',
                                'Квартира', 'Фазность ПУ', 'Номер ПУ', 'Задание', 'Дата исполнения', 'Примечание']
        for column in self.list_of_columns:
            match column:
                case 'Примечание':
                    ctk.CTkLabel(self, text=column, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').place(
                        relx=0.51,
                        rely=0.016)
                    text = Text(self, width=35, height=10, font=self.my_font)
                    text.place(relx=0.65, rely=0.016)
                case 'Тип лица':
                    Section.set_combobox(self, column, self.values, ['ЮЛ', 'ФЛ'], self.row)
                    self.row += 1
                case 'Фазность ПУ':
                    Section.set_combobox(self, column, self.values, ['1Ф', '3Ф', '3Ф ТТ'], self.row)
                    self.row += 1
                case _:
                    Section.set_combobox(self, column, self.values, False, self.row)
                    self.row += 1
            create_service = ctk.CTkButton(self, text="Создать задание", font=self.my_font, height=40,
                                           width=80, bg_color='#d5d8db', fg_color='#004B87',
                                           command=lambda: Base.add_row_in_table(name_table, self.list_of_columns,
                                                                                 self.values, text, self))
            create_service.place(relx=0.82, rely=0.89)

    def appeals(self):
        """Создание модального окна заданий"""
        name_table = 'Обращения'
        self.list_of_columns = ['№Обращения', 'Тип лица', 'ФИО', 'Телефон', 'Населенный пункт', 'Улица', 'Дом',
                                'Квартира', 'Вид обращения', 'Причина обращения', 'Дата регистрации', 'Дата исполнения',
                                'Примечание']
        for column in self.list_of_columns:
            match column:
                case 'Примечание':
                    ctk.CTkLabel(self, text=column, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').place(
                        relx=0.51,
                        rely=0.016)
                    text = Text(self, width=35, height=10, font=self.my_font)
                    text.place(relx=0.65, rely=0.016)
                case 'Тип лица':
                    Section.set_combobox(self, column, self.values, ['ЮЛ', 'ФЛ'], self.row)
                    self.row += 1
                case 'Вид обращения':
                    Section.set_combobox(self, column, self.values, ['Жалоба', 'Заявление'], self.row)
                    self.row += 1
                case 'Причина обращения':
                    Section.set_combobox(self, column, self.values,
                                         ['Качество', 'Наружное освещение', 'Обследование ЛЭП', 'Расчистка трассы',
                                          'Прочее'], self.row)
                    self.row += 1
                case _:
                    Section.set_combobox(self, column, self.values, False, self.row)
                    self.row += 1
            create_service = ctk.CTkButton(self, text="Создать задание", font=self.my_font, height=40,
                                           width=80, bg_color='#d5d8db', fg_color='#004B87',
                                           command=lambda: Base.add_row_in_table(name_table, self.list_of_columns,
                                                                                 self.values, text, self))
            create_service.place(relx=0.82, rely=0.89)

    def tech_conn(self):
        """Создание модального окна технологических присоединений"""
        name_table = 'ТехПрис'
        self.geometry('970x700+300+40')
        self.list_of_columns = ['№Заявки', '№Договора', 'Тип лица', 'Наименование объекта', 'Населенный пункт',
                                'Улица', 'Дом', 'Квартира', 'ФИО', 'Телефон', 'Тип подключения', 'Категория надежности',
                                'Pmax, кВт', 'U,кВ', 'Источник', 'Дата заключения договора', 'Дата исполнения',
                                'Примечание']
        for column in self.list_of_columns:
            match column:
                case 'Примечание':
                    ctk.CTkLabel(self, text=column, font=self.my_font, text_color='#004B87', bg_color='#d5d8db').place(
                        relx=0.51,
                        rely=0.016)
                    text = Text(self, width=35, height=10, font=self.my_font)
                    text.place(relx=0.65, rely=0.016)
                case 'Тип лица':
                    Section.set_combobox(self, column, self.values, ['ЮЛ', 'ФЛ'], self.row)
                    self.row += 1
                case 'Тип подключения':
                    Section.set_combobox(self, column, self.values,
                                         ['Новое ТП', 'Увеличение ММ', 'Изменение точки присоединения',
                                          'Смена собственника', 'Опосредованное ТП', 'Уменьшение ММ'], self.row)
                    self.row += 1
                case 'Категория надежности':
                    Section.set_combobox(self, column, self.values, ['1', '2', '3'], self.row)
                    self.row += 1
                case 'U,кВ':
                    Section.set_combobox(self, column, self.values, ['0,23кВ', '0,4кВ', '10кВ'], self.row)
                    self.row += 1
                case _:
                    Section.set_combobox(self, column, self.values, False, self.row)
                    self.row += 1
            create_service = ctk.CTkButton(self, text="Создать задание", font=self.my_font, height=40,
                                           width=80, bg_color='#d5d8db', fg_color='#004B87',
                                           command=lambda: Base.add_row_in_table(name_table, self.list_of_columns,
                                                                                 self.values, text, self))
            create_service.place(relx=0.82, rely=0.89)

    def control(self):
        """Создание модального окна управления данными"""
        self.geometry('1720x790+300+40')
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=20, fieldbackground="#343638",
                        bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])
        frame_left = ctk.CTkFrame(master=self, width=250, corner_radius=0, fg_color='#d5d8db')
        frame_left.grid(row=0, column=0, sticky="nswe")
        frame_right = ctk.CTkFrame(master=self, fg_color='grey', corner_radius=11, bg_color='#d5d8db')
        frame_right.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(8, minsize=20)
        frame_left.grid_rowconfigure(11, minsize=10)
        add_menu_display211 = ctk.CTkFrame(master=frame_right, corner_radius=15, height=400, width=600)
        add_menu_display211.grid(pady=12, padx=14, sticky="nws")
        columns = (
            'id', 'ФИО', 'Тип лица', 'Телефон', '№ Прибора учета', 'Фазность', 'Населенный пункт', 'Улица', 'Дом',
            'Квартира', 'Задание', 'Дата исполнения', 'CТП')
        self.option_add("*tearOff", FALSE)
        main_menu = Menu()
        file_menu = Menu()
        report_menu = Menu()
        base_menu = Menu()
        help_menu = Menu()
        file_menu.add_command(label="Выгрузить сервисы", command=lambda: Base.unload_table('Сервисы'))
        file_menu.add_separator()
        file_menu.add_command(label="Выгрузить техприсы", command=lambda: Base.unload_table('ТехПрис'))
        file_menu.add_separator()
        file_menu.add_command(label="Выгрузить задания", command=lambda: Base.unload_table('Задания'))
        file_menu.add_separator()
        file_menu.add_command(label="Выгрузить обращения", command=lambda: Base.unload_table('Обращения'))
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_cascade(label="Отчеты", menu=report_menu)
        report_menu.add_command(label="Недельный", command=Base.make_report)
        base_menu.add_command(label="Сделать дамп", command=Base.make_dump)
        main_menu.add_cascade(label="База", menu=base_menu)
        help_menu.add_command(label="О программе")
        help_menu.add_separator()
        help_menu.add_command(label="Инструкция пользователя")
        main_menu.add_cascade(label="Помощь", menu=help_menu)
        self.config(menu=main_menu)
        table = ColorTreeview(master=add_menu_display211,
                              columns=columns,
                              height=35,
                              selectmode='browse',
                              show='headings')
        for i in columns:
            if i in ('id', "Дом", "CТП", "Код"):
                table.column(i, minwidth=45, width=45, anchor=CENTER)
                table.heading(i, text=i)
            elif i in ("Тип лица", "Квартира", "Фазность"):
                table.column(i, minwidth=65, width=65, anchor=CENTER)
                table.heading(i, text=i)
            elif i == "Задание":
                table.column(i, minwidth=300, width=300, anchor=CENTER)
                table.heading(i, text=i)
            else:
                table.column(i, minwidth=130, width=130, anchor=CENTER)
                table.heading(i, text=i)
        table.bind('<Motion>', 'break')
        scroll = ttk.Scrollbar(master=add_menu_display211, orient=VERTICAL, command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        table.pack(fill=BOTH, expand=YES)

        locality = ctk.CTkLabel(master=frame_left, text='Населенный пункт', font=self.control_font,
                                text_color='#565b5e')
        locality.grid(row=0, column=0, pady=7, padx=20)
        locality_var = StringVar()
        locality_entry = ctk.CTkEntry(master=frame_left, width=200, font=self.control_font, textvariable=locality_var)
        locality_entry.grid(row=1, column=0, padx=20)
        street = ctk.CTkLabel(master=frame_left, text='Улица / Переулок', font=self.control_font, text_color='#565b5e')
        street.grid(row=2, column=0, pady=7, padx=20)
        street_var = StringVar()
        street_entry = ctk.CTkEntry(master=frame_left, width=200, font=self.control_font, textvariable=street_var)
        street_entry.grid(row=3, column=0, padx=20)
        check_var = StringVar()
        check_var.set('нет')
        ctk.CTkCheckBox(self, text='Объединять', variable=check_var, onvalue='да', offvalue='нет',
                        fg_color='#004B87', font=self.control_font, text_color='#565b5e',
                        bg_color='#d5d8db').place(x=97, y=310, anchor=CENTER)
        button_1 = ctk.CTkButton(master=frame_left,
                                 font=self.control_font,
                                 text="Найти",
                                 corner_radius=15,
                                 border_width=3,
                                 border_color="#004B87",
                                 fg_color="#565b5e",
                                 width=200,
                                 command=lambda: Base.route(table, str(locality_var.get()), str(street_var.get()),
                                                            check_var.get()))
        button_1.grid(row=4, column=0, pady=10, padx=20)
        button_2 = ctk.CTkButton(master=frame_left,
                                 font=self.control_font,
                                 text="Изменить",
                                 corner_radius=15,
                                 border_width=3,
                                 border_color="#004B87",
                                 fg_color="#565b5e",
                                 width=200,
                                 command=lambda: Section.edit(self, table))
        button_2.grid(row=5, column=0, padx=20)
        button_3 = ctk.CTkButton(master=frame_left,
                                 font=self.control_font,
                                 text="Выполнить",
                                 corner_radius=15,
                                 border_width=3,
                                 border_color="#004B87",
                                 fg_color="#565b5e",
                                 width=200,
                                 command=lambda: Base.get_table_row(table, self))
        button_3.grid(row=6, column=0, pady=10, padx=20)
        button_4 = ctk.CTkButton(master=frame_left,
                                 font=self.control_font,
                                 text="Сформировать",
                                 corner_radius=15,
                                 border_width=3,
                                 border_color="#004B87",
                                 fg_color="#565b5e",
                                 width=200,
                                 command=lambda: Base.upload_route_to_excel(columns, table))
        button_4.place(x=122, y=736, anchor=CENTER)

    def edit(self, table):
        """Создание модального окна по редактированию строк таблицы"""
        selected = table.selection()
        if selected:
            selected_item = table.selection()[0]
            row_values = table.item(selected_item, option="values")
            db = sqlite3.connect(Base.PATH)
            cursor = db.cursor()
            for i in Base.TP_LIST:
                name_table = 'ТехПрис'
                if row_values[10] == i:
                    cursor.execute(f'''SELECT * FROM ТехПрис WHERE id ={row_values[0]}''')
                    tp_rows = cursor.fetchall()
                    db.commit()
                    string_vars = [StringVar() for k in range(17)]
                    tp_master = EditTable(self)
                    for j in tp_rows[0][1:18]:
                        ent = ctk.CTkEntry(tp_master, width=350, font=self.my_font,
                                           textvariable=string_vars[tp_master.ROW])
                        ent.grid(row=tp_master.ROW, column=0)
                        ent.insert(tp_master.ROW, str(j))
                        lbl = ctk.CTkLabel(tp_master, width=250, font=self.my_font,
                                           text=tp_master.TECH_CONN_COLUMNS[tp_master.ROW],
                                           anchor="w")
                        lbl.grid(row=tp_master.ROW, column=1)
                        tp_master.ROW += 1
                    btn = ctk.CTkButton(tp_master, text='Изменить', font=self.control_font, corner_radius=15,
                                        border_width=3,
                                        border_color="#004B87",
                                        fg_color="#565b5e",
                                        width=200,
                                        command=lambda: Section.paste_row(name_table, tp_rows, string_vars, self))
                    btn.place(x=270, y=520, anchor=CENTER)
                    tp_master.mainloop()
                    EditTable.TASK = False
                    tp_master.ROW = 0
            for i in Base.SERVICE_LIST:
                name_table = 'Сервисы'
                if row_values[10] == i:
                    cursor.execute(f'''SELECT * FROM Сервисы WHERE id ={row_values[0]}''')
                    sv_rows = cursor.fetchall()
                    db.commit()
                    string_vars = [StringVar() for k in range(15)]
                    sv_master = EditTable(self)
                    for j in sv_rows[0][1:16]:
                        ent = ctk.CTkEntry(sv_master, width=350, font=self.my_font,
                                           textvariable=string_vars[sv_master.ROW])
                        ent.grid(row=sv_master.ROW, column=0)
                        ent.insert(sv_master.ROW, str(j))
                        lbl = ctk.CTkLabel(sv_master, width=250, font=self.my_font,
                                           text=sv_master.SERVICES_COLUMNS[sv_master.ROW],
                                           anchor="w")
                        lbl.grid(row=sv_master.ROW, column=1)
                        sv_master.ROW += 1
                    btn = ctk.CTkButton(sv_master, text='Изменить', font=self.control_font, corner_radius=15,
                                        border_width=3,
                                        border_color="#004B87",
                                        fg_color="#565b5e",
                                        width=200,
                                        command=lambda: Section.paste_row(name_table, sv_rows, string_vars, self))
                    btn.place(x=270, y=520, anchor=CENTER)
                    sv_master.mainloop()
                    EditTable.TASK = False
                    sv_master.ROW = 0
            for i in Base.APPEAL_LIST:
                name_table = 'Обращения'
                if row_values[10] == i:
                    cursor.execute(f'''SELECT * FROM Обращения WHERE id ={row_values[0]}''')
                    ap_rows = cursor.fetchall()
                    db.commit()
                    string_vars = [StringVar() for k in range(12)]
                    ap_master = EditTable(self)
                    for j in ap_rows[0][1:13]:
                        ent = ctk.CTkEntry(ap_master, width=350, font=self.my_font,
                                           textvariable=string_vars[ap_master.ROW])
                        ent.grid(row=ap_master.ROW, column=0)
                        ent.insert(ap_master.ROW, str(j))
                        lbl = ctk.CTkLabel(ap_master, width=250, font=self.my_font,
                                           text=ap_master.APPEALS_COLUMNS[ap_master.ROW],
                                           anchor="w")
                        lbl.grid(row=ap_master.ROW, column=1)
                        ap_master.ROW += 1
                    btn = ctk.CTkButton(ap_master, text='Изменить', font=self.control_font, corner_radius=15,
                                        border_width=3,
                                        border_color="#004B87",
                                        fg_color="#565b5e",
                                        width=200,
                                        command=lambda: Section.paste_row(name_table, ap_rows, string_vars, self))
                    btn.place(x=270, y=520, anchor=CENTER)
                    ap_master.mainloop()
                    EditTable.TASK = False
                    ap_master.ROW = 0
            if EditTable.TASK:
                name_table = 'Задания'
                cursor.execute(f'''SELECT * FROM Задания WHERE id ={row_values[0]}''')
                tk_rows = cursor.fetchall()
                db.commit()
                string_vars = [StringVar() for k in range(12)]
                tk_master = EditTable(self)
                for j in tk_rows[0][1:13]:
                    ent = ctk.CTkEntry(tk_master, width=350, font=self.my_font,
                                       textvariable=string_vars[tk_master.ROW])
                    ent.grid(row=tk_master.ROW, column=0)
                    ent.insert(tk_master.ROW, str(j))
                    lbl = ctk.CTkLabel(tk_master, width=250, font=self.my_font,
                                       text=tk_master.TASK_COLUMNS[tk_master.ROW],
                                       anchor="w")
                    lbl.grid(row=tk_master.ROW, column=1)
                    tk_master.ROW += 1
                btn = ctk.CTkButton(tk_master, text='Изменить', font=self.control_font, corner_radius=15,
                                    border_width=3,
                                    border_color="#004B87",
                                    fg_color="#565b5e",
                                    width=200,
                                    command=lambda: Section.paste_row(name_table, tk_rows, string_vars, self))
                btn.place(x=270, y=520, anchor=CENTER)
                tk_master.mainloop()
                tk_master.ROW = 0

    @staticmethod
    def paste_row(name_table, tp_rows, string_vars, parent_window):
        """Вставка изменений в базу данных"""
        for i in string_vars:
            Base.VALUES_LIST.append(Base.QUOTES + i.get() + Base.QUOTES)
        db = sqlite3.connect(Base.PATH)
        cursor = db.cursor()
        match name_table:
            case 'ТехПрис':
                cursor.execute(f"""UPDATE ТехПрис SET [№Заявки]={Base.VALUES_LIST[0]},
                                                  [№Договора]={Base.VALUES_LIST[1]},
                                                  [Тип лица]={Base.VALUES_LIST[2]},
                                                  [Наименование объекта]={Base.VALUES_LIST[3]},
                                                  [Населенный пункт]={Base.VALUES_LIST[4]},
                                                  [Улица]={Base.VALUES_LIST[5]},
                                                  [Дом]={Base.VALUES_LIST[6]},
                                                  [Квартира]={Base.VALUES_LIST[7]},
                                                  [ФИО]={Base.VALUES_LIST[8]},
                                                  [Телефон]={Base.VALUES_LIST[9]},
                                                  [Тип подключения]={Base.VALUES_LIST[10]},
                                                  [Категория надежности]={Base.VALUES_LIST[11]},
                                                  [Pmax, кВт]={Base.VALUES_LIST[12]},
                                                  [U,кВ]={Base.VALUES_LIST[13]},
                                                  [Источник]={Base.VALUES_LIST[14]},
                                                  [Дата заключения договора]={Base.VALUES_LIST[15]},
                                                  [Дата исполнения]={Base.VALUES_LIST[16]}
                                    WHERE id = {tp_rows[0][0]};""")
                db.commit()
                cursor.close()
                Base.VALUES_LIST = []
            case 'Сервисы':
                cursor.execute(f"""UPDATE Сервисы SET [№Обращения]={Base.VALUES_LIST[0]},
                                                  [Тип лица]={Base.VALUES_LIST[1]},
                                                  [Вид услуги]={Base.VALUES_LIST[2]},
                                                  [Дата оплаты]={Base.VALUES_LIST[3]},
                                                  [ФИО]={Base.VALUES_LIST[4]},
                                                  [Телефон]={Base.VALUES_LIST[5]},
                                                  [Населенный пункт]={Base.VALUES_LIST[6]},
                                                  [Улица]={Base.VALUES_LIST[7]},
                                                  [Дом]={Base.VALUES_LIST[8]},
                                                  [Квартира]={Base.VALUES_LIST[9]},
                                                  [Фазность ПУ]={Base.VALUES_LIST[10]},
                                                  [Номер ПУ]={Base.VALUES_LIST[11]},
                                                  [Сумма]={Base.VALUES_LIST[12]},
                                                  [СТП]={Base.VALUES_LIST[13]},
                                                  [Дата исполнения]={Base.VALUES_LIST[14]}
                                WHERE id = {tp_rows[0][0]};""")
                db.commit()
                cursor.close()
                Base.VALUES_LIST = []
            case 'Обращения':
                cursor.execute(f"""UPDATE Обращения SET [№Обращения]={Base.VALUES_LIST[0]},
                                                  [Тип лица]={Base.VALUES_LIST[1]},
                                                  [ФИО]={Base.VALUES_LIST[2]},
                                                  [Телефон]={Base.VALUES_LIST[3]},
                                                  [Населенный пункт]={Base.VALUES_LIST[4]},
                                                  [Улица]={Base.VALUES_LIST[5]},
                                                  [Дом]={Base.VALUES_LIST[6]},
                                                  [Квартира]={Base.VALUES_LIST[7]},
                                                  [Вид обращения]={Base.VALUES_LIST[8]},
                                                  [Причина обращения]={Base.VALUES_LIST[9]},
                                                  [Дата регистрации]={Base.VALUES_LIST[10]},
                                                  [Дата исполнения]={Base.VALUES_LIST[11]}
                                WHERE id = {tp_rows[0][0]};""")
                db.commit()
                cursor.close()
                Base.VALUES_LIST = []
            case _:
                cursor.execute(f"""UPDATE Задания SET [Место прибора]={Base.VALUES_LIST[0]},
                                                  [Тип лица]={Base.VALUES_LIST[1]},
                                                  [ФИО]={Base.VALUES_LIST[2]},
                                                  [Телефон]={Base.VALUES_LIST[3]},
                                                  [Населенный пункт]={Base.VALUES_LIST[4]},
                                                  [Улица]={Base.VALUES_LIST[5]},
                                                  [Дом]={Base.VALUES_LIST[6]},
                                                  [Квартира]={Base.VALUES_LIST[7]},
                                                  [Фазность ПУ]={Base.VALUES_LIST[8]},
                                                  [Номер ПУ]={Base.VALUES_LIST[9]},
                                                  [Задание]={Base.VALUES_LIST[10]},
                                                  [Дата исполнения]={Base.VALUES_LIST[11]}
                                WHERE id = {tp_rows[0][0]};""")
                db.commit()
                cursor.close()
                Base.VALUES_LIST = []
        mb.showinfo(title="Информация", message="Успешно!", parent=parent_window)


class EditTable(ctk.CTkToplevel):
    """Класс создающий модальное окно по редактированию данных в таблицах"""
    TECH_CONN_COLUMNS = ('№Заявки', '№Договора', 'Тип лица', 'Наименование объекта', 'Населенный пункт', 'Улица', 'Дом',
                         'Квартира', 'ФИО', 'Телефон', 'Тип подключения', 'Категория надежности', 'Pmax,кВт', 'U,кВ',
                         'Источник', 'Дата заключения договора', 'Дата исполнения', 'Примечание')

    SERVICES_COLUMNS = ('№Обращения', 'Тип лица', 'Вид услуги', 'Дата оплаты', 'ФИО', 'Телефон', 'Населенный пункт',
                        'Улица', 'Дом', 'Квартира', 'Фазность ПУ', 'Номер ПУ', 'Сумма', 'СТП', 'Дата исполнения')

    APPEALS_COLUMNS = ('№Обращения', 'Тип лица', 'ФИО', 'Телефон', 'Населенный пункт', 'Улица', 'Дом', 'Квартира',
                       'Вид обращения', 'Причина обращения', 'Дата регистрации', 'Дата исполнения')

    TASK_COLUMNS = ('Место прибора', 'Тип лица', 'ФИО', 'Телефон', 'Населенный пункт', 'Улица', 'Дом', 'Квартира',
                    'Фазность ПУ', 'Номер ПУ', 'Задание', 'Дата исполнения')

    ROW = 0

    TASK = True

    def __init__(self, master):
        super().__init__(master)
        self.title('Редактирование заявки')
        self.geometry('560x550+400+70')
        self.grab_set()
        self.focus_set()
