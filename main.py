# SISTEMA DE GERENCIAMENTO DE LEITURA

"""
Requisitos:
- cadastrar novo livro (create)
- ver lista de livros (read)
- editar livro cadastrado (update)
- remover livro cadastrado (delete)
"""

import time, os

PATH_REGISTER = "path_directory/registers.txt"

def render_register(item, id):
    reading_percent = (float(item["current_page"])/float(item["total_pages"]))*100
    reading_percent = round(reading_percent,2)

    pag = f"{item["current_page"]}/{item["total_pages"]}"
    print(f"\033[1;33mpag.{pag:<13}\033[0m" + f"[{id}]\033[1;1m {item["book_name"]:<40}\033[0m" + f"\033[1;92m{reading_percent}%\033[0m")

def show_message(message,codigo_ANSI_cor):
    # Verde é 32, Vermelho é 31, Amarelo é 33
    clear_screen()
    print(f"\033[1;{codigo_ANSI_cor}m{message}\033[0m")
    time.sleep(1)
    clear_screen()

def load_registers():
    book_list = []

    try:
        with open(PATH_REGISTER, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha_modificada = linha.rstrip('\n')
                n, p = linha_modificada.split('-')
                c_p , t_p = p.split()

                # Lê um registro do arquivo
                livro = {
                    "book_name": n,
                    "current_page" : c_p,
                    "total_pages" : t_p
                }
                # Salva o registro na lista
                book_list.append(livro)
        show_message("Loading...",33)
        return book_list
    except ValueError:
        show_message(f"Load error: {ValueError}",31)
        return []
    except FileNotFoundError:
        show_message(f"Not file: {FileNotFoundError}",31)
        return []

def create_book():
    print("\033[33mREGISTER A NEW BOOK\033[0m\n")
    try:
        # Solicita os dados do livro para registro
        book_name = input("Type the book name: ")
        while(True):
            current_page = input("Current page: ")
            total_pages = input("Total number of pages: ")

            if current_page == "" or total_pages == "" or book_name == "":
                return

            if int(current_page) < int(total_pages):
                break
            else:
                show_message("Try again!",93)
        with open(PATH_REGISTER, "a", encoding="utf-8") as arquivo:
            # Salva o registro no formato: nome, página atual, total de páginas
            arquivo.write(book_name + "-" + current_page + " " + total_pages + "\n")
        show_message("Register sucess!",32)
    except ValueError:
        show_message(f"Register error: {ValueError}",31)

def read_book():
    book_list = load_registers()
    id=1
    if book_list:
        for item in book_list:
            render_register(item,id)
            id+=1
        print("\n")
    else:
        print("Lista vazia!\n")
    return book_list

def update_book():
    while(True):
        book_list = read_book() # Mostra a lista de registros
        try:
            opcao = input("\n[\033[1;36mEdit\033[0m]: ")
            if opcao == "":
                return
            else:
                opcao = int(opcao)
            if opcao > len(book_list) or opcao <= 0:
                show_message("List limit exceeded",31)
            else:
                break
        except ValueError:
            show_message(f"Type number, please: {ValueError}",31)
    # Editar um registro e regravar todos
    clear_screen()
    render_register(book_list[opcao-1],opcao)
    
    new_book_name = input("Edit the book name: ")
    if new_book_name != "":
        book_list[opcao-1]["book_name"] = new_book_name
    # Validar edição da página atual
    while(True):
        try:
            new_current_page = input("Edit current page: ")
            if new_current_page == "":
                break
            if int(new_current_page) > int(book_list[opcao-1]["total_pages"]):
                show_message("Current page exceed total",31)
            else:
                book_list[opcao-1]["current_page"] = new_current_page
                break
        except ValueError:
            show_message(f"Type number, please: {ValueError}",31)
    # Validar edição no total de páginas
    while(True):
        try:
            new_total_pages = input("Edit total number of pages: ")
            if new_total_pages == "":
                break
            if int(new_total_pages) < int(book_list[opcao-1]["current_page"]):
                show_message("A small number of pages",31)
            else:
                book_list[opcao-1]["total_pages"] = new_total_pages
                break
        except ValueError:
            show_message(f"Type number, please: {ValueError}",31)
    # Regravar dados no arquivo
    try:
        with open(PATH_REGISTER, "w", encoding="utf-8") as arquivo:
            for item in book_list:
                arquivo.write(item["book_name"] + "-" + item["current_page"] + " " + item["total_pages"] + "\n")
        show_message("Edit sucess!",32)
    except OSError:
        show_message(f"Edit error: {OSError}",31)

def delete_book():
    while(True):
        book_list = read_book() # Mostra a lista de registros
        try:
            opcao = input("\n[\033[1;31mDelete\033[0m]: ")
            if opcao == "":
                return
            else:
                opcao = int(opcao)
            if opcao > len(book_list) or opcao <= 0:
                show_message("List limit exceeded",31)
            else:
                break
        except ValueError:
            show_message(f"Type number, please: {ValueError}",31)
    # Deletar um registro e regravar todos
    del book_list[opcao-1]
    try:
        with open(PATH_REGISTER, "w", encoding="utf-8") as arquivo:
            for item in book_list:
                arquivo.write(item["book_name"] + "-" + item["current_page"] + " " + item["total_pages"] + "\n")
        show_message("Delete sucess!",32)
    except OSError:
        show_message(f"Delete error: {OSError}",31)

def clear_screen():
    if os.name == 'nt':
        os.system('cls') # limpar a tela no Windows
    else:
        os.system('clear') # limpar a tela no Linux

clear_screen()

while(True):
    read_book()
    print("\033[1m1 - Register book\n\
2 - Edit list\n\
3 - \033[1;31mDelete item\033[0m")
    opcao = input("\n[\033[1;36mTask\033[0m]: ")
    clear_screen()
    match opcao:
        case '1':
            create_book()
        case '2':
            update_book()
        case '3':
            delete_book()
        case 'q':
            print("\033[1;32mClosing program...\033[0m")
            time.sleep(1)
            break
        case _:
            print("\033[1;31mInvalid decision\033[0m")
            time.sleep(1)
            clear_screen()