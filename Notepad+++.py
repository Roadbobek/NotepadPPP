import customtkinter as ctk
from tkinter import filedialog, messagebox

class Notepad(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Notepad+++")
        self.geometry("800x600")
        self.iconbitmap("images/notepadppp.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, wrap="none", font=("Comic Sans MS", 18))
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.bind("<KeyPress-BackSpace>", self.handle_backspace)
        self.textbox.bind("<KeyPress-Delete>", self.handle_delete)
        self.textbox.bind("<Control-x>", self.handle_cut_event)
        self.textbox.bind("<Control-X>", self.handle_cut_event)

        self.menu = ctk.CTkFrame(self, height=30)
        self.menu.grid(row=1, column=0, sticky="ew")

        self.file_menu = ctk.CTkOptionMenu(self.menu, width=96, height=28, values=["New", "Open", "Save", "Save As", "Exit"], command=self.file_menu_handler)
        self.file_menu.pack(side="left", padx=(10, 5), pady=6)
        self.file_menu.set("File")

        self.edit_menu = ctk.CTkOptionMenu(self.menu, width=96, height=28, values=["Cut", "Copy", "Paste"], command=self.edit_menu_handler)
        self.edit_menu.pack(side="left", padx=5, pady=6)
        self.edit_menu.set("Edit")

        self.footer_text = ctk.CTkLabel(self.menu, text="Notepad+++ made with love by Roadbobek <3")
        self.footer_text.pack(side="right", padx=32, pady=6)

        self.file_path = None

    def file_menu_handler(self, choice):
        if choice == "New":
            self.new_file()
        elif choice == "Open":
            self.open_file()
        elif choice == "Save":
            self.save_file()
        elif choice == "Save As":
            self.save_as_file()
        elif choice == "Exit":
            self.quit()
        self.file_menu.set("File")

    def edit_menu_handler(self, choice):
        if choice == "Cut":
            self.handle_cut()
        elif choice == "Copy":
            self.textbox.event_generate("<<Copy>>")
        elif choice == "Paste":
            self.textbox.event_generate("<<Paste>>")
        self.edit_menu.set("Edit")

    def handle_backspace(self, event):
        if self.textbox.tag_ranges("sel"):
            self.handle_selection_delete()
            return "break"

        char_to_delete_index = self.textbox.index("insert-1c")
        if self.textbox.index("insert") == "1.0":
            return "break"
        char_to_delete = self.textbox.get(char_to_delete_index)
        if char_to_delete == '\n':
            char_to_delete = 'newline'
        if messagebox.askyesno("Confirm Deletion", f"Are you really sure you want to delete '{char_to_delete}'???", default=messagebox.NO):
            self.textbox.delete(char_to_delete_index)
        return "break"

    def handle_delete(self, event):
        if self.textbox.tag_ranges("sel"):
            self.handle_selection_delete()
            return "break"

        char_to_delete_index = self.textbox.index("insert")
        if char_to_delete_index == self.textbox.index("end-1c"):
            return "break"
        char_to_delete = self.textbox.get(char_to_delete_index)
        if char_to_delete == '\n':
            char_to_delete = 'newline'
        if messagebox.askyesno("Confirm Deletion", f"Are you really sure you want to delete '{char_to_delete}'???", default=messagebox.NO):
            self.textbox.delete(char_to_delete_index)
        return "break"

    def handle_selection_delete(self):
        try:
            start, end = self.textbox.tag_ranges("sel")
            selected_text = self.textbox.get(start, end)
            for char in reversed(selected_text):
                char_disp = 'newline' if char == '\n' else char
                if not messagebox.askyesno("Confirm Deletion", f"Are you really sure you want to delete '{char_disp}'???", default=messagebox.NO):
                    return
            self.textbox.delete(start, end)
        except ValueError:
            pass

    def handle_cut_event(self, event):
        self.handle_cut()
        return "break"

    def handle_cut(self):
        try:
            start, end = self.textbox.tag_ranges("sel")
            selected_text = self.textbox.get(start, end)
            
            for char in reversed(selected_text):
                char_disp = 'newline' if char == '\n' else char
                if not messagebox.askyesno("Confirm Deletion", f"Are you really sure you want to cut '{char_disp}'???", default=messagebox.NO):
                    return

            self.clipboard_clear()
            self.clipboard_append(selected_text)
            self.textbox.delete(start, end)
        except ValueError:
            pass

    def new_file(self):
        self.textbox.delete("1.0", "end")
        self.file_path = None

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "r") as f:
                self.textbox.delete("1.0", "end")
                self.textbox.insert("1.0", f.read())
            self.file_path = path

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as f:
                f.write(self.textbox.get("1.0", "end"))
        else:
            self.save_as_file()

    def save_as_file(self):
        path = filedialog.asksaveasfilename()
        if path:
            with open(path, "w") as f:
                f.write(self.textbox.get("1.0", "end"))
            self.file_path = path

if __name__ == "__main__":
    app = Notepad()
    app.mainloop()
