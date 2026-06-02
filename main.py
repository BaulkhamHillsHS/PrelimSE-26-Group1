import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('green')

logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_white.png")

class nutflixApp(ctk.CTk):

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

        #Logo
        logo = ctk.CTkImage(light_image=logo_white, dark_image=logo_red, size=(30, 30))
        
        #Heading
        ctk.CTkLabel(self.frame_start, text="Who's Watching?", font=("Arial", 30), text_color="#000000", image=logo).grid(row=0, column=1, padx=10, pady=10)

        #Menu
        self.frame_profile_menu = ctk.CTkFrame(master=self.frame_start)
        self.frame_profile_menu.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_profile_menu.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_profile_menu.grid_rowconfigure((0), weight=1)


        #Profile Buttons
        self.button_profile1 = ctk.CTkButton(self.frame_profile_menu, fg_color="#919191", hover_color="#626262", text="Profile 1", font=("Arial", 24), width=200, height=200)
        self.button_profile1.grid(row=0, column=0)

        self.button_profile2 = ctk.CTkButton(self.frame_profile_menu, fg_color="#919191", hover_color="#626262", text="Profile 2", font=("Arial", 24), width=200, height=200)
        self.button_profile2.grid(row=0, column=1)

        self.button_profile3 = ctk.CTkButton(self.frame_profile_menu, fg_color="#919191", hover_color="#626262", text="Profile 3", font=("Arial", 24), width=200, height=200)
        self.button_profile3.grid(row=0, column=2)

        self.button_profile_create = ctk.CTkButton(self.frame_profile_menu, fg_color="#6D6D6D", hover_color="#626262", text="Create Profile", font=("Arial", 24), width=200, height=200)
        self.button_profile_create.grid(row=0, column=3)

        #Edit Profiles Button
        self.button_edit_profile = ctk.CTkButton(self.frame_start, fg_color="#C6C6C6", hover_color="#626262", text="Edit Profiles", font=("Arial", 16), width=200, height=50)
        self.button_edit_profile.grid(row=2, column=1)

if __name__ == "__main__":
    app = nutflixApp()
    app.mainloop()