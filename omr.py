import tkinter as tk
from PIL import ImageTk, Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageColor, ImagePalette
from PIL import UnidentifiedImageError

import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("OMR Application")
        self.geometry("1100x580")

        self.grid_columnconfigure(0, weight=1)  # Set weight to 1 for column 0
        self.grid_columnconfigure(1, weight=2)  # Set weight to 2 for column 1
        self.grid_rowconfigure(3, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, width=140, corner_radius=5)
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)  # Expand the single column

        self.header_label = customtkinter.CTkLabel(self.header_frame, text="Examination Paper Auto-Evaluation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.header_label.grid(row=0, column=0, pady=(10, 5))

        self.subheader_label = customtkinter.CTkLabel(self.header_frame, text="Made with OpenCV", font=customtkinter.CTkFont(size=14))
        self.subheader_label.grid(row=1, column=0, pady=(5, 10))

        self.image_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.image_frame.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.image_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.seg_button_1.configure(values=["Processed", "Raw"])
        self.seg_button_1.set("Processed")
        self.seg_button_1.grid_configure(sticky="nsew")

        self.image_holder = customtkinter.CTkFrame(self.image_frame)
        self.image_holder.grid(row=1, column=0, rowspan=4, sticky="nsew")
        self.image_holder.bind("<Configure>", lambda event: self.update_image(event, image_path, self.image_holder))

        self.image_frame.grid_rowconfigure(1, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_holder.grid_rowconfigure(0, weight=1)
        self.image_holder.grid_columnconfigure(0, weight=1)

        # create tabview
        self.parameters_frame = customtkinter.CTkTabview(self, width=250)
        self.parameters_frame.grid(row=1, column=1, rowspan=3, padx=10, pady=0, sticky="nsew")
        self.parameters_frame.add("RAW")
        self.parameters_frame.add("Processed")
        self.parameters_frame.tab("RAW").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.parameters_frame.tab("Processed").grid_columnconfigure(0, weight=1)

        self.parameters_frame2 = customtkinter.CTkFrame(self.parameters_frame, corner_radius=5) 
        self.parameters_frame2.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

        self.combobox_1 = customtkinter.CTkComboBox(self.parameters_frame.tab("RAW"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.status_bar = customtkinter.CTkFrame(self, height=30, corner_radius=5)
        self.status_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
        self.status_label = customtkinter.CTkLabel(self.status_bar, text="Status: Ready")
        self.status_label.grid(row=0, column=0, padx=(10, 5))

        image_path = "images/sample_sheet.jpg"  # Replace with the path to your image
        self.update_image(None, image_path, self.image_holder)  # Call update_image to initially display the image

    def update_image(self, event, image_path, frame):
        image = Image.open(image_path)

        # Check if frame has a valid width and height
        frame_width, frame_height = frame.winfo_width(), frame.winfo_height()
        if frame_width > 0 and frame_height > 0:
            # Calculate the new size of the image based on the frame dimensions
            image_ratio = image.width / image.height
            frame_ratio = frame_width / frame_height

            if frame_ratio > image_ratio:
                new_width = int(frame_height * image_ratio)
                new_height = frame_height
            else:
                new_width = frame_width
                new_height = int(frame_width / image_ratio)

            # Resize the image if the dimensions are valid
            if new_width > 0 and new_height > 0:
                image_margin = 40
                resized_image = image.resize((new_width - image_margin, new_height - image_margin), Image.Resampling.LANCZOS)

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Update the label with the resized image
                image_label = tk.Label(frame, image=photo)
                image_label.image = photo  # Store a reference to prevent garbage collection
                image_label.place(relx=0.5, rely=0.5, anchor="center")  # Place the label within the frame

if __name__ == "__main__":
    app = App()
    app.mainloop()
