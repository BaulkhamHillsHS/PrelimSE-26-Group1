import customtkinter as ctk
from PIL import Image
import csv

ctk.set_appearance_mode('light')
ctk.set_default_color_theme("theme_nutflix.JSON")

logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_transparent.png")

class nutflixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Streaming app")
        self.geometry("1080x720")
        self.resizable(True, True)

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Create frame instances and store them
        for f in (nutflixSignIn, nutflixStart, nutflixCreateProfile):
            frame = f(self.container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the sign in frame first
        self.show_frame(nutflixSignIn)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def set_user_email(self, email): # Setter function to set the email of current user, used for identification
        self.current_user_email = email
    
    def get_user_email(self): # Getter function to receive the email of the current user for identification
        return self.current_user_email

class nutflixSignIn(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()
    
    def build_ui(self):
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(fill="both", expand=True, pady=200)

        self.frame_form.grid_columnconfigure((0), weight=1) 
        self.frame_form.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Logo
        logo = ctk.CTkImage(light_image=logo_white, dark_image=logo_red, size=(30, 30))

        # Heading
        ctk.CTkLabel(self.frame_form, text="Sign In", font=("Arial", 40), text_color="#890000").grid(row=0, column=0, padx=10, pady=10)

        # Text Input
        self.entry_username = ctk.CTkEntry(self.frame_form, placeholder_text="Username", height=50, width=300)
        self.entry_username.grid(row=1, column=0, sticky="n")
        self.entry_password = ctk.CTkEntry(self.frame_form, placeholder_text="Password", height=50, width=300)
        self.entry_password.grid(row=2, column=0, sticky="n")

        # Submit Button
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
                        self.controller.set_user_email(row[2]) # Stores the email of the current user
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

        self.button_profile_create = ctk.CTkButton(self.frame_profile_menu, text="Create Profile", command=lambda: self.controller.show_frame(nutflixCreateProfile), font=("Arial", 24), width=200, height=200)
        self.button_profile_create.grid(row=0, column=3)

        #Edit Profiles Buttons
        self.button_edit_profile = ctk.CTkButton(self.frame_start, text="Edit Profiles", font=("Arial", 16), width=200, height=50)
        self.button_edit_profile.grid(row=2, column=1)

class nutflixCreateProfile(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()
    
    def build_ui(self):
        self.frame_start = ctk.CTkFrame(self)
        self.frame_start.pack(fill="both", expand=True)
        
        self.frame_start.grid_columnconfigure((0), weight=1) 
        self.frame_start.grid_rowconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.frame_start, text="Create Account", font=("Arial", 40), text_color="#890000").grid(row=0, column=0, padx=10, pady=10)
        
        self.profile_name = ctk.CTkEntry(self.frame_start, placeholder_text="Profile Name", height=50, width=300)
        self.profile_name.grid(row=1, column=0, pady=10)
        
        self.age_rating = ctk.CTkOptionMenu(self.frame_start, values=["G", "PG", "M", "MA15+", "R18+"], height=50, width=300)
        self.age_rating.grid(row=2, column=0, pady=10)
        
        ctk.CTkButton(self.frame_start, text="Create Profile", command=self.add_profile).grid(row=3, column=0, sticky="n")
    
    def add_profile(self):
        profile_name = self.profile_name.get()
        profile_age_rating = self.age_rating.get()
        account_email = self.controller.get_user_email()

        profile = [account_email, profile_name, profile_age_rating] # Email is a global value

        with open("profile_information.csv", "r") as file: # Csv containing profile information
            reader = csv.reader(file)
            for row in reader:
                if (row[0], row[1]) == (account_email, profile_name):
                    return # Profile with same name under same email already exists

        with open("profile_information.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(profile) # Adds profile to csv
            
        self.controller.show_frame(nutflixStart) # Takes user back to the start page
 

if __name__ == "__main__":
    app = nutflixApp()
    app.mainloop()