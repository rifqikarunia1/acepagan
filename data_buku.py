from tkinter import *
from tkinter import ttk, messagebox as tkMessageBox
import sqlite3

class DataSiswa(object):
    def __init__(self):
        self.window = Tk()        
        self.window.title('Membuat Aplikasi CRUD TKinter')
        self.lebar = self.window.winfo_screenwidth() / 2
        self.tinggi = self.window.winfo_screenheight() / 2

        self.frame1 = Frame(
            self.window,
            height = self.tinggi / 2,
            width = self.lebar
        )
        self.frame1['relief'] = GROOVE        
        self.frame1.grid_propagate(0)
        self.frame1.pack(side=LEFT, fill=X, expand=False)

        self.frame2 = Frame(
            self.window,
            height = self.tinggi / 2,
            width = self.lebar / 3
        )
        self.frame2['relief'] = RIDGE
        self.frame2.grid_propagate(0)
        self.frame2.pack(side=RIGHT)        

        btn_add = Button(self.frame2)
        btn_add['text'] = 'Tambah'
        btn_add['command'] = self.add_data
        btn_add.grid(row=12, column=0, sticky=W + E)

        btn_all = Button(self.frame2)
        btn_all['text'] = 'All Data'
        btn_all['command'] = self.get_data
        btn_all.grid(row=12, column=1, sticky=W + E)

        btn_exit = Button(self.frame2)
        btn_exit['text'] = 'Exit'
        btn_exit['command'] = self.exit
        btn_exit.grid(row=12, column=2, sticky=W + E)

        self.btn_update = Button(
            self.frame2,
            text='Update',
            command=self.update_data,
            state=DISABLED
        )
        self.btn_update.grid(row=13, column=0, sticky=W + E)

        self.btn_delete = Button(
            self.frame2,
            text='Hapus',
            command=self.delete_data,
            state=DISABLED
        )
        self.btn_delete.grid(row=13, column=1, sticky=W + E)
    
    def exit(self):
        apakah = tkMessageBox.askquestion(
            'Mau keluar dari Aplikasi CRUD?',
            'Apakah mau keluar dari program?',
            icon='warning'
        )
        if apakah == 'yes':
            self.window.destroy()
            exit()

    def db_name(self):
        global conn, cursor
        conn = sqlite3.connect('datasiswa.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS datasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nama CHAR,
            npm INT,
            jurusan CHAR,
            gender CHAR            
        );''')

    def selected_data(self, query, parameters=[]):
        self.db_name()
        cursor.execute(query, parameters)
        conn.commit()
    
    def add_data(self):
        for widget in self.frame1.winfo_children():
            widget.grid_forget()            
        
        ListLabel = ('Judul ', 'Harga', 'Penulis')

        for i, l in enumerate(ListLabel):
            globals()['label%s' % i] = Label(self.frame1, text=l).grid(row=i, column=0, sticky=W)

        text1 = StringVar()
        text2 = IntVar()
        text3 = StringVar()
        textG = StringVar()

        text_1 = Entry(
            self.frame1,
            width = 30,
            textvariable=text1
        )
        text_1.grid(row=0, column=1, sticky=S)
        text_1.focus()

        text_2 = Entry(
            self.frame1,
            width = 30,
            textvariable=text2
        ).grid(row=1, column=1, sticky=S)

        text_3 = Entry(
            self.frame1,
            width = 30,
            textvariable=text3
        ).grid(row=2, column=1, sticky=S)
        
        choice = {'Pria', 'Wanita'}        
        #textG.set('Pria')
        text_G = OptionMenu(
            self.frame1,
            textG,
            *choice
        ).grid(row=3, column=1, sticky=W)
        
        def btn_save():
            query = 'INSERT INTO datasiswa VALUES(NULL, ?, ?, ?, ?)'            
            parameters = (text1.get(), text2.get(), text3.get(), textG.get())
            tkMessageBox.showinfo(
                'Berhasil',
                'Data siswa berhasil disimpan'
            )            
            self.selected_data(query, parameters)            
            return self.add_data()

        btn_sv = Button(
            self.frame1,
            text='Simpan',
            command=btn_save
        ).grid(row=12, column=0, sticky=E)
    
    def get_data(self):
        for widget in self.frame1.winfo_children():
            widget.grid_forget()

        query = "SELECT * FROM datasiswa"
        self.selected_data(query)
        Data = cursor.fetchall()

        self.tree = ttk.Treeview(self.frame1)
        self.tree['columns'] = ('NPM', 'Jurusan', 'Gender')
        self.tree.heading('#0', text='Nama')
        self.tree.heading('#1', text='NPM')
        self.tree.heading('#2', text='Jurusan')
        self.tree.heading('#3', text='Gender')
        for i, v in enumerate(Data):
            self.tree.grid(row=i)
            self.tree.insert('', END, iid=v[0], text=v[1], values=(v[2], v[3], v[4]))
        self.tree.bind('', self.on_select)
        cursor.close()
        conn.close()

    def on_select(self, event): # -> None
        item = self.tree.selection()
        if item is not None:
            self.btn_update['state'] = NORMAL
            self.btn_delete['state'] = NORMAL
        else:
            self.btn_update['state'] = DISABLED
            self.btn_delete['state'] = DISABLED
    
    def update_data(self):
        for widget in self.frame1.winfo_children():
            widget.grid_forget() 

        item = self.tree.selection()
        try:
            item
        except IndexError as e:
            tkMessageBox.showwarning(
                'Pilih Data',
                'Silahkan pilih data terlebih dahulu'
            )
            return
        iddata = int(item[0])
        query = "SELECT * FROM datasiswa WHERE id = ? ;"
        self.selected_data(query, (iddata, ))
        result = cursor.fetchall()

        ListLabel = ('Nama Lengkap', 'NPM', 'Jurusan')        
        for i, l in enumerate(ListLabel):            
            globals()['label%s' % i] = Label(self.frame1, text=l).grid(row=i, column=0, sticky=W)

        text1 = StringVar(value=result[0][1])
        text2 = IntVar(value=result[0][2])
        text3 = StringVar(value=result[0][3])
        textG = StringVar(value=result[0][4])

        text_1 = Entry(
            self.frame1,
            width = 30,
            textvariable=text1
        )
        text_1.grid(row=0, column=1, sticky=S)
        text_1.focus()

        text_2 = Entry(
            self.frame1,
            width = 30,
            textvariable=text2
        ).grid(row=1, column=1, sticky=S)

        text_3 = Entry(
            self.frame1,
            width = 30,
            textvariable=text3
        ).grid(row=2, column=1, sticky=S)
        
        choice = {'Pria', 'Wanita'}        
        #textG.set('Pria')
        text_G = OptionMenu(
            self.frame1,
            textG,
            *choice
        ).grid(row=3, column=1, sticky=W)
        
        def btn_save():
            query = '''UPDATE datasiswa SET nama = ?, npm = ?, jurusan = ?, gender = ? WHERE id = ?'''
            parameters = (text1.get(), text2.get(), text3.get(), textG.get(), iddata)
            tkMessageBox.showinfo(
                'Berhasil',
                'Data siswa berhasil diperbarui'
            )            
            self.selected_data(query, parameters)            
            return self.get_data()

        btn_sv = Button(
            self.frame1,
            text='Simpan',
            command=btn_save
        ).grid(row=12, column=0, sticky=E)
        cursor.close()
        conn.close()

    def delete_data(self):
        item = self.tree.selection()
        try:
            if item is not None:
                apakah = tkMessageBox.askquestion(
                    'Hapus Data',
                    'Apakah kamu akan menghapus data ini?'
                )
                if apakah == 'yes':
                    iddata = int(item[0])                
                    query = "DELETE FROM datasiswa WHERE id = ? ;"
                    self.selected_data(query, (iddata, ))
                    tkMessageBox.showinfo(
                        'Berhasil',
                        'Data berhasil dihapus'
                    )
                    self.get_data()
            else:
                tkMessageBox.showinfo(
                    'Pilih Data',
                    'Silahkan pilih data terlebih dahulu'
                )
                self.get_data()
        except IndexError:
            tkMessageBox.showinfo(
                'Pilih Data',
                'Silahkan pilih data terlebih dahulu'
            )
            self.get_data()
        cursor.close()
        conn.close()
    
def disable_event():
    pass

if __name__ == '__main__':
    w = DataSiswa()
    w.window.protocol("WM_DELETE_WINDOW", disable_event)
    w.window.mainloop()
