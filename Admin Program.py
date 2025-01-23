############ SAM RICHELL COMPUTER SCIENCE NEA ############

from tkinter import *
from tkinter import ttk
import os
import sqlite3


background_colour = "#98F0AA"
button_background_colour = "#048106"
active_button_background_colour = "#049006"
button_text_colour = "#FFFFFF"
label_text_colour = "#000000"
text_box_text_colour = "#000000"
tex_box_background_colour = "#FFFFFF"

# textfont for the whole 
text_font = "Arial"


def setup(bgc, bbc, btc, ltc, tbtc, tbbc, abgc):
    window = Tk()
    #window.geometry("960x540")
    window.configure(bg=bgc)
    style = define_style(window)
    style.configure_button(btc, bbc, abgc)
    style.configure_label(ltc, bgc)
    style.configure_entry(tbtc, tbbc)
    style.configure_checkbutton(bgc)
    style.configure_frame(bgc)
    return window


class Volunteer:
    def __init__(self, ID, forename, surname, email, mobilenumber, address, postcode):
        self.__ID = ID
        self.__forename = forename
        self.__surname =surname
        self.__email = email
        self.__mobilenumber = mobilenumber
        self.__address = address
        self.__postcode = postcode
        self.__PreferredParticipation = []
    
    def add_PP(self, PP):
        self.__PreferredParticipation.append(PP)

    def get_ID(self):
        return self.__ID
    
    def get_forename(self):
        return self.__forename
    
    def get_surname(self):
        return self.__surname
    
    def get_email(self):
        return self.__email
    
    def get_mobilenumber(self):
        return self.__mobilenumber
    
    def get_address(self):
        return self.__address
    
    def get_postcode(self):
        return self.__postcode
    
    def get_PP(self):
        return self.__PreferredParticipation


class define_style:
    def __init__(self, window):
        self.__style = ttk.Style(window)
        self.__style.theme_use("alt")
    
    def configure_button(self, fgc, bgc, abgc):
        self.__style.configure("TButton", foreground=fgc, background=bgc)
        self.__style.map("TButton", background=[("active", abgc)])

    def configure_label(self, fgc, bgc):
        self.__style.configure("TLabel", foreground=fgc, background=bgc)

    def configure_entry(self, fgc, bgc):
        self.__style.configure("TEntry", foreground=fgc, background=bgc)

    def configure_checkbutton(self, bgc):
        self.__style.configure("TCheckbutton", background=bgc)
        self.__style.map("TCheckbutton", background=[("active", bgc)])

    def configure_frame(self, bgc):
        self.__style.configure("TFrame", background=bgc)


def create_frame(root):
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, sticky=(N, E, S, W))
    return frame


class error_window:
    def __init__(self, message, textfont):

        self.__textfont = textfont

        self.__box_window = Tk()
        self.__box_window.configure(bg="#FFFFFF")
        self.__box_window.geometry("150x50+400+300")

        self.__frame = create_frame(self.__box_window)

        self.__error_label = ttk.Label(self.__frame, text=message, font=(self.__textfont, 10))
        self.__error_label.grid(column=0, row=0, sticky=(W, E))

        self.__ok_button = ttk.Button(self.__frame, text="ok", command=self.__box_window.destroy)
        self.__ok_button.grid(column=0, row=1, sticky=(W, E))

        self.__frame.pack()


class Page: # Parent class to all other pages
    def __init__(self, window, textfont, title):
        self._textfont = textfont
        self._window = window
        self._window.title(title)

    def _create_frame(self):
        self._mainframe = create_frame(self._window)
        self._mainframe.pack(padx=250, pady=100)

    def _display_title(self, page_title):
        self._page_title = ttk.Label(self._mainframe, text=page_title, font=(self._textfont, 30, "bold"))

    def _clear_frame(self):
        for widget in self._mainframe.winfo_children():
            widget.destroy()

    def _destroy_frame(self):
        self._mainframe.destroy()

    def _connect(self):
        self._DBPath = os.path.join(os.path.dirname(__file__), "VolunteerDB.sqlite3") #Defining the pathway to the sqlite3 file

        self._SQLiteConnection = sqlite3.connect(self._DBPath) #Connecting to the sql file
        self._cursor = self._SQLiteConnection.cursor() #creating the cursor

    def _close_connection(self):
        self._cursor.close()
        self._SQLiteConnection.close()

    def _display_home_button(self):
        self.__home_button = ttk.Button(self._window, text="Home", command=self.__home)
        self.__home_button.place(x=5, y=5)

    def __home(self): # Subclasses should not be able to access
        self.__home_button.destroy()
        self._clear_frame()
        self._destroy_frame()
        menu_page(self._window, self._textfont)


class password_page(Page): # Password page class
    def __init__(self, window, textfont):
        super().__init__(window, textfont, "Login")
        self._create_frame()
        self._display_title("Welcome")

        self._page_title.grid(column=0, row=0, columnspan=2, padx=5, pady=20)

        self.__correct_password = ""

        self.__password = StringVar()
        self.__password_entry = ttk.Entry(self._mainframe, textvariable=self.__password, width=20, show="*")
        self.__password_entry.grid(column=1, row=1, sticky=(W, E), padx=5, pady=10)
        self.__password_entry.focus()

        self.__login_button = ttk.Button(self._mainframe, text="Login", command=self.__check_password, width=20)
        self.__login_button.grid(column=0, row=2, columnspan=2, sticky=(W, E), padx=5, pady=5)

        self.__password_label = ttk.Label(self._mainframe, text="Password", font=(self._textfont, 16))
        self.__password_label.grid(column=0, row=1, sticky=(W, E), padx=5, pady=5)

    def __check_password(self):       # Checks to make sure the input into the password entry is correct
        if self.__password.get() == self.__correct_password:
            self.__next_page()
        else:
            self.__report_error("Password Incorrect")
    
    def __next_page(self):            # Take user to menu page
        self._clear_frame()
        self._destroy_frame()
        menu_page(self._window, self._textfont)

    def __report_error(self, message): # Uses error_window class to report an error to the user
        error_window(message, self._textfont)


class menu_page(Page): # Menu page class
    def __init__(self, window, textfont):
        super().__init__(window, textfont, "Menu")
        self._create_frame()
        self._display_title("Welcome Admin")
        self._page_title.grid(column=0, row=0, pady=20)

        self.__find_volunteers = ttk.Button(self._mainframe, text="Find Volunteer(s)", command=self.__find_volunteers_page)
        self.__find_volunteers.grid(column=0, row=1, pady=10, sticky=(W, E))

        self.__PP_settings = ttk.Button(self._mainframe, text="Preferred Participation Settings", command=self.__PP_settings_page)
        self.__PP_settings.grid(column=0, row=2, pady=10, sticky=(W, E))

        self.__event_settings = ttk.Button(self._mainframe, text="Event Settings", command=self.__events_settings_page)
        self.__event_settings.grid(column=0, row=3, pady=10, sticky=(W, E))

        self.__log_out = ttk.Button(self._mainframe, text="Log Out", command=self.__logout)
        self.__log_out.grid(column=0, row=4, pady=10, sticky=(W, E))

    def __find_volunteers_page(self):
        self._clear_frame()
        self._destroy_frame()
        find_volunteers_page(self._window, self._textfont)

    def __PP_settings_page(self):
        self._clear_frame()
        self._destroy_frame()
        Preferred_Participation_Settings_Page(self._window, self._textfont)

    def __events_settings_page(self):
        self._clear_frame()
        self._destroy_frame()
        Event_Settings_Page(self._window, self._textfont)

    def __logout(self):
        self._clear_frame()
        self._destroy_frame()
        password_page(self._window, self._textfont)


class find_volunteers_page(Page): # Search for volunteers page class
    def __init__(self, window, textfont):
        super().__init__(window, textfont, "Find Volunteers")
        self._create_frame()
        self._display_title("Find Volunteer(s)")

        self._page_title.grid(column=0, row=0, pady=20, columnspan=3)

        self.__forename = StringVar()
        self.__forename_entry = ttk.Entry(self._mainframe, textvariable=self.__forename)
        self.__forename_entry.grid(column=1, row=1, columnspan=2, pady=15, sticky=(W, E))

        self.__forename_label = ttk.Label(self._mainframe, text="Forename", font=(self._textfont, 14))
        self.__forename_label.grid(column=0, row=1)

        self.__surname = StringVar()
        self.__surname_entry = ttk.Entry(self._mainframe, textvariable=self.__surname)
        self.__surname_entry.grid(column=1, row=2, columnspan=2, pady=15, sticky=(W, E))

        self.__surname_label = ttk.Label(self._mainframe, text="Surname", font=(self._textfont, 14))
        self.__surname_label.grid(column=0, row=2)

        self.__postcode = StringVar()
        self.__postcode_entry = ttk.Entry(self._mainframe, textvariable=self.__postcode)
        self.__postcode_entry.grid(column=1, row=3, columnspan=2, pady=15, sticky=(W, E))

        self.__postcode_label = ttk.Label(self._mainframe, text="Postcode", font=(self._textfont, 14))
        self.__postcode_label.grid(column=0, row=3)

        self.__display_PP()

        self.__search_button = ttk.Button(self._mainframe, text="Search", command=self.__search)
        self.__search_button.grid(column=2, row=self.__count, pady=15, sticky=(E))

        self._display_home_button()

    def __display_PP(self):

        self._connect()

        query = """SELECT ParticipationName
        FROM PreferredParticipation;"""

        self.__PP_array = []
        self.__count = 4

        for row in self._cursor.execute(query):

            self.__PP_label = ttk.Label(self._mainframe, text=row[0], font=(self._textfont, 14))
            self.__PP_label.grid(column=0, row=self.__count, columnspan=2, pady=15)

            self.__PP_choice = IntVar()
            self.__PP_checkbutton = ttk.Checkbutton(self._mainframe, variable=self.__PP_choice)
            self.__PP_checkbutton.grid(column=2, row=self.__count)

            self.__PP = {"label": self.__PP_label,
                         "text": row[0],
                         "variable": self.__PP_choice,
                         "button": self.__PP_checkbutton}     # All the values for each of the Preferred Participation buttons are stored as a dictionary
            
            self.__PP_array.append(self.__PP)

            self.__count += 1

        self._close_connection()

    def __display_results(self):

        self.__volunteers = Volunteer_Stack(self.__returned_volunteers)

        self.__result_frame = Result_Frame(self._mainframe, self._textfont)

        self.__next_results()

        self.__show_in_detail_button = ttk.Button(self._mainframe, text="Show More Detail", command=self.__show_in_detail)
        self.__show_in_detail_button.grid(column=1, row=1)

    def __display(self):
        
        try:
            self.__result_frame.reset()
        except:
            pass

        self.__result_frame.display_frame(self.__to_display)

        if self.__volunteers.is_to_see_empty() != True: # Only displays button if user can go forward
            self.__next_button = ttk.Button(self._mainframe, text="Next", command=self.__next_results)
            self.__next_button.grid(column=2, row=0)

        if self.__volunteers.is_seen_empty() != True: # Only displays button if user can go backwards
            self.__back_button = ttk.Button(self._mainframe, text="Back", command=self.__previous_results)
            self.__back_button.grid(column=0, row=0)

    def __next_results(self):
        self.__volunteers.four_forward()
        self.__to_display = self.__volunteers.get_current()
        self.__remove_result_buttons()
        self.__display()

    def __previous_results(self):
        self.__volunteers.four_backward()
        self.__to_display = self.__volunteers.get_current()
        self.__remove_result_buttons()
        self.__display()

    def __remove_result_buttons(self):   # Will remove any buttons that are there
        try:
            self.__back_button.destroy()
        except:
            pass
        try:
            self.__next_button.destroy()
        except:
            pass

    def __add_volunteer(self, row):
        if row[0] in self.__returned_IDs:

            for volunteer in self.__returned_volunteers:
                if volunteer.get_ID() == row[0]:
                    volunteer.add_PP(row[7])

        else:
            self.__volunteer = Volunteer(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            self.__volunteer.add_PP(row[7])
            self.__returned_volunteers.append(self.__volunteer)
            self.__returned_IDs.append(row[0])

    def __search(self):
        self._connect()

        self.__search_for = []   # List for all that 

        if self.__forename.get() != "":
            self.__search_for.append({"type": "Forename", "value": self.__forename.get(), "PP": False})

        if self.__surname.get() != "":
            self.__search_for.append({"type": "Surname", "value": self.__surname.get(), "PP": False})

        if self.__postcode.get() != "":
            self.__search_for.append({"type": "Postcode", "value": self.__postcode.get(), "PP": False})

        for PP in self.__PP_array:
            if PP["variable"].get() == 1:
                self.__search_for.append({"type": PP["text"], "value": PP["variable"].get(), "PP": True})

        self.__command = """SELECT Volunteers.VolunteerID, Volunteers.Forename, Volunteers.Surname, Volunteers.Email, Volunteers.MobileNumber, Volunteers.Address, Volunteers.Postcode, PreferredParticipation.ParticipationName
        FROM Volunteers, PreferredParticipation, ParticipationAssignment
        WHERE""" # start to the SQL query to find volunteers

        for PP in self.__search_for:
            if PP["PP"] == True:
                self.__command += f" PreferredParticipation.ParticipationName = '{PP['type']}' AND"
            else:
                self.__command += f" Volunteers.{PP['type']} = '{PP['value']}' AND"
        
        self.__command += f" Volunteers.VolunteerID = ParticipationAssignment.VolunteerID AND ParticipationAssignment.ParticipationID = PreferredParticipation.ParticipationID;"

        self._cursor.execute(self.__command)
        self.__results = self._cursor.fetchall()

        if len(self.__results) == 0:          # Results in an error when no volunteers are returned
            error_window("No Volunteers Found", "Arial")
        else:
            self.__returned_volunteers = []
            self.__returned_IDs = []

            for row in self.__results:
                self.__add_volunteer(row)

            self._close_connection()

            self._clear_frame()

            self.__display_results()

    def __show_in_detail(self):
        self.__result_frame.reset()

        self.__show_in_detail_button.destroy()
        self.__remove_result_buttons()

        self.__all_volunteers, self.__position = self.__volunteers.get_all()

        self.__show_detail = Detailed_Volunteers(self._mainframe, self._textfont)

        self.__show_detail.display_volunteer(self.__all_volunteers[self.__position])

        self.__show_detailed_buttons()

    def __show_detailed_buttons(self):
        if self.__position != len(self.__all_volunteers)-1:
            self.__next_detail_button = ttk.Button(self._mainframe, text="Next", command=self.__next_detailed)
            self.__next_detail_button.grid(column=2, row=0)

        if self.__position != 0:
            self.__last_detail_button = ttk.Button(self._mainframe, text="Back", command=self.__last_detailed)
            self.__last_detail_button.grid(column=0, row=0)

    def __remove_detailed_buttons(self):
        try:
            self.__next_detail_button.destroy()
        except:
            pass
        try:
            self.__last_detail_button.destroy()
        except:
            pass

    def __next_detailed(self):
        self.__remove_detailed_buttons()
        self.__position += 1
        self.__show_detail.display_volunteer(self.__all_volunteers[self.__position])
        self.__show_detailed_buttons()

    def __last_detailed(self):
        self.__remove_detailed_buttons()
        self.__position -= 1
        self.__show_detail.display_volunteer(self.__all_volunteers[self.__position])
        self.__show_detailed_buttons()


class Result_Frame: # Result frame to display results from volunteer search
    def __init__(self, root_frame, textfont):

        self.__root_frame = root_frame
        self.__textfont = textfont

    def __create_frame(self, root_frame):
        self.__frame = create_frame(root_frame)
        self.__frame.grid(row=0, column=1)

    def reset(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__frame.destroy()

    def display_frame(self, volunteers):

        self.__create_frame(self.__root_frame)

        self.__currently_displayed = []

        self.__name_label = ttk.Label(self.__frame, text="Name", font=(self.__textfont, 12,  "bold"))
        self.__name_label.grid(column=0, row=0, pady=40, padx=40)

        self.__postcode_label = ttk.Label(self.__frame, text="Postcode", font=(self.__textfont, 12, "bold"))
        self.__postcode_label.grid(column=1, row=0, pady=40, padx=40)

        self.__PP_label = ttk.Label(self.__frame, text="Preferred Participation", font=(self.__textfont, 12, "bold"))
        self.__PP_label.grid(column=2, row=0, pady=40, padx=20)

        self.__count = 1
        for value in volunteers:

            name_label = ttk.Label(self.__frame, text=f"{value.get_forename()} {value.get_surname()}", font=self.__textfont)
            name_label.grid(column=0, row=self.__count, pady=40)

            postcode_label = ttk.Label(self.__frame, text=value.get_postcode(), font=self.__textfont)
            postcode_label.grid(column=1, row=self.__count, pady=40)

            PP_string = ""

            for PP in value.get_PP():
                PP_string += f"{PP}\n"

            PP_string = PP_string[0:-1]   # Removes the final \n from the string

            PP_label = ttk.Label(self.__frame, text=PP_string, font=self.__textfont)
            PP_label.grid(column=2, row=self.__count, sticky=W)

            volunteer = {"Name Label": name_label,
                         "Postcode Label": postcode_label,
                         "PP Label": PP_label}

            self.__currently_displayed.append(volunteer)
            self.__count += 1


class Stack: # Stack allowing easy viewing of 
    def __init__(self, array):
        self.__stack = array

    def get_value(self):
        to_return = self.__stack.pop()
        return to_return
    
    def add_value(self, value):
        self.__stack.append(value)

    def is_empty(self):
        if len(self.__stack) == 0:
            empty = True
        else:
            empty = False
        return empty
    
    def get_all(self):
        return self.__stack


class Volunteer_Stack:
    def __init__(self, volunteers):
        self.__to_see = Stack(volunteers)
        self.__seen = Stack([]) # No volunteers have been seen yet so stack starts empty
        self.__not_volunteer = Volunteer(0, "", "", "", "", "", "-")
        self.__not_volunteer.add_PP("")
        self.__current = []

    def __forward(self):
        try:
            value = self.__to_see.get_value()
        except: # This will fill in any empty slots as a dash
            value = self.__not_volunteer
        self.__current.append(value)
    
    def __backward(self):
        value = self.__seen.get_value()
        self.__current.append(value)
    
    def four_forward(self):
        for value in self.__current[::-1]:    # Reversing the appended current array means the volunteers will be added back to the stack in the correct order
            self.__seen.add_value(value)
        self.__current = []
        for i in range(4):
            self.__forward()
    
    def four_backward(self):
        for value in self.__current[::-1]:   # Reversing the appended current array means the volunteers will be added back to the stack in the correct order
            self.__to_see.add_value(value)
        self.__current = []
        for i in range (4):
            self.__backward()
    
    def get_current(self):
        return self.__current
    
    def get_all(self):
        seen = self.__seen.get_all()
        to_see = self.__to_see.get_all()
        position = len(seen)
        volunteer_array = []
        for volunteer in seen[::-1]:
            volunteer_array.append(volunteer)
        for volunteer in self.__current:
            volunteer_array.append(volunteer)
        for volunteer in to_see[::-1]:
            volunteer_array.append(volunteer)
        return volunteer_array, position
    
    def is_seen_empty(self):
        return self.__seen.is_empty()
    
    def is_to_see_empty(self):
        return self.__to_see.is_empty()


class Detailed_Volunteers:
    def __init__(self, root_frame, textfont):
        self.__root_frame = root_frame
        self.__textfont = textfont
        self.__create_frame()

    def __create_frame(self):
        self.__frame = create_frame(self.__root_frame)
        self.__frame.grid(row=0, column=1)

    def __reset_frame(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()

    def display_volunteer(self, volunteer):

        self.__reset_frame()

        self.__name_label = ttk.Label(self.__frame, text=f"{volunteer.get_forename()} {volunteer.get_surname()}", font=(self.__textfont, 16, "bold"))
        self.__name_label.grid(column=1, row=0, pady=10)

        self.__email_label = ttk.Label(self.__frame, text=f"{volunteer.get_email()}", font=self.__textfont)
        self.__email_label.grid(column=1, row=1, pady=5)

        self.__number_label = ttk.Label(self.__frame, text=f"{volunteer.get_mobilenumber()}", font=self.__textfont)
        self.__number_label.grid(column=1, row=2, pady=5)

        self.__address_label = ttk.Label(self.__frame, text=f"{volunteer.get_address()}", font=self.__textfont)
        self.__address_label.grid(column=1, row=3, pady=5)

        self.__postcode_label = ttk.Label(self.__frame, text=f"{volunteer.get_postcode()}", font=self.__textfont)
        self.__postcode_label.grid(column=1, row=4, pady=5)

        self.__PreferredParticipation_label = ttk.Label(self.__frame, text="Preferred Participation", font=(self.__textfont, 16, "bold"))
        self.__PreferredParticipation_label.grid(column=1, row=5, pady=10)

        PP_array = volunteer.get_PP()

        self.__PP = []

        for i in range (0, len(PP_array)):
            PP_label = ttk.Label(self.__frame, text=f"{PP_array[i]}", font=self.__textfont)
            PP_label.grid(column=1, row=i+6, pady=2)
            PP = {"Label": PP_label,
                  "text": PP_array[i]}
            self.__PP.append(PP)


class Preferred_Participation_Settings_Page(Page):
    def __init__(self, window, textfont):
        super().__init__(window, textfont, "Preferred Participation Settings")
        self._create_frame()

        self.__display_page()

    def __display_page(self):
        self._display_title("Preferred Participation")
        self._page_title.grid(column=0, row=0, columnspan=3, pady=40)

        self.__display_PP()

        self.__add_new = ttk.Button(self._mainframe, text="Add New Preferred Participation", command=self.__add_new_PP)
        self.__add_new.grid(column=0, row=self.__count, columnspan=3, sticky=(W, E))

        self._display_home_button()

    def __display_PP(self):
        
        self._connect()

        query = """SELECT ParticipationName
        FROM PreferredParticipation;"""

        self.__PP_array = []
        self.__count = 1

        self._cursor.execute(query)
        self.__results = self._cursor.fetchall()

        for row in self.__results:

            PP_label = ttk.Label(self._mainframe, text=row[0], font=(self._textfont, 14))
            PP_label.grid(column=0, row=self.__count, columnspan=2, pady=15)
            
            PP_delete_button = ttk.Button(self._mainframe, text="Delete", command=lambda to_delete=row[0]: self.__delete_PP(to_delete))
            PP_delete_button.grid(column=2, row=self.__count)
            
            PP = {"label": PP_label,
                  "text": row[0],
                  "button": PP_delete_button}     # All the values for each of the Preferred Participation buttons are stored as a dictionary

            self.__PP_array.append(PP)

            self.__count += 1

        self._close_connection()

    def __delete_PP(self, to_delete):
        self._connect()
        for PP in self.__PP_array:
            if PP["text"] == to_delete:
                query = f"SELECT ParticipationID FROM PreferredParticipation WHERE ParticipationName = '{PP['text']}'"
                self._cursor.execute(query)
                to_remove_ID, = self._cursor.fetchone()
                self.__remove_from_ParticipationAssignment(to_remove_ID) # Delete any users connected to PP before deleting PP
                self.__remove_PP(to_remove_ID)
        self._SQLiteConnection.commit()
        self._clear_frame()
        self.__display_page()

    def __remove_from_ParticipationAssignment(self, PP_ID):
        delete_command = f"DELETE FROM ParticipationAssignment WHERE ParticipationID={PP_ID}"
        self._cursor.execute(delete_command)

    def __remove_PP(self, PP_ID):
        remove_command = f"DELETE FROM PreferredParticipation WHERE ParticipationID={PP_ID}"
        self._cursor.execute(remove_command)

    def __add_new_PP(self):
        self._clear_frame()
        self._display_title("Add New")
        self._page_title.grid(column=0, row=0, columnspan=3, pady=40)

        self.__name_label = ttk.Label(self._mainframe, text="Title", font=(self._textfont, 14))
        self.__name_label.grid(column=1, row=1)

        self.__new_name = StringVar()
        self.__name_entry = ttk.Entry(self._mainframe, textvariable=self.__new_name)
        self.__name_entry.grid(column=0, row=2, columnspan=3)

        self.__description_label = ttk.Label(self._mainframe, text="Description", font=(self._textfont, 14))
        self.__description_label.grid(column=1, row=3)

        self.__new_description = StringVar()
        self.__description_entry = ttk.Entry(self._mainframe, textvariable=self.__new_description, width=80)
        self.__description_entry.grid(column=0, row=4, columnspan=3)

        self.__save_button = ttk.Button(self._mainframe, text="Save", command=self.__add_to_db)
        self.__save_button.grid(column=0, row=5, columnspan=3, pady=10, sticky=E)

    def __add_to_db(self):

        self._connect()

        query = "SELECT ParticipationID FROM PreferredParticipation"
        self._cursor.execute(query)
        results = self._cursor.fetchall()
        last_ID = 0
        found = False
        for row in results:
            to_check, = row  # Splits the returned tuple
            if to_check != last_ID + 1 and found == False:
                new_ID = last_ID + 1
                found = True
            last_ID = to_check
        if found == False:
            new_ID = last_ID + 1

        command = f"INSERT INTO PreferredParticipation (ParticipationID, ParticipationName, ParticipationDescription) VALUES ({new_ID}, '{self.__new_name.get()}', '{self.__new_description.get()}')"
        self._cursor.execute(command)
        self._SQLiteConnection.commit()

        self._close_connection()

        self._clear_frame()
        self.__display_page()


class Event_Settings_Page(Page):
    def __init__(self, window, textfont):
        super().__init__(window, textfont, "Event Settings")

        self._create_frame()

        self.__display_page()

    def __display_page(self):
        
        self._display_title("Event")
        self._page_title.grid(column=0, row=0, columnspan=3, pady=40)

        self.__display_events()
        
        self.__add_new = ttk.Button(self._mainframe, text="Add New Event", command=self.__add_new_event)
        self.__add_new.grid(column=0, row=self.__count, columnspan=3, sticky=(W, E))

        self._display_home_button()

    def __display_events(self):
        self._connect()

        query = """SELECT EventName
        FROM Events;"""

        self.__event_array = []
        self.__count = 1

        for row in self._cursor.execute(query):

            event_label = ttk.Label(self._mainframe, text=row[0], font=(self._textfont, 14))
            event_label.grid(column=0, row=self.__count, columnspan=2, pady=15)

            event_delete_button = ttk.Button(self._mainframe, text="Delete", command=lambda to_delete=row[0]: self.__delete_event(to_delete))
            event_delete_button.grid(column=2, row=self.__count)

            event = {"label": event_label,
                     "text": row[0],
                     "delete button": event_delete_button}     # All the values for each of the Preferred Participation buttons are stored as a dictionary
            
            self.__event_array.append(event)

            self.__count += 1

        self._close_connection()

    def __add_new_event(self):
        self._clear_frame()
        self._display_title("Add New")
        self._page_title.grid(column=0, row=0, columnspan=2, pady=40, padx=70)

        self.__name_label = ttk.Label(self._mainframe, text="Title", font=(self._textfont, 14))
        self.__name_label.grid(column=0, row=1)

        self.__new_name = StringVar()
        self.__name_entry = ttk.Entry(self._mainframe, textvariable=self.__new_name)
        self.__name_entry.grid(column=1, row=1, sticky=(W, E))

        self.__date_label = ttk.Label(self._mainframe, text="Date", font=(self._textfont, 14))
        self.__date_label.grid(column=0, row=2)

        self.__new_date = StringVar()
        self.__date_entry = ttk.Entry(self._mainframe, textvariable=self.__new_date)
        self.__date_entry.grid(column=1, row=2, sticky=(W, E))

        self.__time_label = ttk.Label(self._mainframe, text="Time", font=(self._textfont, 14))
        self.__time_label.grid(column=0, row=3)

        self.__new_time = StringVar()
        self.__time_entry = ttk.Entry(self._mainframe, textvariable=self.__new_time)
        self.__time_entry.grid(column=1, row=3, sticky=(W, E))

        self.__address_label = ttk.Label(self._mainframe, text="Address", font=(self._textfont, 14))
        self.__address_label.grid(column=0, row=4)

        self.__new_address = StringVar()
        self.__address_entry = ttk.Entry(self._mainframe, textvariable=self.__new_address)
        self.__address_entry.grid(column=1, row=4, sticky=(W, E))

        self.__postcode_label = ttk.Label(self._mainframe, text="Postcode", font=(self._textfont, 14))
        self.__postcode_label.grid(column=0, row=5)

        self.__new_postcode = StringVar()
        self.__postcode_entry = ttk.Entry(self._mainframe, textvariable=self.__new_postcode)
        self.__postcode_entry.grid(column=1, row=5, sticky=(W, E))

        self.__save_button = ttk.Button(self._mainframe, text="Save", command=self.__add_to_db)
        self.__save_button.grid(column=0, row=6, columnspan=2, pady=10, sticky=E)

    def __delete_event(self, to_delete):
        self._connect()
        for PP in self.__event_array:
            if PP["text"] == to_delete:
                query = f"SELECT EventID FROM Events WHERE EventName = '{PP['text']}'"
                self._cursor.execute(query)
                to_remove_ID, = self._cursor.fetchone()
                self.__remove_from_EventAssignment(to_remove_ID) # Delete any users connected to PP before deleting PP
                self.__remove_event(to_remove_ID)
        self._SQLiteConnection.commit()
        self._clear_frame()
        self.__display_page()

    def __remove_from_EventAssignment(self, event_ID):
        delete_command = f"DELETE FROM EventAssignment WHERE EventID={event_ID}"
        self._cursor.execute(delete_command)

    def __remove_event(self, event_ID):
        remove_command = f"DELETE FROM Events WHERE EventID={event_ID}"
        self._cursor.execute(remove_command)

    def __add_to_db(self):
        
        self._connect()

        query = "SELECT EventID FROM Events"
        self._cursor.execute(query)
        results = self._cursor.fetchall()
        greatest_ID = 0
        for row in results:
            to_check, = row  # Splits the returned tuple
            if to_check > greatest_ID:
                greatest_ID = to_check

        command = f"INSERT INTO Events (EventID, EventName, Date, Time, Address, Postcode) VALUES ({greatest_ID+1}, '{self.__new_name.get()}', '{self.__new_date.get()}', '{self.__new_time.get()}', '{self.__new_address.get()}', '{self.__new_postcode.get()}')"
        self._cursor.execute(command)
        self._SQLiteConnection.commit()

        self._close_connection()

        self._clear_frame()
        self.__display_page()

window = setup(background_colour, button_background_colour, button_text_colour, label_text_colour, text_box_text_colour, tex_box_background_colour, active_button_background_colour)
password_page(window, text_font)
window.mainloop()
