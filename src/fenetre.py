import os
import threading
from tkinter import Tk, Label, Button, filedialog, Radiobutton, Frame, StringVar, IntVar, Entry, ttk, Menu, PhotoImage, \
    Toplevel, Canvas, Scrollbar
import directories_manangement as dm
import file_metadata as fm
import map
from PIL import Image, ImageTk


class HolidaysSortPicturesApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pixif")
        self.geometry("800x800")
        self.resizable(False, False)
        self.all_elements = []
        self.create_menu()
        self.init_welcome_page()

    def init_sort_variables(self):
        # Variables
        self.source_directory = StringVar()
        self.destination_directory = StringVar()
        self.sort_by = StringVar()
        # List of files with problems
        self.files_problem = []
        # Number of files sorted
        self.nb_files_sorted = IntVar()
        self.nb_files_to_sort = IntVar()
        # Generate map
        self.generate_map = IntVar()

    def create_menu(self):
        # Create the menu
        menu_bar = Menu(self)
        # Create the file menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Welcome page", command=self.init_welcome_page)
        file_menu.add_command(label="Sort directory", command=self.init_sort_page)
        file_menu.add_command(label="Find pictures", command=self.init_find_page)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        # Display the menu
        self.config(menu=menu_bar)

    def init_welcome_page(self):
        """Initializes the welcome page."""
        # Init variables
        self.remove_all_elements()
        # Title
        label_title = Label(self, text="Welcome to Pixif", font=("Arial", 20, "bold"), fg="blue", width=50)
        label_title.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nswe")
        # Explanation
        label_explanation = Label(self,
                                  text="This application allows you to sort your pictures or find them by localization.")
        label_explanation.grid(row=1, column=0, columnspan=6, padx=10, pady=20, sticky="nswe")
        # Sort button
        button_sort = Button(self, text="Sort pictures", command=self.init_sort_page)
        button_sort.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nswe")
        # Find button
        button_find = Button(self, text="Find pictures", command=self.init_find_page)
        button_find.grid(row=2, column=3, columnspan=2, padx=10, pady=10, sticky="nswe")

        self.all_elements.append(label_title)
        self.all_elements.append(label_explanation)
        self.all_elements.append(button_sort)
        self.all_elements.append(button_find)



    def init_sort_page(self):
        """Initializes the sort page."""
        # Init variables
        self.remove_all_elements()
        self.init_sort_variables()
        # Title
        label_title = Label(self, text="Sort Your Pictures", font=("Arial", 20, "bold"), fg="blue", width=50)
        label_title.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nswe")
        # Explanation
        label_explanation = Label(self,
                                  text="This application allows you to sort your pictures by place, date or both.")
        label_explanation.grid(row=1, column=0, columnspan=6, padx=10, pady=20, sticky="nswe")
        # Source
        label_source = Label(self, text="Source directory :")
        label_source.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        self.entry_source = Button(self, text="Select", command=self.select_source_directory)
        self.entry_source.grid(row=2, column=3, padx=10, pady=10, sticky="W")
        label_source_value = Entry(self, textvariable=self.source_directory, width=40)
        label_source_value.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="E")

        # Destination
        label_destination = Label(self, text="Destination directory :")
        label_destination.grid(row=3, column=0, padx=10, pady=10, sticky="E")
        label_destination_value = Entry(self, textvariable=self.destination_directory, width=40)
        label_destination_value.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="E")
        self.entry_destination = Button(self, text="Select", command=self.select_destination_directory)
        self.entry_destination.grid(row=3, column=3, padx=10, pady=10, sticky="W")
        # Sort by
        label_sort_by = Label(self, text="Sort by :")
        label_sort_by.grid(row=4, column=0, padx=10, pady=10, sticky="E")

        # Radio buttons
        self.sort_by.set("Place")
        radio_button1 = Radiobutton(self, text="Place", variable=self.sort_by, value="Place")
        radio_button1.grid(row=4, column=1, padx=10, pady=10, sticky="E")

        radio_button2 = Radiobutton(self, text="Date", variable=self.sort_by, value="Date")
        radio_button2.grid(row=4, column=2, padx=10, pady=10)

        radio_button3 = Radiobutton(self, text="Both", variable=self.sort_by, value="Both")
        radio_button3.grid(row=4, column=3, padx=10, pady=10, sticky="W")

        # Check button for generated map
        check_button = ttk.Checkbutton(self, text="Generate map", variable=self.generate_map)
        check_button.grid(row=5, column=2, padx=10, pady=10, sticky="W")

        # Sort button
        button_sort = Button(self, text="Sort", command= self.sort, bg="#00FF00")
        button_sort.grid(row=6, column=0, columnspan=6, padx=10, pady=10)

        # Label error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

        # Add elements to the list of all elements
        self.all_elements.append(label_title)
        self.all_elements.append(label_explanation)
        self.all_elements.append(label_source)
        self.all_elements.append(self.entry_source)
        self.all_elements.append(label_source_value)
        self.all_elements.append(label_destination)
        self.all_elements.append(label_destination_value)
        self.all_elements.append(self.entry_destination)
        self.all_elements.append(label_sort_by)
        self.all_elements.append(radio_button1)
        self.all_elements.append(radio_button2)
        self.all_elements.append(radio_button3)
        self.all_elements.append(check_button)
        self.all_elements.append(button_sort)
        self.all_elements.append(self.label_error)



    def init_find_page(self):
        """Initializes find pictures page"""
        self.remove_all_elements()
        self.init_find_variables()
        # Title
        label_title = Label(self, text="Find Your Pictures", font=("Arial", 20, "bold"), fg="blue", width=50)
        label_title.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nswe")
        # Explanation
        label_explanation = Label(self, text="This application allows you to find your pictures.")
        label_explanation.grid(row=1, column=0, columnspan=6, padx=10, pady=20, sticky="nswe")
        # Source
        label_source = Label(self, text="Source directory :")
        label_source.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        self.entry_source = Button(self, text="Select", command=self.select_source_directory)
        self.entry_source.grid(row=2, column=3, padx=10, pady=10, sticky="W")
        label_source_value = Entry(self, textvariable=self.source_directory, width=40)
        label_source_value.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="E")

        # Place entry
        label_place = Label(self, text="Place :")
        label_place.grid(row=3, column=0, padx=10, pady=10, sticky="E")
        self.entry_place = Entry(self, textvariable=self.place, width=40)
        self.entry_place.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="E")

        # Exact match
        self.exact_match.set(0)
        check_button = ttk.Checkbutton(self, text="Exact match", variable=self.exact_match)
        check_button.grid(row=3, column=3, padx=10, pady=10, sticky="W")

        # Find button
        button_find = Button(self, text="Find", command=self.find, bg="#00FF00")
        button_find.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

        # Label error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.grid(row=5, column=0, columnspan=6, padx=10, pady=10)

        # Add elements to the list of all elements
        self.all_elements.append(label_title)
        self.all_elements.append(label_explanation)
        self.all_elements.append(label_source)
        self.all_elements.append(self.entry_source)
        self.all_elements.append(label_source_value)
        self.all_elements.append(label_place)
        self.all_elements.append(self.entry_place)
        self.all_elements.append(check_button)
        self.all_elements.append(button_find)
        self.all_elements.append(self.label_error)


    def select_source_directory(self):
        """Select the source directory"""
        directory = filedialog.askdirectory()
        self.source_directory.set(directory)

    def select_destination_directory(self):
        """Select the destination directory"""
        directory = filedialog.askdirectory()
        self.destination_directory.set(directory)

    def sort(self):
        """Sort the pictures"""
        if self.source_directory.get() != "" and self.destination_directory.get() != "" and self.sort_by.get() != "":
            self.show_process()
            # Create a new thread for the sorting operation
            sorting_thread = threading.Thread(target=self.perform_sorting)
            sorting_thread.start()
        else:
            self.label_error.config(text="Please select directories and sort algorithm.")

    def perform_sorting(self):
        """Perform the sorting operation"""
        try:
            self.sort_pictures()  # Update the variables within the sorting process
            self.hide_process()
        except Exception as e:
            self.label_error.config(text="An error was encountered while sorting: " + str(e))
            self.hide_process()

    def find(self):
        """Find the pictures"""
        if self.source_directory.get() != "" and self.place.get() != "":
            # Create a new thread for the sorting operation
            finding_thread = threading.Thread(target=self.perform_finding)
            finding_thread.start()
        else:
            self.label_error.config(text="Please select directory and place.", fg="red")

    def perform_finding(self):
        """Perform the finding operation"""
        try:
            self.label_error.config(text="Finding pictures...", fg="blue")
            pictures = self.find_pictures(self.source_directory.get())
            self.show_pictures(pictures)
            self.label_error.config(text="Found " + str(len(pictures)) + " pictures.", fg="blue")
        except Exception as e:
            self.label_error.config(text="An error was encountered while finding: " + str(e), fg="red")

    def hide_label_error(self):
        """Hide the label error"""
        self.label_error.config(text="")

    def add_file_problem(self, dict_problem : dict):
        """Add a file to the list of files that could not be sorted"""
        self.files_problem.append(dict_problem)

    def update_progress_bar(self):
        """Update the progress bar"""
        if self.sort_by.get() == "Place" or self.sort_by.get() == "Date":
            self.progress_bar["value"] = self.nb_files_sorted.get() / self.nb_files_to_sort.get() * 100
        else :
            self.progress_bar["value"] = self.nb_files_sorted.get() / (self.nb_files_to_sort.get() * 2) * 100

    def show_process(self):
        """Show the process"""
        # Hide the label error
        self.hide_label_error()
        # Process frame
        self.process_frame = Frame(self, borderwidth=2, relief="groove", padx=10, pady=10)
        # Initialize the labels
        self.label_process = Label(self.process_frame, text="Sorting...")
        self.label_process.grid(row=0, column=0, padx=10, pady=10)
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.process_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"] = 0
        self.progress_bar.grid(row=1, column=0, padx=10, pady=10)
        self.label_nb_files_sorted = Label(self.process_frame, text="Number of files sorted : ")
        self.label_nb_files_sorted.grid(row=2, column=0, padx=10, pady=10)
        self.value_nb_files_sorted = Label(self.process_frame, textvariable=self.nb_files_sorted)
        self.value_nb_files_sorted.grid(row=2, column=1, padx=10, pady=10)
        self.label_nb_files_to_sort = Label(self.process_frame, text="Number of files to sort : ")
        self.label_nb_files_to_sort.grid(row=3, column=0, padx=10, pady=10)
        self.value_nb_files_to_sort = Label(self.process_frame, textvariable=self.nb_files_to_sort)
        self.value_nb_files_to_sort.grid(row=3, column=1, padx=10, pady=10)
        # Display the process frame
        self.process_frame.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

    def hide_process(self):
        """Hide the process"""
        # Remove the process frame if it exists
        if self.process_frame.winfo_exists():
            self.process_frame.destroy()

    def show_pictures(self, pictures : list):
        """Show matching pictures"""
        if len(pictures) > 0:
            # Create a Canvas frame
            canvas_frame = Frame(self)
            canvas_frame.grid(row=8, column=0, columnspan=6, padx=10, pady=10)

            canvas = Canvas(canvas_frame, bg="white", width=500, height=300)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = Scrollbar(canvas_frame, command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.config(yscrollcommand=scrollbar.set)

            # Bind mousewheel and double click events
            canvas.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(event, canvas))

            images_per_row = 4 if len(pictures) >= 4 else len(pictures)
            image_width = 100 if len(pictures) >= 4 else 400 // len(pictures)
            image_height = 100 if len(pictures) >= 4 else 400 // len(pictures)

            self.images_references = []

            # Display each picture
            for idx, filename in enumerate(pictures):
                image = self.resize_image(filename, image_width, image_height)
                self.images_references.append(image)
                row = idx // images_per_row
                col = idx % images_per_row
                x = col * image_width + 10 * col
                y = row * image_height + 10 * row
                canvas.create_image(x, y, anchor="nw", image=image, tags=filename)


    def remove_all_elements(self):
        """Remove all elements from the window"""
        for element in self.all_elements:
            element.destroy()
        self.all_elements = []

    def init_find_variables(self):
        # Variables
        self.source_directory = StringVar()
        self.place = StringVar()
        self.exact_match = IntVar()
        
        
    # SORT ALGORITHMS

    def sort_picture_place(self, source_directory: str, destination_directory: str):
        """Sorts the picture in the source directory by place."""
        # Change the current directory to the source directory
        os.chdir(source_directory)
        # For each file in the source directory
        for file in os.listdir(source_directory):
            if dm.is_image(file):
                # Process
                exif_data = fm.picture_exif_data(file)
            elif dm.is_video(file):
                # Process
                exif_data = fm.video_exif_data(file)
            else:
                # Do nothing
                print(f"The file {file} is not a picture or a video.")
                dict_problem = {"file": file, "reason": "not a picture or a video"}
                self.add_file_problem(dict_problem)
                continue
            try:
                # Get the location
                decimal_pos = fm.exif2decimal_position(exif_data["GPSInfo"])
                location = fm.get_location(decimal_pos[0], decimal_pos[1])
                # Get the place
                place = fm.place(location)
                # Create the place directory if it does not exist
                city_folder = dm.create_subdirectory(destination_directory, place)
                # Move the file to the city directory
                path_img = dm.move_file(file, city_folder)
                print(f"File '{file}' moved to '{city_folder}' successfully.")
                # Add one to the number of files moved
                self.nb_files_sorted.set(self.nb_files_sorted.get() + 1)
                self.update_progress_bar()
                # Add the place to the map if necessary
                if self.generate_map.get() != 0 and dm.is_image(path_img):
                    self.map = map.add_marker(self.map, decimal_pos[0], decimal_pos[1], path_img)
            except KeyError:
                print(f"The file {file} does not contain GPS information.")
                dict_problem = {"file": file, "reason": "no GPS information"}
                self.add_file_problem(dict_problem)

    def sort_picture_date(self, source_directory: str, destination_directory: str):
        """Sorts the picture in the source directory by date."""
        for file in os.listdir(source_directory):
            if dm.is_image(file):
                # Process
                exif_data = fm.picture_exif_data(file)
            elif dm.is_video(file):
                # Process
                exif_data = fm.video_exif_data(file)
            else:
                # Do nothing
                print(f"The file {file} is not a picture or a video.")
                dict_problem = {"file": file, "reason": "not a picture or a video"}
                self.add_file_problem(dict_problem)
                continue
            try:
                # Get the location
                decimal_pos = fm.exif2decimal_position(exif_data["GPSInfo"])
                # Get the date
                date = fm.date(exif_data)
                # Create the date directory if it does not exist
                date_folder = dm.create_subdirectory(destination_directory, date)
                # Move the file to the date directory
                path_img = dm.move_file(file, date_folder)
                print(f"File '{file}' moved to '{date_folder}' successfully.")
                # Add one to the number of files moved
                self.nb_files_sorted.set(self.nb_files_sorted.get() + 1)
                self.update_progress_bar()
                # Add the place to the map if necessary
                if self.generate_map.get() != 0 and dm.is_image(path_img):
                    self.map = map.add_marker(self.map, decimal_pos[0], decimal_pos[1], path_img)
            except KeyError:
                print(f"The file {file} does not contain GPS information.")
                dict_problem = {"file": file, "reason": "no GPS information"}
                self.add_file_problem(dict_problem)

    def sort_pictures(self):
        """Sorts the picture in the source directory by sort_by (place, date or both)."""
        source = self.source_directory.get()
        destination = self.destination_directory.get()
        # Reset the number of files sorted
        self.nb_files_sorted.set(0)
        if self.generate_map.get() == 1:
            self.map = map.create_map()
        if self.sort_by.get() == "Place":
            self.nb_files_to_sort.set(dm.number_of_images_or_videos(source))
            self.sort_picture_place(source, destination)
        elif self.sort_by.get() == "Date":
            self.nb_files_to_sort.set(dm.number_of_images_or_videos(self.source_directory.get()))
            self.sort_picture_date(source, destination)
        elif self.sort_by.get() == "Both":
            self.nb_files_to_sort.set(dm.number_of_images_or_videos(self.source_directory.get()))
            # Fist sort by date
            self.sort_picture_date(source, destination)
            # Sort every subdirectory by date
            subdirectories = os.listdir(destination)
            for directory in subdirectories:
                # If it's a directory
                if os.path.isdir(os.path.join(destination, directory)):
                    global_path = os.path.join(destination, directory)
                    print(f"Sorting {global_path} by place.")
                    # Sort by place
                    self.sort_picture_place(global_path, global_path)
        if self.generate_map.get() == 1:
            # Go to destination directory
            os.chdir(destination)
            map.save_map(self.map)
            # Display map in browser
            map.web_view("map.html")
        else:
            print(f"The sort_by argument '{self.sort_by.get()}' is not valid.")

    # FIND ALGORITHMS
    def find_pictures(self, source_directory: str) -> list:
        """Find every pictures taken in a place"""
        # Get variables values
        place = self.place.get()
        exact_match = self.exact_match.get()
        # Process
        os.chdir(source_directory)
        matching_pictures = []
        # For each file in the source directory
        for file in os.listdir(source_directory):
            path = os.path.join(source_directory, file)
            if dm.is_image(file):
                # Process
                exif_data = fm.picture_exif_data(file)
                try:
                    # Get the location
                    decimal_pos = fm.exif2decimal_position(exif_data["GPSInfo"])
                    location = fm.get_location(decimal_pos[0], decimal_pos[1])
                    if fm.is_place_corresponding(location, place, bool(exact_match)):
                        matching_pictures.append(path)
                except KeyError:
                    print(f"The file {file} does not contain GPS information.")
                    self.add_file_problem({"file": file, "reason": "no GPS information"})
            elif dm.is_video(file):
                # Process
                exif_data = fm.video_exif_data(file)
                try:
                    # Get the location
                    decimal_pos = fm.exif2decimal_position(exif_data["GPSInfo"])
                    location = fm.get_location(decimal_pos[0], decimal_pos[1])
                    if fm.is_place_corresponding(location, place, bool(exact_match)):
                        matching_pictures.append(path)
                except KeyError:
                    print(f"The file {file} does not contain GPS information.")
                    self.add_file_problem({"file": file, "reason": "no GPS information"})
            elif dm.is_directory(file):
                # Recursively call the function
                matching_pictures += self.find_pictures(path)
            else:
                # Do nothing
                print(f"The file {file} is not a picture or a video.")
                self.add_file_problem({"file": file, "reason": "not a picture or a video"})
                continue
        return matching_pictures

    # PICTURES ALGORITHMS

    def resize_image(self, image_path, width, height):
        img = Image.open(image_path)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)


    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
