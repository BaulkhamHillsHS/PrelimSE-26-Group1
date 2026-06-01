import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class streamApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Streaming app")
        self.geometry("720x1080")
        self.resizable(True, True)

        self._build_ui()
    
    def _build_ui(self):
        self._build_start_frame()
    
    def _build_start_frame(self):
        self.frame_start = ctk.CTkFrame(self)

if __name__ == "__main__":
    app = streamApp()
    app.mainloop()