from tkinter import *
from tkinter import messagebox
import mysql.connector
import sys
import os
import json
import bcrypt
idusuario_logado = None
task_frame = None
invitation_frame = None

with open('database_credentials.json') as json_file:
    credentials = json.load(json_file)

# Obtém as credenciais do arquivo JSON
username = credentials['username']
password = credentials['password']

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
    database="lista"
)


def exit_app():
    window.destroy()


def back_to_main_screen():
    task_frame.destroy()
    show_main_screen()


def back_to_main_screen2():
    invitation_frame.destroy()
    show_main_screen()


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def add_list():
    list_name = entry_list_name.get()
    if list_name:
        global idusuario_logado
        user_id = idusuario_logado  # Obter o ID do usuário logado
        cursor = db.cursor()  # Cria o cursor
        query_last_list_id = "SELECT MAX(id) FROM lista_tarefas;"
        cursor.execute(query_last_list_id)
        result = cursor.fetchone()
        last_list_id = result[0]

        new_user_id = last_list_id + 1 if last_list_id else 1

        query = "INSERT INTO lista_tarefas (id,nome_lista, data_criacao, data_modificacao, id_usuario) VALUES (%s,%s, NOW(), NOW(), %s)"
        values = (new_user_id, list_name, user_id)
        cursor.execute(query, values)
        db.commit()
        show_popup("Sucesso! Lista de tarefas adicionada com sucesso.")
        entry_list_name.delete(0, "end")
        show_lists()
    else:
        show_popup("Aviso! Por favor, insira um nome para a lista de tarefas.")


def share_list():
    selected_list = listbox_lists.get(listbox_lists.curselection())

    if selected_list:
        share_window = Toplevel(window)
        share_window.title("Compartilhar Lista")
        center_window(share_window)

        share_frame = Frame(share_window, padx=20, pady=20)
        share_frame.pack()

        label = Label(share_frame, text="Usuário:")
        label.pack()

        user_entry = Entry(share_frame)
        user_entry.pack()

        def share():
            username = user_entry.get()

            if username:
                cursor = db.cursor(buffered=True)
                # Get the ID of the selected list
                query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
                values = (selected_list,)
                cursor.execute(query, values)
                list_id = cursor.fetchone()[0]

                # Get the ID of the user to share with
                query = "SELECT id FROM usuarios WHERE nome_usuario = %s"
                values = (username,)
                cursor.execute(query, values)
                user_id = cursor.fetchone()

                if user_id:
                    user_id = user_id[0]

                    # Check if the list is already shared with the user
                    query = "SELECT * FROM compartilha WHERE id_tarefa = %s AND id_dono = %s AND id_convidado = %s"
                    values = (list_id, idusuario_logado, user_id)
                    cursor.execute(query, values)
                    result = cursor.fetchone()

                    if result:
                        show_popup(
                            "A lista já está compartilhada com o usuário.")
                    else:
                        # Share the list with the user
                        query = "INSERT INTO compartilha (id_tarefa, id_dono, id_convidado) VALUES (%s, %s, %s)"
                        values = (list_id, idusuario_logado, user_id)
                        cursor.execute(query, values)
                        db.commit()
                        show_popup("Lista compartilhada com sucesso.")
                        share_window.destroy()
                else:
                    show_popup("Usuário não encontrado.")
            else:
                show_popup("Por favor, insira um nome de usuário.")

        share_button = Button(share_frame, text="Compartilhar", command=share)
        share_button.pack(pady=10)
    else:
        show_popup(
            "Aviso! Por favor, selecione uma lista de tarefas para compartilhar.")


def access_selected_list():
    selected_list = listbox_lists.get(listbox_lists.curselection())
    show_task_screen(selected_list)
    


def show_lists():
    global idusuario_logado
    user_id = idusuario_logado  # Obter o ID do usuário logado
    cursor = db.cursor()  # Cria o cursor
    query = "SELECT nome_lista FROM lista_tarefas WHERE id_usuario = %s"
    values = (user_id,)
    cursor.execute(query, values)
    lists = cursor.fetchall()

    # Get the task lists shared with the user
    query = """
            SELECT l.nome_lista
            FROM compartilha c
            INNER JOIN lista_tarefas l ON c.id_tarefa = l.id
            INNER JOIN usuarios u ON c.id_convidado = u.id
            WHERE u.id = %s
            """
    values = (idusuario_logado,)
    cursor.execute(query, values)
    shared_lists = cursor.fetchall()

    # Clear the listbox
    listbox_lists.delete(0, END)

    # Add the owned task lists to the listbox
    for list_name in lists:
        listbox_lists.insert(END, list_name[0])

    # Add the shared task lists to the listbox
    for list_name in shared_lists:
        listbox_lists.insert(END, list_name[0])


def remove_list():
    # Obtém o índice da lista selecionada
    selected_list = listbox_lists.curselection()

    if selected_list:
        # Obtém o nome da lista selecionada
        list_name = listbox_lists.get(selected_list)

        # Verifica se o usuário é o criador da lista
        cursor = db.cursor()
        query = "SELECT id_usuario FROM lista_tarefas WHERE nome_lista = %s"
        cursor.execute(query, (list_name,))
        results = cursor.fetchall()

        if (idusuario_logado,) in results:
            # O usuário é o criador da lista, pode realizar a exclusão

            # Exclui as tarefas relacionadas à lista
            query = "DELETE FROM tarefa WHERE id_lista IN (SELECT id FROM lista_tarefas WHERE nome_lista = %s)"
            cursor.execute(query, (list_name,))
            db.commit()

            # Exclui os registros relacionados na tabela compartilha
            query = "DELETE FROM compartilha WHERE id_tarefa IN (SELECT id FROM lista_tarefas WHERE nome_lista = %s)"
            cursor.execute(query, (list_name,))
            db.commit()

            # Exclui a lista de tarefas
            query = "DELETE FROM lista_tarefas WHERE nome_lista = %s AND id_usuario = %s"
            values = (list_name, idusuario_logado)
            cursor.execute(query, values)
            db.commit()

            show_popup("Sucesso! Lista de tarefas removida com sucesso.")
            show_lists()
        else:
            show_popup(
                "Aviso! Você não tem permissão para remover esta lista de tarefas.")
    else:
        show_popup(
            "Aviso! Por favor, selecione uma lista de tarefas para remover.")


def show_task_screen(list_name):
    def add_task():
        task_description = task_entry.get()

        if task_description:
            cursor = db.cursor(buffered=True)
            # Obtém o ID da lista com base no nome
            query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
            values = (list_name,)
            cursor.execute(query, values)
            list_id = cursor.fetchone()[0]

            query_last_tarefa_id = "SELECT MAX(id) FROM tarefa;"
            cursor.execute(query_last_tarefa_id)
            result = cursor.fetchone()
            last_tarefa_id = result[0]

            new_tarefa_id = last_tarefa_id + 1 if last_tarefa_id else 1

            query = "INSERT INTO tarefa (id,descricao, data_criacao, conclusao, id_lista) VALUES (%s,%s, NOW(), 0, %s)"
            values = (new_tarefa_id, task_description, list_id)
            cursor.execute(query, values)
            db.commit()

            task_entry.delete(0, "end")  # Limpa o campo de entrada de texto
            show_tasks()  # Atualiza a exibição das tarefas

    def remove_task():
        selected_task_index = task_listbox.curselection()

        if selected_task_index:
            selected_task = task_listbox.get(selected_task_index)
            cursor = db.cursor(buffered=True)
            # Obtém o ID da lista com base no nome
            query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
            values = (list_name,)
            cursor.execute(query, values)
            list_id = cursor.fetchone()[0]

            query = "DELETE FROM tarefa WHERE descricao = %s AND id_lista = %s"
            values = (selected_task, list_id)
            cursor.execute(query, values)
            db.commit()

            show_tasks()  # Atualiza a exibição das tarefas

    def edit_task():
        selected_task_index = task_listbox.curselection()

        if selected_task_index:
            selected_task = task_listbox.get(selected_task_index)
            new_task_description = task_entry.get()

            if new_task_description:
                cursor = db.cursor(buffered=True)
                # Obtém o ID da lista com base no nome
                query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
                values = (list_name,)
                cursor.execute(query, values)
                list_id = cursor.fetchone()[0]

                query = "UPDATE tarefa SET descricao = %s, conclusao = 0 WHERE descricao = %s AND id_lista = %s"
                values = (new_task_description, selected_task, list_id)
                cursor.execute(query, values)
                db.commit()

                # Limpa o campo de entrada de texto
                task_entry.delete(0, "end")
                show_tasks()  # Atualiza a exibição das tarefas

    def mark_task_as_completed():
        selected_task_index = task_listbox.curselection()

        if selected_task_index:
            selected_task = task_listbox.get(selected_task_index)
            cursor = db.cursor(buffered=True)
            # Obtém o ID da lista com base no nome
            query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
            values = (list_name,)
            cursor.execute(query, values)
            list_id = cursor.fetchone()[0]

            query = "UPDATE tarefa SET conclusao = 1 WHERE descricao = %s AND id_lista = %s"
            values = (selected_task, list_id)
            cursor.execute(query, values)
            db.commit()

            show_tasks()  # Atualiza a exibição das tarefas

    global task_frame, task_listbox
    # Oculta a tela principal
    main_frame.pack_forget()

    # Cria uma nova tela para exibir as tarefas
    task_frame = Frame(window, padx=20, pady=20)
    task_frame.pack()

    # Título da tela
    title_label = Label(task_frame, text=list_name, font=("Arial", 16))
    title_label.pack(pady=10)

    listbox_frame = Frame(task_frame)
    listbox_frame.pack()

    # Scrollbar para a lista de tarefas
    scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Listbox para exibir as tarefas
    task_listbox = Listbox(listbox_frame, width=50, height=10,
                           yscrollcommand=scrollbar.set)
    task_listbox.pack()

    # Configura a scrollbar para funcionar com a listbox
    scrollbar.config(command=task_listbox.yview)
    task_listbox.config(yscrollcommand=scrollbar.set)

    task_entry_frame = Frame(task_frame)
    task_entry_frame.pack(pady=5)

    task_entry = Entry(task_entry_frame, width=50)
    task_entry.pack()

    button_frame = Frame(task_frame)
    button_frame.pack(pady=20)

    # Botão de adicionar tarefa
    add_button = Button(
        button_frame, text="Adicionar Tarefa", command=add_task)
    add_button.pack(side="left", padx=10)
    # Botão de editar tarefa

    edit_button = Button(button_frame, text="Editar Tarefa", command=edit_task)
    edit_button.pack(side="left", padx=10)

    # Botão de remover tarefa
    remove_button = Button(
        button_frame, text="Remover Tarefa", command=remove_task)
    remove_button.pack(side="left", padx=10)

    # Botão de marcar tarefa como concluída
    mark_complete_button = Button(
        button_frame, text="Concluir Tarefa", command=mark_task_as_completed)
    mark_complete_button.pack(side="left", padx=10)

    back_button_frame = Frame(task_frame)
    back_button_frame.pack(pady=20)

    # Botão de voltar para a tela principal
    back_button = Button(back_button_frame, text="Voltar",
                         command=back_to_main_screen)
    back_button.pack(pady=10)
    # Função para exibir as tarefas da lista selecionada

    def show_tasks():
        # Limpa a listbox antes de exibir as tarefas
        task_listbox.delete(0, "end")
        cursor = db.cursor()
        # Obtém o ID da lista com base no nome
        query = "SELECT id FROM lista_tarefas WHERE nome_lista = %s"
        values = (list_name,)
        cursor.execute(query, values)
        list_id = cursor.fetchone()[0]

        #_ = cursor.fetchall()  # Limpa os resultados não lidos

        # Obtém as tarefas da lista selecionada
        query = "SELECT id, descricao, conclusao FROM tarefa WHERE id_lista = %s"
        values = (list_id,)
        cursor.execute(query, values)
        tasks = cursor.fetchall()

        # Adiciona as tarefas na listbox
        for task in tasks:
            task_id, task_description, task_completed = task
            task_listbox.insert("end", task_description)
            if task_completed:
                task_listbox.itemconfig(
                    "end", background="lightgreen", foreground="gray")
            else:
                task_listbox.itemconfig(
                    "end", background="white", foreground="black")

    # Chama a função para exibir as tarefas
    show_tasks()


def show_invitations_screen():
    global invitation_frame
    global main_frame
    global idusuario_logado

    # Hide the main screen
    main_frame.pack_forget()

    # Create a new screen to display invitations
    invitation_frame = Frame(window, padx=20, pady=20)
    invitation_frame.pack()

    # Title of the screen
    title_label = Label(
        invitation_frame, text="Invitations", font=("Arial", 16))
    title_label.pack(pady=10)

    listbox_frame = Frame(invitation_frame)
    listbox_frame.pack()

    # Scrollbar for the list of invitations
    scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Listbox to display the invitations
    invitation_listbox = Listbox(
        listbox_frame, width=50, height=10, yscrollcommand=scrollbar.set)
    invitation_listbox.pack()

    # Configure the scrollbar to work with the listbox
    scrollbar.config(command=invitation_listbox.yview)
    invitation_listbox.config(yscrollcommand=scrollbar.set)

    def show_invitations():
        # Clear the listbox before displaying invitations
        invitation_listbox.delete(0, "end")

        # Fetch and display the invitations for the current user
        cursor = db.cursor(buffered=True)
        query = "SELECT lista_tarefas.nome_lista, usuarios.nome FROM compartilha JOIN lista_tarefas ON compartilha.id_tarefa = lista_tarefas.id JOIN usuarios ON compartilha.id_dono = usuarios.id WHERE compartilha.id_convidado = %s AND compartilha.aceita IS NULL"
        values = (idusuario_logado,)
        cursor.execute(query, values)
        invitations = cursor.fetchall()

        # Add the invitations to the listbox
        for invitation in invitations:
            list_name, owner_name = invitation
            invitation_listbox.insert(
                "end", f"{list_name} (from: {owner_name})")

    # Call the function to display the invitations
    show_invitations()

    def accept_invitation():
        selected_invitation_index = invitation_listbox.curselection()

        if selected_invitation_index:
            selected_invitation = invitation_listbox.get(
                selected_invitation_index)

            # Extract the list name and owner name from the selected invitation
            list_name, owner_name = selected_invitation.split(" (from: ")
            list_name = list_name.strip()
            owner_name = owner_name[:-1]

            cursor = db.cursor(buffered=True)

            # Get the IDs of the list and owner
            query = "SELECT lista_tarefas.id, usuarios.id FROM lista_tarefas JOIN usuarios ON lista_tarefas.id_usuario = usuarios.id WHERE lista_tarefas.nome_lista = %s AND usuarios.nome = %s"
            values = (list_name, owner_name)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                list_id, owner_id = result

                # Update the invitation acceptance status
                query = "UPDATE compartilha SET aceita = true WHERE id_dono = %s AND id_convidado = %s AND id_tarefa = %s"
                values = (owner_id, idusuario_logado, list_id)
                cursor.execute(query, values)
                db.commit()

                show_popup("Convite aceito, Você aceitou o convite.")

                # Call the function to display the updated invitations
                show_invitations()
            else:
                show_popup("Erro, Falha ao recusar o convite.")

    def decline_invitation():
        selected_invitation_index = invitation_listbox.curselection()

        if selected_invitation_index:
            selected_invitation = invitation_listbox.get(
                selected_invitation_index)

            # Extract the list name and owner name from the selected invitation
            list_name, owner_name = selected_invitation.split(" (from: ")
            list_name = list_name.strip()
            owner_name = owner_name[:-1]

            cursor = db.cursor(buffered=True)

            # Get the IDs of the list and owner
            query = "SELECT lista_tarefas.id, usuarios.id FROM lista_tarefas JOIN usuarios ON lista_tarefas.id_usuario = usuarios.id WHERE lista_tarefas.nome_lista = %s AND usuarios.nome = %s"
            values = (list_name, owner_name)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                list_id, owner_id = result

                # Delete the invitation entry from the database
                query = "DELETE FROM compartilha WHERE id_dono = %s AND id_convidado = %s AND id_tarefa = %s"
                values = (owner_id, idusuario_logado, list_id)
                cursor.execute(query, values)
                db.commit()

                show_popup("Convite recusado, você recusou o convite.")

                # Call the function to display the updated invitations
                show_invitations()
            else:
                messagebox.showerror("Erro, Falha ao recusar o convite.")

    # Button to accept the invitation
    accept_button = Button(
        invitation_frame, text="Accept Invitation", command=accept_invitation)
    accept_button.pack(pady=5)

    # Button to decline the invitation
    decline_button = Button(
        invitation_frame, text="Decline Invitation", command=decline_invitation)
    decline_button.pack(pady=5)

    # Button to go back to the main screen
    back_button = Button(invitation_frame, text="Back",
                         command=back_to_main_screen2)
    back_button.pack(pady=10)


def show_main_screen():
    login_frame.pack_forget()
    register_frame.pack_forget()
    main_frame.pack()
    center_window(window)
    title_label.config(text="Lista")
    show_lists()


def show_login_screen():
    login_frame.pack()
    register_frame.pack_forget()
    center_window(window)


def show_popup(message):
    popup_window = Toplevel(window)
    popup_window.title("Mensagem")

    # Cria um rótulo com o texto da mensagem
    message_label = Label(popup_window, text=message)
    message_label.pack(pady=20)

    # Obtém as dimensões do texto da mensagem
    message_width = message_label.winfo_reqwidth()
    message_height = message_label.winfo_reqheight()

    # Calcula a posição x e y para centralizar o popup
    screen_width = popup_window.winfo_screenwidth()
    screen_height = popup_window.winfo_screenheight()
    popup_width = message_width + 20  # Adiciona um espaço extra
    # Adiciona espaço extra para outros elementos
    popup_height = message_height + 100
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2

    # Define o tamanho e a posição do popup
    popup_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    popup_window.resizable(False, False)

    # Botão de fechar
    close_button = Button(popup_window, text="Fechar",
                          command=popup_window.destroy)
    close_button.pack(pady=10)


def show_register_screen():
    login_frame.pack_forget()
    register_frame.pack()
    center_window(window)


def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        show_popup("Por favor, preencha todos os campos.")
        return
    
    # Cursor para executar as consultas SQL
    cursor = db.cursor()
    query = "SELECT senha FROM usuarios WHERE nome_usuario = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        hashed_password = hashed_password.encode('utf-8')
        password = password.encode('utf-8')
        # Verify the entered password against the stored hashed password
        if bcrypt.checkpw(password, hashed_password):
            show_popup("Login bem-sucedido!")
            global idusuario_logado
            idusuario_logado = username
            show_main_screen()
        else:
            show_popup("Credenciais inválidas!")
    else:
        show_popup("Credenciais inválidas!")

def logout():
    window.destroy()  # Fecha a janela principal
    # Reinicia a aplicação
    python = sys.executable
    os.execl(python, python, *sys.argv)


def register():
    username = register_username_entry.get()
    email = email_entry.get()
    password = register_password_entry.get()
    name = name_entry.get()
    phone = phone_entry.get()

    # Verifica se os campos estão vazios
    if not username or not name or not phone or not email or not password:
        show_popup("Por favor, preencha todos os campos.")
        return
    
    # encrypting passwd
    password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)

    # Cursor para executar as consultas SQL
    cursor = db.cursor()

    query_last_user_id = "SELECT MAX(id) FROM usuarios;"
    cursor.execute(query_last_user_id)
    result = cursor.fetchone()
    last_user_id = result[0]

    new_user_id = last_user_id + 1 if last_user_id else 1

    # Consulta para inserir um novo usuário com ID manual
    query_insert_user = """
        INSERT INTO usuarios (id, nome_usuario, nome, telefone, email, senha)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (new_user_id, username, name, phone, email, password)
    cursor.execute(query_insert_user, values)

    # Efetiva a transação no banco de dados
    db.commit()

    show_popup("Registro realizado!")


# Configuração da janela
window = Tk()
window.title("Login e Registro")

# Tamanho da janela
window_width = 800
window_height = 600

# Frame de login
login_frame = Frame(window)
login_frame.pack()

# Configura a geometria da janela
window.geometry(f"{window_width}x{window_height}")

# Label de título (login)
title_label = Label(login_frame, text="Bem-vindo!", font=("Arial", 16))
title_label.pack(pady=10)

# Espaço extra para barras de login
login_frame = Frame(window, padx=20, pady=20)

# Entradas de usuário e senha (login)
username_label = Label(login_frame, text="Usuário:")
username_label.pack()
username_entry = Entry(login_frame)
username_entry.pack()

password_label = Label(login_frame, text="Senha:")
password_label.pack()
password_entry = Entry(login_frame, show="*")
password_entry.pack()

button_framel = Frame(login_frame)
button_framel.pack(side="bottom", pady=10)

# Botões
login_button = Button(button_framel, text="Login", command=login)
login_button.pack(side='left', padx=10)
register_button = Button(button_framel, text="Registrar",
                         command=show_register_screen)
register_button.pack(side="left", padx=10)
exit_button = Button(button_framel, text="Sair", command=exit_app)
exit_button.pack(side="left", padx=10)

# Frame de registro
register_frame = Frame(window)
register_frame.pack_forget()

# Label de título (registro)
register_title_label = Label(
    register_frame, text="Registro", font=("Arial", 16))
register_title_label.pack(pady=10)

# Espaço extra para tela de registro
register_frame = Frame(window, padx=20, pady=20)

# Entradas de usuário, e-mail e senha (registro)
register_username_label = Label(register_frame, text="Usuário:")
register_username_label.pack()
register_username_entry = Entry(register_frame)
register_username_entry.pack()

name_label = Label(register_frame, text="Nome:")
name_label.pack()
name_entry = Entry(register_frame)
name_entry.pack()

phone_label = Label(register_frame, text="Telefone:")
phone_label.pack()
phone_entry = Entry(register_frame)
phone_entry.pack()


email_label = Label(register_frame, text="Email:")
email_label.pack()
email_entry = Entry(register_frame)
email_entry.pack()

register_password_label = Label(register_frame, text="Senha:")
register_password_label.pack()
register_password_entry = Entry(register_frame, show="*")
register_password_entry.pack()

# Botões de voltar e registrar (registro)
back_button = Button(register_frame, text="Voltar", command=show_login_screen)
back_button.pack(pady=5)

register_button = Button(register_frame, text="Registrar", command=register)
register_button.pack(pady=5)

# tela principal
main_frame = Frame(window, padx=20, pady=20)

lists_frame = Frame(main_frame)
lists_frame.pack(pady=10)
# Criação do scroll
scrollbar = Scrollbar(lists_frame)
scrollbar.pack(side="right", fill="y")

# Criação da listbox
listbox_lists = Listbox(
    lists_frame, yscrollcommand=scrollbar.set, height=10, width=50)
listbox_lists.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox_lists.yview)

# Criação do frame para os botões
buttons_framelist = Frame(main_frame)
buttons_framelist.pack(pady=10)
# Criação do Entry para inserir nome da lista
entry_list_name = Entry(buttons_framelist, width=50)
entry_list_name.pack()

# Botão para adicionar lista
add_list_button = Button(
    buttons_framelist, text="Adicionar Lista", command=add_list)
add_list_button.pack(side="left", padx=10)

# Botão de acesso à lista
access_button = Button(buttons_framelist, text="Acessar",
                       command=access_selected_list)
access_button.pack(side="left", padx=10)

share_button = Button(
    buttons_framelist, text="Compartilhar", command=share_list)
share_button.pack(side="left", padx=10)

# Botão para remover lista
remove_list_button = Button(
    buttons_framelist, text="Remover Lista", command=remove_list)
remove_list_button.pack(side="left", padx=10)

# Criação do frame para os botões
button_frame = Frame(main_frame)
button_frame.pack(pady=10)

logout_button = Button(button_frame, text="Deslogar", command=logout)
logout_button.pack(side="left", padx=10)
exit_button = Button(button_frame, text="Sair", command=exit_app)
exit_button.pack(side="left", padx=10)

invitation_frame = Frame(main_frame)
invitation_frame.pack(side="bottom", pady=10)

invitation_button = Button(
    invitation_frame, text="Convites", command=show_invitations_screen)
invitation_button.pack(pady=5)

# Label de mensagem
message_label = Label(window, text="")
message_label.pack()

# Exibir tela de login inicialmente
show_login_screen()

# Centraliza a janela principal
center_window(window)

# Loop principal da janela
window.mainloop()
