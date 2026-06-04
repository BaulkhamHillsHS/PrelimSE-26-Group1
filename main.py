import customtkinter as ctk
from PIL import Image
import csv

ctk.set_appearance_mode('light')
ctk.set_default_color_theme("theme_nutflix.JSON")

logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_transparent.png")

class nutflixSignIn(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Streaming app")
        self.geometry("1080x720")
        self.resizable(True, True)

        self.build_ui()
    
    def build_ui(self):
        self.build_form_frame()
    
    def build_form_frame(self):
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(fill="both", expand=True, pady=200)

        self.frame_form.grid_columnconfigure((0), weight=1) 
        self.frame_form.grid_rowconfigure((0, 1, 2), weight=1)

        #Logo
        logo = ctk.CTkImage(light_image=logo_white, dark_image=logo_red, size=(30, 30))

        #Heading
        ctk.CTkLabel(self.frame_form, text="Sign In", font=("Arial", 40), text_color="#890000").grid(row=0, column=0, padx=10, pady=10)

        #Text Input
        self.entry_username = ctk.CTkEntry(self.frame_form, placeholder_text="Username", height=50, width=300)
        self.entry_username.grid(row=1, column=0, sticky="n")
        self.entry_password = ctk.CTkEntry(self.frame_form, placeholder_text="Password", height=50, width=300)
        self.entry_password.grid(row=2, column=0, sticky="n")

        #Submit Button
        ctk.CTkButton(self.frame_form, text="Sign In", command=self.sign_in).grid(row=3, column=0, sticky="n")
    
    def sign_in(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if self.validate_credentials(username, password):
            print("Sign in successful")

            #Show start menu frame
            self.controller.show_frame(nutflixStart)
        else:
            print("Sign in failed")

    def validate_credentials(self, username, password):
        try:
            with open("account_information.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        return True
            return False
        except FileNotFoundError:
            return False

class nutflixStart(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.build_ui()
    
    def build_ui(self):
        self.build_start_frame()
    
    def build_start_frame(self):
        self.frame_start = ctk.CTkFrame(self)
        self.frame_start.pack(fill="both", expand=True)

        self.frame_start.grid_columnconfigure((0, 1, 2), weight=1) 
        self.frame_start.grid_rowconfigure((0, 1, 2), weight=1)

        #Logo
        logo = ctk.CTkImage(light_image=logo_white, dark_image=logo_red, size=(30, 30))
        
        #Heading
        ctk.CTkLabel(self.frame_start, text="Who's Watching?", font=("Arial", 40), text_color="#890000").grid(row=0, column=1, padx=10, pady=10)

        #Menu
        self.frame_profile_menu = ctk.CTkFrame(master=self.frame_start)
        self.frame_profile_menu.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_profile_menu.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_profile_menu.grid_rowconfigure((0), weight=1)


        #Profile Buttons
        self.button_profile1 = ctk.CTkButton(self.frame_profile_menu, text="Profile 1", font=("Arial", 24), width=200, height=200)
        self.button_profile1.grid(row=0, column=0)

        self.button_profile2 = ctk.CTkButton(self.frame_profile_menu, text="Profile 2", font=("Arial", 24), width=200, height=200)
        self.button_profile2.grid(row=0, column=1)

        self.button_profile3 = ctk.CTkButton(self.frame_profile_menu, text="Profile 3", font=("Arial", 24), width=200, height=200)
        self.button_profile3.grid(row=0, column=2)

        self.button_profile_create = ctk.CTkButton(self.frame_profile_menu, text="Create Profile", font=("Arial", 24), width=200, height=200)
        self.button_profile_create.grid(row=0, column=3)

        #Edit Profiles Button
        self.button_edit_profile = ctk.CTkButton(self.frame_start, text="Edit Profiles", font=("Arial", 16), width=200, height=50)
        self.button_edit_profile.grid(row=2, column=1)

if __name__ == "__main__":
    app = nutflixApp()
    app.mainloop()