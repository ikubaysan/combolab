import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext
import pygame


class ButtonCheckWindow:

    def __init__(self, controller_index, enable_buttons_callback):
        self.controller_index = controller_index
        self.joystick = pygame.joystick.Joystick(controller_index)
        self.joystick.init()

        self.window = tk.Toplevel()
        self.window.title(self.joystick.get_name())

        # Create buttons for each joystick button horizontally
        self.button_frame = tk.Frame(self.window)
        self.buttons = [tk.Button(self.button_frame, text=str(i)) for i in range(self.joystick.get_numbuttons())]
        for i, btn in enumerate(self.buttons):
            btn.grid(row=0, column=i)
        self.button_frame.pack()

        # We care only about axes 4 and 5 since they represent the Z-axis.
        # Thus, we create buttons only for these axes.
        self.axes = [tk.Button(self.window, text=f"Axis {i}") for i in [4, 5]]
        for axis_btn in self.axes:
            axis_btn.pack()

        # Hat representation
        self.hat_value = tk.StringVar(value="(0, 0)")
        hat_label = tk.Label(self.window, text="Hat:")
        hat_display = tk.Label(self.window, textvariable=self.hat_value)
        hat_label.pack()
        hat_display.pack()

        self.console = scrolledtext.ScrolledText(self.window, width=40, height=10)
        self.console.pack(pady=20)

        self.window.after(100, self.update_controller_status)

        self.enable_buttons_callback = enable_buttons_callback
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.enable_buttons_callback()
        self.window.destroy()

    def update_controller_status(self):
        pygame.event.pump()
        current_time = datetime.now().strftime('%H:%M:%S:%f')[:-3]

        # Handle buttons
        for i, btn in enumerate(self.buttons):
            if self.joystick.get_button(i):
                btn.config(bg='red')
                message = f"{current_time} - Button {i} Pressed\n"
                self.console.insert(tk.END, message)
                self.console.yview(tk.END)
            else:
                btn.config(bg='gray')

        # Handle Z-axis (axes 4 and 5)
        for i in [4, 5]:
            axis_value = self.joystick.get_axis(i)
            axis_btn = self.axes[i - 4]  # since we only have buttons for axes 4 and 5
            if axis_value < 0:  # If the axis is near 0, treat it as not pressed
                axis_btn.config(bg='gray')
            else:
                axis_btn.config(bg='red')
                message = f"{current_time} - Axis {i} Positive Pressed\n"
                self.console.insert(tk.END, message)
                self.console.yview(tk.END)

        # Handle hat
        hat_x, hat_y = self.joystick.get_hat(0)
        self.hat_value.set(f"({hat_x}, {hat_y})")
        if hat_x != 0 or hat_y != 0:
            message = f"{current_time} - Hat: {hat_x}, {hat_y}\n"
            self.console.insert(tk.END, message)
            self.console.yview(tk.END)

        # Continue checking
        self.window.after(100, self.update_controller_status)
