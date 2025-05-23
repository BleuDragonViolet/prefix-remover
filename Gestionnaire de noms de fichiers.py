import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def rename_files():
    folder_path = folder_path_var.get()
    prefix = prefix_var.get()
    remove_everywhere = remove_everywhere_var.get()
    include_subfolders = include_subfolders_var.get()
    case_insensitive = case_insensitive_var.get()
    
    if not folder_path:
        messagebox.showerror("Erreur", "Veuillez sélectionner un dossier")
        return
    if not prefix:
        messagebox.showerror("Erreur", "Veuillez entrer un préfixe à supprimer")
        return
    
    try:
        for root_dir, _, files in os.walk(folder_path):
            if not include_subfolders and root_dir != folder_path:
                continue
            
            for filename in files:
                new_name = filename
                
                if case_insensitive:
                    prefix_pattern = re.compile(re.escape(prefix), re.IGNORECASE)
                    if remove_everywhere:
                        new_name = prefix_pattern.sub("", new_name)
                    else:
                        if prefix_pattern.match(new_name):
                            new_name = prefix_pattern.sub("", new_name, count=1)
                else:
                    if remove_everywhere:
                        new_name = new_name.replace(prefix, "")
                    else:
                        if new_name.startswith(prefix):
                            new_name = new_name[len(prefix):]
                
                old_path = os.path.join(root_dir, filename)
                new_path = os.path.join(root_dir, new_name)
                
                if old_path != new_path:
                    os.rename(old_path, new_path)
        
        messagebox.showinfo("Succès", "Les fichiers ont été renommés avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)

# Interface Tkinter avec un design fluide et un thème "bleu crépuscule foncé"
root = tk.Tk()
root.title("Renommage de fichiers")
root.geometry("500x350")
root.configure(bg="#072747")

style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 11), padding=3, background="#0A3D62")
style.map("Custom.TButton", 
          background=[("active", "#1B4F72"), ("!disabled", "#0A3D62")])
style.configure("TLabel", font=("Arial", 11), background="#072747", foreground="white")
style.configure("TCheckbutton", background="#072747", foreground="white")
style.configure("TEntry", font=("Arial", 11), padding=5)

folder_path_var = tk.StringVar()
prefix_var = tk.StringVar()
remove_everywhere_var = tk.BooleanVar()
include_subfolders_var = tk.BooleanVar()
case_insensitive_var = tk.BooleanVar()

frame = tk.Frame(root, bg="#072747")
frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Dossier :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(frame, textvariable=folder_path_var, width=40).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame, text="📁", command=select_folder, style="Custom.TButton", width=3).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(frame, text="Préfixe à supprimer :").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(frame, textvariable=prefix_var, width=40).grid(row=1, column=1, padx=5, pady=5, columnspan=2)

ttk.Checkbutton(frame, text="Supprimer le préfixe partout", variable=remove_everywhere_var).grid(row=2, column=1, pady=5, sticky="w")
ttk.Checkbutton(frame, text="Inclure les sous-dossiers", variable=include_subfolders_var).grid(row=3, column=1, pady=5, sticky="w")
ttk.Checkbutton(frame, text="Ignorer la casse (Maj/Min)", variable=case_insensitive_var).grid(row=4, column=1, pady=5, sticky="w")

ttk.Button(root, text="Renommer", command=rename_files, style="Custom.TButton").pack(pady=15)

root.mainloop()



