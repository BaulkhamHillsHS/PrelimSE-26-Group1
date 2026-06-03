import customtkinter as ctk
from PIL import Image

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

        self._build_ui()
    
    def _build_ui(self):
        self._build_form_frame()
    
    def _build_form_frame(self):
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
        ctk.CTkButton(self.frame_form, text="Sign In", command=self._sign_in).grid(row=3, column=0, sticky="n")
    
    def _sign_in(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        print(username, password)
