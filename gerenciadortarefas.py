import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class AdminTarefas:
    def __init__(self):
        self.root = Tk()
        self.conecta_bd()  # Conecta ao banco de dados e cria tabelas
        self.setup_ui()
        self.root.mainloop()

    def conecta_bd(self):
        """Conecta ao banco de dados e cria as tabelas necessárias."""
        self.conn = sqlite3.connect("tarefas.db")
        self.cursor = self.conn.cursor()

        # Criação da tabela tarefas (tarefas ativas)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, atividade TEXT NOT NULL)""")

        # Criação da tabela historico (histórico de tarefas realizadas)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade TEXT NOT NULL)""")

        self.conn.commit()

    def setup_ui(self):
        """Cria a interface gráfica."""
        self.root.title("Gerenciador de Tarefas")
        self.root.configure(background="#FAFAD2")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Frame principal
        self.main_frame = Frame(self.root, bd=4, bg="#87CEEB", highlightbackground="#778899", highlightthickness=2)
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Botões
        self.add_task_button = Button(self.main_frame, text="Adicionar Tarefa", bg="#32CD32", fg="white", font=("verdana", 10, "bold"), command=self.add_atividade)
        self.add_task_button.place(relx=0.3, rely=0.05, relwidth=0.4, relheight=0.05)

        self.save_tasks_button = Button(self.main_frame, text="Salvar Tarefas", bg="#FFA500", fg="white", font=("verdana", 10, "bold"), command=self.save_atividades)
        self.save_tasks_button.place(relx=0.05, rely=0.15, relwidth=0.4, relheight=0.05)
              
               
        self.list_history_button = Button(self.main_frame, text="Listar Tarefas Salvas", bg="#808080", fg="white", font=("verdana", 10, "bold"), command=self.list_historico_atividades)
        self.list_history_button.place(relx=0.3, rely=0.25, relwidth=0.4, relheight=0.05)

        self.delete_all_button = Button(self.main_frame, text="Apagar Todas as Tarefas", bg="#FF0000", fg="white", font=("verdana", 10, "bold"), command=self.delete_all_atividades)
        self.delete_all_button.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.05)
        
        
        self.remove_task_button = Button(self.main_frame, text="Remover Tarefa", bg="#DC143C", fg="white", font=("verdana", 10, "bold"), command=self.remove_atividade)
        self.remove_task_button.place(relx=0.55, rely=0.15, relwidth=0.4, relheight=0.05)
                     
                
        
        # Campo de entrada e lista de tarefas
        self.atividade_entry = Entry(self.main_frame, font=("verdana", 10))
        self.atividade_entry.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.05)

        self.atividade_list = Listbox(self.main_frame, font=("verdana", 10))
        self.atividade_list.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3)

    def add_atividade(self):
        """Adiciona uma tarefa ao banco de dados."""
        atividade = self.atividade_entry.get()
        if atividade:
            self.cursor.execute("INSERT INTO tarefas (atividade) VALUES (?)", (atividade,))
            self.conn.commit()
            self.atividade_entry.delete(0, END)
            self.list_saved_atividades()  # Atualiza a lista de tarefas
        else:
            messagebox.showwarning("Aviso", "Digite uma tarefa para adicionar!")


    def remove_atividade(self):
        """Remove a tarefa selecionada do banco de dados."""
        selected_indices = self.atividade_list.curselection()
        if selected_indices:
            index = selected_indices[0]
            atividade = self.atividade_list.get(index)

            # Remove do banco de dados
            self.cursor.execute("DELETE FROM tarefas WHERE atividade = ?", (atividade,))
            self.conn.commit()

            # Atualiza a lista de tarefas
            self.list_saved_atividades()
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")
            
            

    def save_atividades(self):
        """Move as tarefas para o histórico."""
        self.cursor.execute("SELECT * FROM tarefas")
        tarefas = self.cursor.fetchall()

        if tarefas:
            for tarefa in tarefas:
                self.cursor.execute("INSERT INTO historico (atividade) VALUES (?)", (tarefa[1],))
            self.cursor.execute("DELETE FROM tarefas")  # Remove todas as tarefas ativas
            self.conn.commit()

            self.list_saved_atividades()  # Atualiza a lista de tarefas
            messagebox.showinfo("Sucesso", "Tarefas salvas no histórico!")
        else:
            messagebox.showwarning("Aviso", "Não há tarefas para salvar!")
            
            

    def list_saved_atividades(self):
        """Lista todas as tarefas salvas no banco de dados."""
        self.atividade_list.delete(0, END)  # Limpa a lista visual

        self.cursor.execute("SELECT atividade FROM tarefas")
        tarefas = self.cursor.fetchall()

        for tarefa in tarefas:
            self.atividade_list.insert(END, tarefa[0])
            
            
            

    def list_historico_atividades(self):
        """Lista todas as tarefas no histórico."""
        self.atividade_list.delete(0, END)  # Limpa a lista visual

        self.cursor.execute("SELECT atividade FROM historico")
        historico = self.cursor.fetchall()

        for tarefa in historico:
            self.atividade_list.insert(END, tarefa[0])
            
            

    def delete_all_atividades(self):
        """Apaga todas as tarefas e o histórico."""
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar todas as tarefas e o histórico?")
        if resposta:
            self.cursor.execute("DELETE FROM tarefas")
            self.cursor.execute("DELETE FROM historico")
            self.conn.commit()

            self.list_saved_atividades()  # Atualiza a lista de tarefas
            messagebox.showinfo("Sucesso", "Todas as tarefas foram apagadas com sucesso!")


if __name__ == "__main__":
    AdminTarefas()