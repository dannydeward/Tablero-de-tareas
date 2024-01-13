import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class KanbanBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablero Kanban")

        # Definir colores para cada columna
        self.column_colors = {"Pendiente": "red", "En Progreso": "green", "Completado": "blue"}

        # Crear columnas
        self.column_names = ["Pendiente", "En Progreso", "Completado"]
        self.columns = {name: tk.Listbox(root, selectmode=tk.SINGLE, bg="white") for name in self.column_names}

        # Agregar eventos de doble clic y clic derecho a las columnas
        for column_name in self.column_names:
            self.columns[column_name].bind("<Double-1>", lambda event, column_name=column_name: self.move_or_delete_task(event, column_name))
            self.columns[column_name].bind("<Button-3>", lambda event, column_name=column_name: self.add_task(event, column_name))

        # Ubicar columnas en la ventana
        for i, name in enumerate(self.column_names):
            label = tk.Label(root, text=name, bg=self.column_colors[name], font=("Helvetica", 12, "bold"), pady=5)
            label.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

            self.columns[name].grid(row=1, column=i, padx=10, pady=10, sticky="nsew")
            self.columns[name].insert(tk.END, f"{name} Tarea 1", f"{name} Tarea 2")

        # Configurar el diseño de la ventana
        for i in range(len(self.column_names)):
            self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(1, weight=1)

    def move_or_delete_task(self, event, from_column):
        selected_index = self.columns[from_column].curselection()
        if selected_index:
            task = self.columns[from_column].get(selected_index)

            # Determinar la acción en función de la columna actual
            if from_column == "Completado":
                # Eliminar tarea cuando se completa
                self.columns[from_column].delete(selected_index)
                messagebox.showinfo("Tarea completada", f"La tarea '{task}' se ha completado y se eliminó.")
            else:
                # Mover tarea a la siguiente columna
                to_column = self.get_next_column(from_column)
                self.columns[to_column].insert(tk.END, task)
                self.columns[from_column].delete(selected_index)
                messagebox.showinfo("Movimiento de tarea", f"La tarea '{task}' se movió de {from_column} a {to_column}.")

    def add_task(self, event, to_column):
        task = simpledialog.askstring("Nueva Tarea", "Ingrese el nombre de la nueva tarea:")
        if task:
            self.columns[to_column].insert(tk.END, task)
            messagebox.showinfo("Nueva Tarea", f"Se agregó una nueva tarea '{task}' a la columna {to_column}.")

    def get_next_column(self, current_column):
        index = self.column_names.index(current_column)
        if index < len(self.column_names) - 1:
            return self.column_names[index + 1]
        else:
            return current_column

if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanBoard(root)
    root.mainloop()
