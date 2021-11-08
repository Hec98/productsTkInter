from os import path
from tkinter import Tk, LabelFrame, Label, Entry, Button, ttk
import sqlite3 

class Product:
    db_name = 'db/database.db'
    def __init__(self, window):
        self.wind = window
        self.wind.title('Administración de ingresos')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Nuevo registro', borderwidth = 0)
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        # Name Input
        Label(frame, text = 'Ingreso: ').grid(row = 1, column = 0)
        self.entry = Entry(frame)
        self.entry.focus()
        self.entry.grid(row = 1, column = 1)

        # Price Input
        Label(frame, text = 'Importe: ').grid(row = 2, column = 0)
        self.amount = Entry(frame)
        self.amount.grid(row = 2, column = 1)

        # Button Add Product
        ttk.Button(frame, text = 'Guardar', command = self.add_product).grid(row = 3, columnspan = 2, sticky = 'W E')

        # Output Messages
        self.message = Label(frame, text = '', fg = 'red')
        self.message.grid(row = 4, column = 0, columnspan = 2,sticky = 'W E')

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 1, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Ingreso')
        self.tree.heading('#1', text = 'Importe')
        
        # Buttons
        ttk.Button(text = 'Eliminar').grid(row = 2, column = 0, pady = 10, sticky = 'W E')
        ttk.Button(text = 'Actualizar').grid(row = 2, column = 1, pady = 10, sticky = 'W E')
        ttk.Button(text = 'Cerrar', command = self.wind.quit).grid(row = 3, column = 0, columnspan = 2, sticky = 'W E')

        # Filling the Row
        self.get_products()
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records: self.tree.delete(element)

        # Query data
        query = 'SELECT * FROM data ORDER BY entry DESC'
        db_rows = self.run_query(query)

        # Fulling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
    
    def validation(self):
        return len(self.entry.get()) != 0 and len(self.amount.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO data VALUES(NULL, ?, ?)'
            parameters = (self.entry.get(), self.amount.get())
            self.run_query(query, parameters)
            self.message['text'] = '{} agregado correctamente'.format(self.entry.get())
            self.entry.delete(0, len(self.entry.get()))
            self.amount.delete(0, len(self.amount.get()))
        else:
            self.message['text'] = 'Se requiere ingreso e importe'
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
