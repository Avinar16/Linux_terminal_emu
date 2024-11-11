import tkinter as tk
from tkinter import simpledialog
from shell import Shell


class ShellGUI(tk.Frame):
    def __init__(self, master=None, shell=None):
        super().__init__(master)
        self.master = master
        self.shell = Shell('vfs.zip')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.cmd_entry = tk.Entry(self)
        self.cmd_entry.pack(side="top", fill=tk.X)

        self.run_btn = tk.Button(self)
        self.run_btn["text"] = "Run Command"
        self.run_btn["command"] = self.run_command
        self.run_btn.pack(side="top")

        self.output = tk.Text(self)
        self.output.pack(side="top")

    def run_command(self):
        cmd_line = self.cmd_entry.get()
        args = cmd_line.split()
        command = args[0]
        if command == "ls":
            listing = "\n".join(self.shell.ls())
            self.output.insert(tk.END, listing + "\n" if listing else "Empty directory\n")
        elif command == "cd" and len(args) > 1:
            self.shell.cd(args[1])
            self.output.insert(tk.END, f"Changed directory to {args[1]}\n")
        elif command == "rm" and len(args) > 1:
            self.shell.rm(args[1])
            self.output.insert(tk.END, f"Removed {args[1]}\n")
        elif command == "cp" and len(args) > 2:
            self.shell.cp(args[1], args[2])
            self.output.insert(tk.END, f"Copied {args[1]} to {args[2]}\n")
        self.cmd_entry.delete(0, tk.END)


root = tk.Tk()
app = ShellGUI(master=root)
app.mainloop()
