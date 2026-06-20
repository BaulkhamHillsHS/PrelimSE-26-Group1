import customtkinter as ctk
from PIL import Image, ImageEnhance
import csv
import random
import ast

import os
import platform
from datetime import datetime

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme_nutflix.JSON")

logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_transparent.png")

age_rating_order = ["G", "PG", "M", "MA15+", "R18+"] # Used for comparing age ratings of profiles and media
plan_profile_limits = {"Peanut": 2, "Kingnut": 4} # Limits on how many profiles an account can have, based on their subscription tier

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

    def get_name(self): # Getter function for the widget to collect the name
        return self.name
    
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

class account:
    def __init__(self, username, password, email, plan):
        self.current_user_username = username
        self.current_user_password = password
        self.current_user_email = email
        self.current_user_plan = plan

    def get_user_information(self, parameter): # Getter function to receive the details  of the current user
        if parameter == "username":
            return self.current_user_username
        if parameter == "password":
            return self.current_user_password
        if parameter == "email":
            return self.current_user_email
        if parameter == "full_name":
            return self.current_user_full_name
        if parameter == "plan":
            return self.current_user_plan
    
    def profile_added(self, name, age_rating): # Called when the user adds a new profile
        new_profile = profile(name, age_rating, "[]", "[]", self.current_user_username, self.current_user_password, self.current_user_email, self.current_user_plan)
        current_account_profiles.append(new_profile)

class profile(account):
    def __init__(self, name, age_rating, recently_watched, watchlist, username, password, email, plan):
        super().__init__(username, password, email, plan)
        self.name = name
        self.age_rating = age_rating
        self.recently_watched = recently_watched
        self.watchlist = watchlist
        self.email = email
    
    def get_name(self):
        return self.name
    
    def get_age_rating(self):
        return self.age_rating
    
    def get_recently_watched(self):
        return self.recently_watched
    
    def get_watchlist(self):
        return self.watchlist
    
    def get_email(self):
        return self.email

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
        for f in (nutflixSignIn, nutflixStart, nutflixCreateProfile, nutflixSubscriptions, nutflixBrowse, nutflixWatch):
            frame = f(self.container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(nutflixSignIn)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == nutflixBrowse:
            frame.build_ui(media_list)
            self.update_watchlist(self.current_profile_watchlist)
        if cont == nutflixStart:
            frame.build_profile_buttons()
        if cont == nutflixSubscriptions:
            frame.show_plans()
        frame.tkraise()
    
    def set_user_information(self, username, password, email, plan): # Setter function to set the account information of the current uer
        self.current_user_username = username
        self.current_user_password = password
        self.current_user_email = email
        self.current_user_plan = plan
    
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
            return self.current_user_plan
    
    def set_profile(self, profile_name, max_age_rating, recently_watched, watchlist):
        self.current_profile_name = profile_name
        self.current_profile_age_rating = max_age_rating
        self.current_profile_recently_watched = recently_watched
        self.current_profile_watchlist = watchlist
    
    def get_profile(self, parameter):
        if parameter == "name":
            return self.current_profile_name
        if parameter == "age_rating":
            return self.current_profile_age_rating
        if parameter == "recently_watched":
            return self.current_profile_recently_watched
        if parameter == "watchlist":
            return self.current_profile_watchlist
    
    def update_watchlist(self, watchlist): # Used to update the profile watchlist ui when a title is added to the watchlist
        for widget in self.frames[nutflixBrowse].scrollable_watchlist.winfo_children(): # Destroy exisitng widgets first
            widget.destroy()

        self.current_profile_watchlist = watchlist
        self.frames[nutflixBrowse].build_watchlist(ast.literal_eval(watchlist))
    
    def set_watching(self, watching): # Setter function for setting the show/movie the user is currently watching
        self.watching = watching
    
    def get_watching(self): # Getter function to know which show/movie the user is watching
        try:
            return self.watching
        except:
            print("User is not watching...")

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
                    global current_account # This becomes the currently logged in account
                    current_account = account(row[0], row[1], row[2], row[3]) # Sets the current user details
                    self.get_existing_profiles(row[0], row[1], row[2], row[3])
                    return True
    
    def get_existing_profiles(self, username, password, email, plan):
        global current_account_profiles # List of all profiles under the account
        current_account_profiles = []
        
        with open("profile_information.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    current_profile = profile(row[1], row[2], row[3], row[4], username, password, email, plan)

                    current_account_profiles.append(current_profile)

                    print(current_account_profiles)

class nutflixStart(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()
    
    def build_ui(self):
        self.frame_start = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_start.pack(fill="both", expand=True)

        self.frame_start.grid_columnconfigure(0, weight=1) 
        self.frame_start.grid_rowconfigure(0, weight=1) # top spacing
        self.frame_start.grid_rowconfigure(1, weight=0) # heading
        self.frame_start.grid_rowconfigure(2, weight=0) # profiles
        self.frame_start.grid_rowconfigure(3, weight=1) # bottom spacing
        self.frame_start.grid_rowconfigure(4, weight=0) # bottom buttons
        
        # Heading
        ctk.CTkLabel(self.frame_start, text="Who's Watching?", font=("Arial", 42, "bold")).grid(row=1, column=0, pady=(0, 50))

        # Profile Select
        self.frame_profile_menu = ctk.CTkFrame(self.frame_start, fg_color="transparent")
        self.frame_profile_menu.grid(row=2, column=0)

        # Bottom Buttons
        self.frame_bottom = ctk.CTkFrame(self.frame_start, fg_color="transparent")
        self.frame_bottom.grid(row=4, column=0, sticky="ew", padx=40, pady=30)
        self.frame_bottom.grid_columnconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(1, weight=1)

        self.button_subscription = ctk.CTkButton(self.frame_bottom, text="Manage Subscription", font=("Arial", 14), width=160, height=40, command=lambda: self.controller.show_frame(nutflixSubscriptions))
        self.button_subscription.grid(row=0, column=1, sticky="e")

    def build_profile_buttons(self): # Runs whenever the page loads through the controller
        #Profile Buttons
        tile = 160
        
        profile_amount = len(current_account_profiles)

        for i in self.frame_profile_menu.winfo_children(): # Destroys pre-existing widgets for clean execution
            i.destroy()

        for i, profile in enumerate(current_account_profiles):
            # Variables of the profile
            name = profile.get_name()
            age_rating = profile.get_age_rating()
            recently_watched = profile.get_recently_watched()
            watchlist = profile.get_watchlist()

            profile_tile = ctk.CTkFrame(self.frame_profile_menu, fg_color="transparent")
            profile_tile.grid(row=0, column=i, padx=18)

            button_profile = ctk.CTkButton(profile_tile, command=lambda name=name, age=age_rating, recent=recently_watched, watchlist=watchlist: self.select_profile(name, age, recent, watchlist), text="", corner_radius=10, width=tile, height=tile)
            button_profile.pack()

            ctk.CTkLabel(profile_tile, text=name, font=("Arial", 16), text_color="#cccccc").pack(pady=(10, 0))

            button_delete = ctk.CTkButton(self.frame_profile_menu, text="Delete Profile", font=("Arial", 14), width=125, height=25, command=lambda i=i: self.delete_profile(i))
            button_delete.grid(row=1, column=i, pady=0)

        #Create Profile
        if profile_amount < 4: # If the profile amount has not reached the limit, the create profile button will show up
            create_tile = ctk.CTkFrame(self.frame_profile_menu, fg_color="transparent")
            create_tile.grid(row=0, column=profile_amount, padx=18)

            self.button_profile_create = ctk.CTkButton(create_tile, text="+", command=lambda: self.controller.show_frame(nutflixCreateProfile), font=("Arial", 48), corner_radius=10, width=tile, height=tile, fg_color="#1a1a1a", hover_color="#2a2a2a", border_width=2, border_color="#555555", text_color="#888888")
            self.button_profile_create.pack()

            ctk.CTkLabel(create_tile, text="Add Profile", font=("Arial", 16), text_color="#888888").pack(pady=(10, 0))

    def delete_profile(self, index):
        profile = current_account_profiles[index]
        name = profile.get_name()

        remaining_rows = []
        with open("profile_information.csv", "r") as file: # Csv containing profile information
            reader = csv.reader(file)
            for row in reader:
                if not (row[1] == name and row[0] == current_account.current_user_email):
                    remaining_rows.append(row)
        
        with open("profile_information.csv", "w", newline="") as file: # Delete profile from csv
            writer = csv.writer(file)
            writer.writerows(remaining_rows)
        
        for i in current_account_profiles:
            if i.get_name() == name and i.get_email() == current_account.current_user_email:
                current_account_profiles.remove(i)
        self.controller.show_frame(nutflixStart) # Refreshes page to update ui
    
    def select_profile(self, name, age_rating, recently_watched, watchlist):
        self.controller.set_profile(name, age_rating, recently_watched, watchlist)
        self.controller.show_frame(nutflixBrowse)

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

        ctk.CTkLabel(self.frame_start, text="Create Profile", font=("Arial", 40)).grid(row=0, column=0, padx=10, pady=10)
        
        self.profile_name = ctk.CTkEntry(self.frame_start, placeholder_text="Profile Name", height=50, width=300)
        self.profile_name.grid(row=1, column=0, pady=10)
        
        self.age_rating = ctk.CTkOptionMenu(self.frame_start, values=["G", "PG", "M", "MA15+", "R18+"], height=50, width=300)
        self.age_rating.grid(row=2, column=0, pady=10)
        
        ctk.CTkButton(self.frame_start, text="Create Profile", command=self.add_profile).grid(row=3, column=0, sticky="n")
    
    def add_profile(self):
        profile_name = self.profile_name.get()
        profile_age_rating = self.age_rating.get()
        recently_watched = "[]"
        watchlist = "[]"
        account_email = current_account.get_user_information("email")

        profile = [account_email, profile_name, profile_age_rating, recently_watched, watchlist] # Email is a global value

        with open("profile_information.csv", "r") as file: # csv containing profile information
            reader = csv.reader(file)
            for row in reader:
                if (row[0], row[1]) == (account_email, profile_name):
                    return # Profile with same name under same email already exists

        with open("profile_information.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(profile) # Adds profile to csv
        
        current_account.profile_added(profile_name, profile_age_rating) # Immediately updates the profile count of the current account by +1   
        self.controller.show_frame(nutflixStart) # Takes user back to the start page

plan_details = {
    "Peanut": {
        "price": "$7.99/mo",
        "perks": [
            "SD, 720p",
            "Watch on 1 device at a time",
            "Download on 1 device",
            ],
    },
    "Kingnut": {
        "price": "$14.99/mo",
        "perks": [
            "Ultra HD 4K + HDR",
            "Watch on 4 devices at a time",
            "Download on 4 devices",
            "Spatial, Lossless Audio",
            "Ad-Free",
            ],
    }
}

class nutflixSubscriptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()
    
    def build_ui(self):
        self.frame_start = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_start.pack(fill="both", expand=True)
        
        self.frame_start.grid_columnconfigure(0, weight=1)
        self.frame_start.grid_rowconfigure(0, weight=1) # top spacing
        self.frame_start.grid_rowconfigure(1, weight=0) # heading
        self.frame_start.grid_rowconfigure(2, weight=0) # plan details
        self.frame_start.grid_rowconfigure(3, weight=1) # info label
        self.frame_start.grid_rowconfigure(4, weight=1) # bottom spacing
        self.frame_start.grid_rowconfigure(5, weight=0) # back button
        
        ctk.CTkLabel(self.frame_start, text="Manage Subscription", font=("Arial", 40, "bold")).grid(row=1, column=0, pady=(0, 50))
        
        self.frame_plans = ctk.CTkFrame(self.frame_start, fg_color="transparent")
        self.frame_plans.grid(row=2, column=0)
        
        self.info_label = ctk.CTkLabel(self.frame_start, text="", font=("Arial", 14), text_color="#888888")
        self.info_label.grid(row=3, column=0, pady=(20, 0))
        
        ctk.CTkButton(self.frame_start, text="Back", command=lambda: self.controller.show_frame(nutflixStart)).grid(row=5, column=0, pady=30)
    
    def show_plans(self):
        self.info_label.configure(text="")
        for widget in self.frame_plans.winfo_children():
            widget.destroy()
        
        current_plan = current_account.get_user_information("plan")
        
        for col, (plan_name, details) in enumerate(plan_details.items()):
            is_current = (plan_name == current_plan)
            
            card = ctk.CTkFrame(self.frame_plans, width=280, height=380, corner_radius=10, border_width=2, border_color="#C0152A" if is_current else "#2A2A2A")
            card.grid(row=0, column=col, padx=20)
            card.grid_propagate(False)
            card.grid_columnconfigure(0, weight=1)
            card.grid_rowconfigure(2, weight=1)
            card.grid_rowconfigure(3, weight=0)
            
            ctk.CTkLabel(card, text=plan_name, font=("Arial", 26, "bold")).grid(row=0, column=0, pady=(25, 5))
            ctk.CTkLabel(card, text=details["price"], font=("Arial", 16)).grid(row=1, column=0, pady=(0, 20))
            
            perks_text = "\n".join(f"✓  {perk}" for perk in details["perks"])
            ctk.CTkLabel(card, text=perks_text, font=("Arial", 14), justify="left", anchor="w").grid(row=2, column=0, padx=25, sticky="nw")

            if is_current:
                ctk.CTkButton(card, text="Current Plan", font=("Arial", 14), width=200, height=40, fg_color="#2A2A2A", hover_color="#2A2A2A", text_color="#888888", state="disabled").grid(row=3, column=0, pady=(20, 25))
            else:
                ctk.CTkButton(card, text="Switch to " + plan_name, font=("Arial", 14), width=200, height=40, command=lambda p=plan_name: self.switch_plan(p)).grid(row=3, column=0, pady=(20, 25))
    
    def switch_plan(self, new_plan):
        updated_rows = []
        with open("account_information.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == current_account.get_user_information("email"):
                    row[3] = new_plan
                updated_rows.append(row)
                
        with open("account_information.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
            
        current_account.current_user_plan = new_plan
        self.show_plans()
    
class nutflixBrowse(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        global media_list
    
    def add_watchlist(self, name):
        current_watchlist = self.controller.get_profile("watchlist")
        if name in current_watchlist:
            print("Title already in watchlist.")
            return
            
        editable_watchlist = ast.literal_eval(current_watchlist) # Converts the string representation of the list into an actual list
        editable_watchlist.append(name)

        updated_rows = []
        with open("profile_information.csv", "r", newline="") as file: # Reads the current data
            reader = csv.reader(file)
            for row in reader:
                if row[0] == current_account.get_user_information("email") and row[1] == self.controller.get_profile("name"): # Finds the row which matches with the current user and the specific profile
                    row[4] = str(editable_watchlist)
                updated_rows.append(row) # Copies the current data into 'updated_rows', along with the updated row
            
        with open("profile_information.csv", "w", newline="") as file: # Rewrites the 'account_information.csv' using the updated rows
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        self.controller.update_watchlist(str(editable_watchlist))

    def remove_watchlist(self, name):
        current_watchlist = self.controller.get_profile("watchlist")
        
        editable_watchlist = ast.literal_eval(current_watchlist) # Converts the string representation of the list into an actual list
        editable_watchlist.remove(name)

        updated_rows = []
        with open("profile_information.csv", "r", newline="") as file: # Reads the current data
            reader = csv.reader(file)
            for row in reader:
                if row[0] == current_account.get_user_information("email") and row[1] == self.controller.get_profile("name"): # Finds the row which matches with the current user and the specific profile
                    row[4] = str(editable_watchlist)
                updated_rows.append(row) # Copies the current data into 'updated_rows', along with the updated row
           
        with open("profile_information.csv", "w", newline="") as file: # Rewrites the 'account_information.csv' using the updated rows
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        self.controller.update_watchlist(str(editable_watchlist))
    
    def build_ui(self, media_list):
        # Everything in this scrollable menu
        self.scrollable_menu = ctk.CTkScrollableFrame(self)
        self.scrollable_menu.pack(fill="both", expand=True)
        
        # Recommended Movie/TV Show shows at the top of the scrollable menu
        self.banner_frame = ctk.CTkFrame(self.scrollable_menu, height=600)
        self.banner_frame.pack(fill="x", expand=False, pady=(0, 50))
        
        banner_image = self.choose_banner_media()
        banner = banner_image.get_image().resize((1080, 600))
        banner_ctk = ctk.CTkImage(light_image=banner, dark_image=banner, size=(1080, 600))
        
        ctk.CTkLabel(self.banner_frame, image=banner_ctk, text="").pack(fill="both", expand=True)
        ctk.CTkLabel(self.banner_frame, text=banner_image.get_name(), font=("Arial", 40, "bold"), text_color="white").place(x=30, y=300)
        ctk.CTkButton(self.banner_frame, text="▶ Play", command=lambda: self.watch(banner_image)).place(x=30, y=380)
        ctk.CTkButton(self.banner_frame, text="Add to Watchlist", fg_color="white", text_color="#C0152A", command=lambda: self.add_watchlist(banner_image.get_name())).place(x=180, y=380)

        # Watchlist horizontal scroller
        ctk.CTkLabel(self.scrollable_menu, text="My Watchlist", font=("Arial", 32), anchor="w", bg_color="#161616").pack(fill="both", expand=True, pady=20)

        self.scrollable_watchlist = ctk.CTkScrollableFrame(self.scrollable_menu, orientation="horizontal", height=148)
        self.scrollable_watchlist.pack(fill="x", expand=False, pady=(0, 50))

        self.scrollable_watchlist.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1) 
        self.scrollable_watchlist.grid_rowconfigure((0), weight=0)

        # Media browsing grid
        ctk.CTkLabel(self.scrollable_menu, text="Browse", font=("Arial", 32), anchor="w", bg_color="#161616").pack(fill="both", expand=True, pady=20)

        # Bar for various buttons
        self.frame_buttons = ctk.CTkFrame(self.scrollable_menu, fg_color="#161616", height=30)
        self.frame_buttons.pack(fill="both", expand=True)

        self.frame_buttons.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        self.frame_buttons.grid_rowconfigure((0), weight=0)

        # Download viewing report button
        self.button_download = ctk.CTkButton(self.frame_buttons, text="Open Viewing History", command=self.create_viewing_report)
        self.button_download.grid(row=0, column=3)

        self.grid_frame = ctk.CTkFrame(self.scrollable_menu, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)
        
        self.grid_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) 
        self.grid_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        max_age_rating = self.controller.get_profile("age_rating")
        allowed_media = []
        for i in media_list:
            if age_rating_order.index(i.age_rating) <= age_rating_order.index(max_age_rating): # Filters out media that is above the profile's age rating
                allowed_media.append(i)
        
        for i in allowed_media: # Creates instance of media_widget in a grid layout
            index = allowed_media.index(i)
            row = index // 5 # 5 rows
            col = index % 5 # (5-1) columns
            self.media_widget(i, self.grid_frame, False).grid(row=row, column=col, padx=10, pady=20)
    
    def choose_banner_media(self):
        max_age_rating = self.controller.get_profile("age_rating")
        recently_watched = ast.literal_eval(self.controller.get_profile("recently_watched"))

        # Filtering based on previously watched genres and age rating
        watched_media = []
        for title in recently_watched:
            for i in media_list:
                if i.name == title:
                    if age_rating_order.index(i.age_rating) <= age_rating_order.index(max_age_rating):
                        watched_media.append(i)
        
        watched_genres = set()
        for i in watched_media:
            watched_genres.add(i.genre1)
            watched_genres.add(i.genre2)
    
        matches = []
        for i in media_list:
            if age_rating_order.index(i.age_rating) <= age_rating_order.index(max_age_rating):
                if i.name not in recently_watched:
                    if i.genre1 in watched_genres or i.genre2 in watched_genres:
                        matches.append(i)
        
        # If no matches, pick any movie/TV show that's age appropriate
        if len(matches) == 0:
            matches = []
            for i in media_list:
                if age_rating_order.index(i.age_rating) <= age_rating_order.index(max_age_rating): # if the movie is within the range of which the profile user can watch
                    matches.append(i)
        
        return random.choice(matches)
    
    def media_widget(self, media, frame, isWatchlist):
        name = media.get_name()
        if len(name) > 20: # Ensures that the widget doesnt not stretch out or cut off text abruptly
            name = name[:20] + "..."
        
        frame_thumbnail = ctk.CTkFrame(frame, corner_radius=6, fg_color="#C0152A")
        
        # Button of the widget
        label_thumbnail = ctk.CTkLabel(frame_thumbnail, text=name, height=126, width=192, corner_radius=6, bg_color="#C0152A")
        label_thumbnail.pack(fill="both", expand=True)

        # Hover Preview
        image = ctk.CTkImage(light_image=ImageEnhance.Brightness(media.get_image()).enhance(0.4), dark_image=ImageEnhance.Brightness(media.get_image()).enhance(0.4), size=(180, 116))

        # Add to watchlist button
        if isWatchlist:
            button_watchlist = ctk.CTkButton(label_thumbnail, text="-", height=20, width=20, command=lambda: self.remove_watchlist(media.get_name())) # For destroying widget
        else:
            button_watchlist = ctk.CTkButton(label_thumbnail, text="+", height=20, width=20, command=lambda: self.add_watchlist(media.get_name())) # For adding widget
        
        button_watchlist.place(relx=0.95, rely=0.05, anchor="center")

        def show_image(event):
            label_thumbnail.configure(image=image)
        
        def hide_image(event):
            label_thumbnail.configure(image="")
        
        label_thumbnail.bind("<Enter>", show_image)
        label_thumbnail.bind("<Leave>", hide_image)
        label_thumbnail.bind("<Button-1>", lambda e: self.watch(media))

        return frame_thumbnail
    
    def build_watchlist(self, watchlist):
        for i in watchlist:
            for v in media_list: # Matches the names found in watchlist with its corresponding media object in media_list
                if v.get_name() == i:
                    self.media_widget(v, self.scrollable_watchlist, True).grid(row=0, column=watchlist.index(i), padx=5, pady=5, sticky="w")

    def watch(self, media):
        self.controller.set_watching(media)
        self.controller.show_frame(nutflixWatch) # Todo: Create a new function in NutflixApp for specifically handling nutflixWatch()

    def create_viewing_report(self):
        watch_history = self.controller.get_profile("recently_watched")
        with open("viewing_report.txt", "w", encoding="utf-8") as file:
            current_time = str(datetime.now())

            file.write("///// VIEWING HISTORY /////\n")
            file.write("Time of creation [" + current_time + "]\n")
            for i in ast.literal_eval(watch_history):
                file.write("‣" + i + "\n")

        try:
            if platform.system() == "Darwin":  # macOS
                os.system("open viewing_report.txt")
            elif platform.system() == "Windows":
                    os.startfile("viewing_report.txt")
            elif platform.system() == "Linux":
                os.system("xdg-open viewing_report.txt")
        except Exception as e:
            print(f"Error opening file: {e}")

class nutflixWatch(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()
    
    def build_ui(self):
        self.frame_start = ctk.CTkFrame(self)
        self.frame_start.pack(fill="both", expand=True)
        
        self.frame_start.grid_columnconfigure((0), weight=1) 
        self.frame_start.grid_rowconfigure((0, 1, 2, 3), weight=1)

if __name__ == "__main__":
    app = nutflixApp()
    app.mainloop()