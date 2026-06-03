import customtkinter as ctk
from PIL import Image

from classes.signin_frame import nutflixSignIn
from classes.start_frame import nutflixStart

ctk.set_appearance_mode('light')
ctk.set_default_color_theme("theme_nutflix.JSON")


logo_red = Image.open("images/logo_red.png")
logo_white = Image.open("images/logo_transparent.png")


if __name__ == "__main__":
    app = nutflixStart()
    app.mainloop()