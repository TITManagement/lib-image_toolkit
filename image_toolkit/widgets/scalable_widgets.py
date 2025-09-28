import customtkinter as ctk

class ScalableLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

class StyledButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
