import customtkinter as ctk
from PIL import Image, ImageEnhance
import csv

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme_nutflix.JSON")

logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_transparent.png")

class medium:
        def __init__(self, type):
            self.type = type

class genre(medium): # Inherits type (move or tv show) from medium()
    def __init__(self, genre1, genre2, type):
        super().__init__(type)
        self.genre1 = genre1
        self.genre2 = genre2

class media(genre): # Inherits genres from genre(), called in get_media()
    def __init__(self, name, type, genre1, genre2, age_rating, image):
        super().__init__(genre1, genre2, type)
        self.name = name
        self.age_rating = age_rating
        self.image = Image.open(image)
    
    def get_image(self): # Getter function for the widget to collect the image file
        return self.image

def get_media():
        list = []
        with open("watch_information.csv", "r") as file: # Open watch_information.csv and collect each movie/show
            reader = csv.reader(file)
            for row in reader:
                m = media(row[0], row[1], row[2], row[3], row[4], row[5]) # name, type, genre1, genre2, age_rating, image
                list.append(m) # Add movie/tv show to list
        return list

media_list = get_media() # Preload all media

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
        for f in (nutflixSignIn, nutflixStart, nutflixCreateProfile, nutflixBrowse):
            frame = f(self.container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the sign in frame first
        self.show_frame(nutflixBrowse)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def set_user_information(self, username, password, email, full_name, plan, profile_count): # Setter function to set the account information of the current uer
        self.current_user_username = username
        self.current_user_password = password
        self.current_user_email = email
        self.current_user_full_name = full_name
        self.current_user_plan = plan
        self.current_user_profile_count = profile_count
    
    def get_user_information(self, parameter): # Getter function to receive the email of the current user for identification
        if parameter == "username":
            return self.current_user_username
        if parameter == "password":
            return self.current_user_password
        if parameter == "email":
            return self.current_user_email
        if parameter == "full_name":
            return self.current_user_full_name
        if parameter == "plan":
            return self.plan
        if parameter == "profile_count":
            return self.current_user_profile_count

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
        ctk.CTkLabel(self.frame_form, text="Sign In", font=("Arial", 40)).grid(row=0, column=0, padx=10, pady=10)

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
        with open("account_information.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    self.controller.set_user_information(row[0], row[1], row[2], row[3], row[4], row[5]) # Sets the current user details
                    return True

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
        ctk.CTkLabel(self.frame_start, text="Who's Watching?", font=("Arial", 40)).grid(row=0, column=1, padx=10, pady=10)

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

        ctk.CTkLabel(self.frame_start, text="Create Account", font=("Arial", 40)).grid(row=0, column=0, padx=10, pady=10)
        
        self.profile_name = ctk.CTkEntry(self.frame_start, placeholder_text="Profile Name", height=50, width=300)
        self.profile_name.grid(row=1, column=0, pady=10)
        
        self.age_rating = ctk.CTkOptionMenu(self.frame_start, values=["G", "PG", "M", "MA15+", "R18+"], height=50, width=300)
        self.age_rating.grid(row=2, column=0, pady=10)
        
        ctk.CTkButton(self.frame_start, text="Create Profile", command=self.add_profile).grid(row=3, column=0, sticky="n")
    
    def add_profile(self):
        profile_name = self.profile_name.get()
        profile_age_rating = self.age_rating.get()
        account_email = self.controller.get_user_information("email")

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
    
class nutflixBrowse(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global media_list
        self.build_ui(media_list)
    
    def build_ui(self, media):
        self.scrollable_menu = ctk.CTkScrollableFrame(self)
        self.scrollable_menu.pack(fill="both", expand=True)
        
        self.scrollable_menu.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) 
        self.scrollable_menu.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        for i in media: # Creates instance of media_widget in a grid layout
            index = media.index(i)
            row = index // 5 # 5 rows
            col = index % 5 # (5-1) columns
            self.media_widget(i).grid(row=row, column=col, padx=5, pady=5, sticky="n")
    
    def media_widget(self, media):
        frame_thumbnail = ctk.CTkFrame(self.scrollable_menu)
        # ImageEnhance dims the thumbnail image by 0.5
        image_thumbnail = ctk.CTkImage(light_image=media.get_image(), dark_image=media.get_image(), size=(192, 108))

        #Image of the widget
        label_thumbnail = ctk.CTkLabel(frame_thumbnail, image=image_thumbnail, text="")
        label_thumbnail.pack(fill="both", padx=1, pady=1)

        self.label_thumbnail = label_thumbnail
        self.image_thumbnail = image_thumbnail

        return frame_thumbnail

if __name__ == "__main__":
    app = nutflixApp()
    app.mainloop()