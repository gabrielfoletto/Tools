import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import font as tkfont

# Função para selecionar a pasta de destino usando uma caixa de diálogo
def select_destination_folder():
    destination_folder = filedialog.askdirectory()
    destination_folder_entry.delete(0, tk.END)
    destination_folder_entry.insert(0, destination_folder)
    
# Função para selecionar a pasta de origem usando uma caixa de diálogo
def select_folder():
    source_folder = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, source_folder)

# Função para iniciar o processamento
def start_processing():
    destination_folder = destination_folder_entry.get()
    source_folder = source_folder_entry.get()

    if not os.path.isdir(destination_folder):
        print("Error.")
        return
    
    processed_folders = set()

    execution_folder = destination_folder
    os.makedirs(execution_folder, exist_ok=True)

    existing_files = [
        file for file in os.listdir(execution_folder)
        if file.endswith('.json') and file[:-5].isdigit()
    ]
    last_index = max([int(file[:-5]) for file in existing_files], default=0)
    folders = [
        folder for folder in os.listdir(source_folder)
        if os.path.isdir(os.path.join(source_folder, folder))
    ]

    new_folders = [folder for folder in folders if folder not in processed_folders]
    for folder_name in new_folders:
        if folder_name == 'latest':
            continue

        report_folder = os.path.join(source_folder, folder_name, "reports")
        if not os.path.exists(report_folder):
            continue

        for file_name in os.listdir(report_folder):
            if file_name.endswith('.json'):
                last_index += 1
                new_file = f"{last_index}.json"

                shutil.copy(
                    os.path.join(report_folder, file_name),
                    os.path.join(execution_folder, new_file)
                )

        processed_folders.add(folder_name)

# Cria a janela principal
window = tk.Tk()
style = ttk.Style()
style.theme_use('alt')
style.configure('Custom.TButton', background='black', foreground='white')
window.title("Extract JSON files")
window.geometry("400x260")
window.configure(bg='#363636')
pfont = tkfont.Font(size=9)
l_border = tk.Frame(window, bg='#1C1C1C', width=35)
l_border.pack(side='left', fill='y')
r_border = tk.Frame(window, bg='#1C1C1C', width=35)
r_border.pack(side='right', fill='y')
txt= tk.Label(window, text="The program will get all JSONs files\n from every execution available", font=pfont, fg='white', bg='#363636')
txt.pack()

# Campo de entrada para o nome da pasta
source_folder_label = ttk.Label(window, text="JSON Folder:")
source_folder_label.pack(pady=2)
source_folder_entry = ttk.Entry(window)
source_folder_entry.pack()
select_folder_button = ttk.Button(window, text="Select", command=select_folder, width=5.5,style='Custom.TButton')
select_folder_button.pack(pady=2)

# Campo de entrada para a pasta de destino
destination_folder_label = ttk.Label(window, text="Send to:")
destination_folder_label.pack()
destination_folder_entry = ttk.Entry(window)
destination_folder_entry.pack(pady=2)

# Botão para selecionar a pasta de destino
select_destination_folder_button = ttk.Button(window, text="Select", command=select_destination_folder,width=5.5, style='Custom.TButton')
select_destination_folder_button.pack()

# Botão para iniciar o processamento
start_button = ttk.Button(window, text="Start", command=start_processing,width=4, style='Custom.TButton')
start_button.pack(pady=2)

txt= tk.Label(window, text='Warning: The JSON files generated by cuckoo usually\nstay in ~/.cuckoo/storage/analysis/', font=pfont, fg='white', bg='#363636')
txt.pack()
# Executa a janela principal
window.mainloop()