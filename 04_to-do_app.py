import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, timedelta
import json
import os

class Task:
    def __init__(self, text, done=False, due_date=None):
        self.text = text
        self.done = done
        self.due_date = due_date

    def to_dict(self):
        return {"text": self.text, "done": self.done, "due_date": self.due_date}

    @staticmethod
    def from_dict(data):
        return Task(data["text"], data["done"], data.get("due_date"))

class TaskManager:
    def __init__(self, filepath="tasks.json"):
        self.filepath = filepath
        self.tasks = []
        self.original_order = []

    def add_task(self, task):
        self.tasks.append(task)
        self.original_order.append(task)

    def delete_tasks(self, indices):
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self.tasks):
                # Also remove from original_order
                task_to_remove = self.tasks[index]
                self.tasks.pop(index)
                if task_to_remove in self.original_order:
                    self.original_order.remove(task_to_remove)

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
                self.original_order = self.tasks.copy()

    def sort_tasks(self, method="entry"):
        if method == "alphabet":
            self.tasks.sort(key=lambda t: t.text.lower())
        elif method == "length":
            self.tasks.sort(key=lambda t: len(t.text))
        elif method == "due_date":
            self.tasks.sort(key=lambda t: (t.due_date or "9999-12-31"))
        elif method == "entry":
            # Restore original order for existing tasks only
            filtered_order = [t for t in self.original_order if t in self.tasks]
            self.tasks = filtered_order.copy()

class ToDoApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("To-Do List App")
        self.geometry("500x600")
        self.minsize(350, 450)

        self.task_manager = TaskManager()
        self.task_manager.load()
        self.selected_vars = []

        self._create_menu()
        self._create_widgets()
        self._render_tasks()
        self.after(1000 * 60, self._check_reminders)

    def _create_menu(self):
        menubar = tk.Menu(self)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: self._change_theme("flatly"))
        theme_menu.add_command(label="Dark Theme", command=lambda: self._change_theme("darkly"))
        theme_menu.add_command(label="Solar Theme", command=lambda: self._change_theme("solar"))
        menubar.add_cascade(label="Themes", menu=theme_menu)
        self.config(menu=menubar)

    def _change_theme(self, name):
        self.style.theme_use(name)

    def _create_widgets(self):
        self.main_frame = tb.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        entry_frame = tb.Frame(self.main_frame)
        entry_frame.pack(fill=X, pady=(0, 10))

        self.entry = tb.Entry(entry_frame)
        self.entry.pack(side=LEFT, fill=X, expand=YES)
        self.entry.bind("<Return>", lambda e: self._add_task())

        self.add_btn = tb.Button(entry_frame, text="Add Task", command=self._add_task)
        self.add_btn.pack(side=LEFT, padx=(10, 0))

        self.task_list_container = tb.Frame(self.main_frame)
        self.task_list_container.pack(fill=BOTH, expand=YES)

        self.canvas = tb.Canvas(self.task_list_container, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.scrollbar = tb.Scrollbar(self.task_list_container, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.task_list_frame = tb.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw")
        self.task_list_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        control_frame = tb.Frame(self.main_frame)
        control_frame.pack(fill=X, pady=(10, 0))

        # Sort dropdown
        tb.Label(control_frame, text="Sort by:").pack(side=LEFT, padx=(0,5))

        self.sort_var = tk.StringVar(value="entry")
        sort_options = ["entry", "alphabet", "length", "due_date"]
        sort_labels = {
            "entry": "Entry Order",
            "alphabet": "Alphabet",
            "length": "Length",
            "due_date": "Due Date"
        }
        self.sort_dropdown = tb.OptionMenu(control_frame, self.sort_var,
                                          *sort_options,
                                          command=self._on_sort_change,
                                          style="info")
        # Show user friendly names in dropdown
        menu = self.sort_dropdown["menu"]
        menu.delete(0, "end")
        for key in sort_options:
            menu.add_command(label=sort_labels[key],
                             command=lambda v=key: self.sort_var.set(v) or self._on_sort_change(v))

        self.sort_dropdown.pack(side=LEFT, padx=(0,10))

        self.delete_btn = tb.Button(control_frame, text="Delete Selected", bootstyle="danger", command=self._delete_selected)
        self.delete_btn.pack(side=LEFT, expand=YES, fill=X, padx=5)

    def _add_task(self):
        initial_text = self.entry.get().strip()

        def on_submit():
            text = text_entry.get().strip()
            if not text:
                messagebox.showerror("Error", "Task cannot be empty.")
                return

            selected_date = date_picker.entry.get().strip()
            due_date = selected_date if selected_date else None
            popup.destroy()

            self.task_manager.add_task(Task(text, due_date=due_date))
            self.task_manager.save()
            self._render_tasks()
            self.entry.delete(0, END)  # Clear main entry

        popup = tb.Toplevel(self)
        popup.title("New Task")
        popup.geometry("300x160")
        popup.resizable(False, False)
        popup.grab_set()

        frame = tb.Frame(popup, padding=10)
        frame.pack(fill=BOTH, expand=YES)

        tb.Label(frame, text="Task:").pack(anchor="w")
        text_entry = tb.Entry(frame)
        text_entry.pack(fill=X, pady=5)
        text_entry.insert(0, initial_text)
        text_entry.focus()

        tb.Label(frame, text="Due date (optional):").pack(anchor="w")
        date_picker = tb.DateEntry(frame, bootstyle="info", width=20)
        date_picker.pack(fill=X, pady=5)

        tb.Button(frame, text="Add", bootstyle="success", command=on_submit).pack(pady=5)

    def _render_tasks(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        self.selected_vars.clear()

        for idx, task in enumerate(self.task_manager.tasks):
            var = tb.BooleanVar(value=task.done)
            task_text = task.text
            if task.due_date:
                task_text += f" (Due: {task.due_date})"

            cb = tb.Checkbutton(
                self.task_list_frame,
                text=task_text,
                bootstyle="success-round-toggle" if task.done else "secondary-round-toggle",
                variable=var,
                command=lambda i=idx, v=var: self._toggle_done(i, v.get())
            )
            cb.pack(anchor="w", pady=2, padx=5)
            cb.bind("<Double-1>", lambda e, i=idx: self._edit_task(i))
            self.selected_vars.append(var)

    def _toggle_done(self, index, done):
        self.task_manager.tasks[index].done = done
        self.task_manager.save()
        self._render_tasks()

    def _delete_selected(self):
        indices_to_delete = [i for i, var in enumerate(self.selected_vars) if var.get()]
        if not indices_to_delete:
            return
        self.task_manager.delete_tasks(indices_to_delete)
        self.task_manager.save()
        self._render_tasks()

    def _on_sort_change(self, selection):
        self.task_manager.sort_tasks(selection)
        self._render_tasks()

    def _edit_task(self, index):
        task = self.task_manager.tasks[index]
        new_text = simpledialog.askstring("Edit Task", "Update task text:", initialvalue=task.text)
        if new_text:
            task.text = new_text
            self.task_manager.save()
            self._render_tasks()

    def _check_reminders(self):
        today = datetime.today().date()
        due_soon = []

        for task in self.task_manager.tasks:
            if task.due_date and not task.done:
                try:
                    due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    if today <= due_date <= today + timedelta(days=1):
                        due_soon.append(task.text + f" (Due: {task.due_date})")
                except Exception:
                    continue

        if due_soon:
            messagebox.showinfo("Reminder", "Tasks due soon:\n" + "\n".join(due_soon))

        self.after(1000 * 60 * 60, self._check_reminders)

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
