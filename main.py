import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class streamApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Streaming app")
        self.geometry("1080x720")
        self.resizable(True, True)

        self._build_ui()
    
    def _build_ui(self):
        self._build_start_frame()
    
    def _build_start_frame(self):
        self.frame_start = ctk.CTkFrame(self)
        self.frame_start.pack(fill="both", expand=True)

        self.frame_start.grid_columnconfigure((0, 1, 2), weight=1) 
        self.frame_start.grid_rowconfigure((0, 1, 2), weight=1)

        #Heading
        ctk.CTkLabel(self.frame_start, text="Select a profile", font=("Arial", 24)).grid(row=0, column=1, padx=10, pady=10)

        #Menu
        self.frame_menu = ctk.CTkFrame(master=self.frame_start)
        self.frame_menu.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_menu.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_menu.grid_rowconfigure((0), weight=1)


        #Profile buttons
        self.button_profile1 = ctk.CTkButton(self.frame_menu, fg_color="#202020", hover_color="#626262", text="Profile 1", width=200, height=200)
        self.button_profile1.grid(column=0, row=0)

        self.button_profile2 = ctk.CTkButton(self.frame_menu, fg_color="#202020", hover_color="#626262", text="Profile 2", width=200, height=200)
        self.button_profile2.grid(column=1, row=0)

        self.button_profile3 = ctk.CTkButton(self.frame_menu, fg_color="#202020", hover_color="#626262", text="Profile 3", width=200, height=200)
        self.button_profile3.grid(column=2, row=0)
        

if __name__ == "__main__":
    app = streamApp()
    app.mainloop()