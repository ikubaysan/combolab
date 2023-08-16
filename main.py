import pygame
import tkinter as tk
from ButtonCheckWindow import ButtonCheckWindow

pygame.init()

class ComboLabApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Controller List")

        self.joystick_count = pygame.joystick.get_count()
        self.listbox = tk.Listbox(self.root, width=50)

        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.listbox.insert(tk.END, joystick.get_name())

        self.listbox.pack(pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.on_controller_select)

        # Add "Button Check" and "Next" buttons, but disable them initially
        self.btn_check = tk.Button(self.root, text="Button Check", command=self.launch_button_check_window,
                                   state=tk.DISABLED)
        self.btn_check.pack(pady=10)

        self.btn_next = tk.Button(self.root, text="Begin Training", command=self.launch_emulation_window, state=tk.DISABLED)
        self.btn_next.pack(pady=10)

    def on_controller_select(self, evt):
        # Enable the buttons when a controller is selected
        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.NORMAL)
        self.selected_controller = self.listbox.curselection()[0]

    def launch_button_check_window(self):
        self.btn_check.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        ButtonCheckWindow(self.selected_controller, self.enable_buttons)

    def launch_emulation_window(self):
        self.btn_check.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        TrainingWindow(self.selected_controller, self.enable_buttons)

    def enable_buttons(self):
        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.NORMAL)

class TrainingWindow:

    def __init__(self, controller_index, enable_buttons_callback):
        self.controller_index = controller_index
        self.joystick = pygame.joystick.Joystick(controller_index)
        self.joystick.init()

        self.window = tk.Toplevel()
        self.window.title("Training Window")

        self.controller_status_label = tk.Label(self.window, text=f"Selected Controller: {self.joystick.get_name()}")
        self.controller_status_label.pack()

        self.controller_connection_label = tk.Label(self.window, text="Controller Connection Status:")
        self.controller_connection_label.pack()

        self.connection_status_label = tk.Label(self.window, text="", fg="green")
        self.connection_status_label.pack()

        self.window.after(100, self.update_connection_status)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.enable_buttons_callback = enable_buttons_callback

    def update_connection_status(self):
        pygame.joystick.quit()
        pygame.joystick.init()

        new_joystick_count = pygame.joystick.get_count()

        if new_joystick_count == 0 or not pygame.joystick.Joystick(self.controller_index).get_init():
            self.connection_status_label.config(text="Disconnected", fg="red")
        else:
            self.connection_status_label.config(text="Connected", fg="green")

        self.window.after(1000, self.update_connection_status)

    def close_window(self):
        self.enable_buttons_callback()
        self.window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ComboLabApp(root)
    root.mainloop()
