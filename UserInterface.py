import tkinter as tk
import time
#import nltk
#nltk.download('punkt')

from nltk import sent_tokenize

from Controller import Controller
from Settings import *
from EyeTracking import start_eye_tracking


# Styles
TITLE_FONT_STYLE = ("David", 28, "bold")
SUBTITLE_FONT_STYLE = ("David", 24, "bold")
TEXT_FONT = ("David", 20)
TEXT_FONT_BOLD = ("David", 20, "bold")
QUESTION_TEXT_FONT = ("David", 18)
QUESTION_TEXT_FONT_BOLD = ("David", 18, "bold")
STATUSBAR_FONT = ("David", 16)
BUTTON_FONT_STYLE = ("David", 20, "bold")
TITLE_FONT_COLOR = 'DarkBlue'
BACKGROUND_COLOR = "azure2"

# Main controller
controller = Controller()

# Texts
texts = []
current_text_id = ""
current_text = ""
current_text_title = ""
current_text_questions = []
current_text_answers = []
current_text_correct_answers = []
next_text = 1

# User Results (Per text)
highlighted_sentences = []
highlighted_sentences_scores = []
text_summary = ""
questions_answers = []
timer_text_reading = 0
timer_text_summarization = 0
timer_highlighting = 0
timer_ranking = 0
timer_q1 = 0
timer_q2 = 0
timer_q3 = 0
participant_id = 0

# Demo / Experiment
demo = False

statusbar = ""

# For controlling opened popups
opened_popups = []

ranking_closed_illegaly = False

# Initiate texts
def init_texts():
    global texts, current_text_id, current_text, current_text_questions, current_text_answers, next_text, demo, current_text_title, current_text_correct_answers
    if demo:
        print("demo")
        texts = controller.get_demo_texts()
        print(texts)
    else:
        texts = controller.get_texts()

    current_text_id = texts[0]["ID"]
    current_text = texts[0]["Text"]
    current_text_questions = [texts[0]["Q1"], texts[0]["Q2"], texts[0]["Q3"]]
    current_text_answers = [texts[0]["Q1A1"], texts[0]["Q1A2"], texts[0]["Q1A3"], texts[0]["Q1A4"],
                            texts[0]["Q2A1"], texts[0]["Q2A2"], texts[0]["Q2A3"], texts[0]["Q2A4"],
                            texts[0]["Q3A1"], texts[0]["Q3A2"], texts[0]["Q3A3"], texts[0]["Q3A4"]]
    current_text_correct_answers = [texts[0]["Q1C"], texts[0]["Q2C"], texts[0]["Q3C"]]
    current_text_title = texts[0]["Title"]

    next_text = 1


# Initiate next text
def init_next_text():
    global texts, current_text_id, current_text, current_text_questions, current_text_answers, next_text, current_text_title, current_text_correct_answers
    current_text_id = texts[next_text]["ID"]
    current_text = texts[next_text]["Text"]
    current_text_questions = [texts[next_text]["Q1"], texts[next_text]["Q2"], texts[next_text]["Q3"]]
    current_text_answers = [texts[next_text]["Q1A1"], texts[next_text]["Q1A2"], texts[next_text]["Q1A3"], texts[next_text]["Q1A4"], texts[next_text]["Q2A1"],
                            texts[next_text]["Q2A2"], texts[next_text]["Q2A3"], texts[next_text]["Q2A4"], texts[next_text]["Q3A1"], texts[next_text]["Q3A2"],
                            texts[next_text]["Q3A3"], texts[next_text]["Q3A4"]]
    current_text_correct_answers = [texts[next_text]["Q1C"], texts[next_text]["Q2C"], texts[next_text]["Q3C"]]

    current_text_title = texts[next_text]["Title"]

    next_text += 1


# Clear the user's results
def clear_user_results():
    global highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, timer_text_reading, timer_text_summarization, timer_highlighting, timer_ranking, timer_q1, timer_q2, timer_q3
    highlighted_sentences = []
    highlighted_sentences_scores = []
    text_summary = ""
    questions_answers = []
    timer_text_reading = 0
    timer_text_summarization = 0
    timer_highlighting = 0
    timer_ranking = 0
    timer_q1 = 0
    timer_q2 = 0
    timer_q3 = 0

# Save user results
def save_results():
    global questions_answers

    questions_answers = [int(elem) for elem in questions_answers]
    questions_answers_final = []

    for i in range(len(questions_answers)):
        if questions_answers[i] == current_text_correct_answers[i]:
            questions_answers_final.append(str(questions_answers[i]) + "C")
        else:
            questions_answers_final.append(str(questions_answers[i]) + "W")

    if not demo:
        times = [timer_text_reading, timer_text_summarization, timer_highlighting, timer_ranking, timer_q1, timer_q2, timer_q3]
        controller.save_text_results(current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers_final, times)

opened_ranking_popup = False
ranking_var = ""


def on_close(win):
    pass


ranking_dict = {
    1: "normal",
    2: "normal",
    3: "normal",
    4: "normal",
    5: "normal",
}
def ranking_popup():
    global opened_ranking_popup, ranking_var
    ranking_var = tk.IntVar()

    if opened_ranking_popup is False:
        win = tk.Toplevel()
        win.wm_title("Ranking")
        win.configure(bg=BACKGROUND_COLOR)
        win.protocol("WM_DELETE_WINDOW", lambda w = win: on_close(w))

        # Popup size
        popup_width = 150
        popup_height = 300

        # Center the popup
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x_coordinate = int((screen_width) - (popup_width))
        y_coordinate = int((screen_height / 2) - (popup_height / 2))
        win.geometry("{}x{}+{}+{}".format(popup_width, popup_height, x_coordinate, y_coordinate))

        new_title(win, "Ranking")

        ranking_buttons = []

        for i in range(1, 6):
            btn = tk.Button(win, text=str(i), bg=BACKGROUND_COLOR, font=("David", 14, "bold"))
            btn["state"] = ranking_dict[i]
            btn.configure(command=lambda val=i: ranking_var.set(val))
            btn.pack()
            ranking_buttons.append(btn)


        opened_ranking_popup = True
        btn.wait_variable(ranking_var)

        win.destroy()
        opened_ranking_popup = False

        return ranking_var.get()


def error_popup(content, justify="left"):
    for w in opened_popups:
        if w is None:
            opened_popups.remove(w)
        else:
            w.destroy()
            w = None

    win = tk.Toplevel()
    win.wm_title("Error!")
    win.configure(bg=BACKGROUND_COLOR)

    # Popup size
    popup_width = 400
    popup_height = 200

    # Center the popup
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (popup_width / 2))
    y_coordinate = int((screen_height / 2) - (popup_height / 2))
    win.geometry("{}x{}+{}+{}".format(popup_width, popup_height, x_coordinate, y_coordinate))

    new_title(win, "Error")
    tk.Label(win, text=content, bg=BACKGROUND_COLOR, justify=justify).pack()

    opened_popups.append(win)

# Open a custom popup
def popup(title, content, justify="left"):
    for w in opened_popups:
        if w is None:
            opened_popups.remove(w)
        else:
            w.destroy()
            w = None

    win = tk.Toplevel()
    win.wm_title(title)
    win.configure(bg=BACKGROUND_COLOR)

    # Popup size
    popup_width = 700
    popup_height = 400

    # Center the popup
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (popup_width / 2))
    y_coordinate = int((screen_height / 2) - (popup_height / 2))
    win.geometry("{}x{}+{}+{}".format(popup_width, popup_height, x_coordinate, y_coordinate))

    new_title(win, title)
    tk.Label(win, text=content, bg=BACKGROUND_COLOR, justify=justify).pack()

    opened_popups.append(win)

# Adds new title to frame
def new_title(frame, title):
    title = tk.Label(frame, text=title, fg=TITLE_FONT_COLOR, font=TITLE_FONT_STYLE, bg=BACKGROUND_COLOR)
    title.pack(side="top", fill="x", pady=10)
    return title

# Adds new button to frame
def new_button(frame, btn_text, btn_command):
    btn = tk.Button(frame, text=btn_text, command=btn_command, fg="white", bg="darkblue", font=BUTTON_FONT_STYLE)
    return btn

# Adds new sub title to frame
def new_subtitle(frame, subtitle):
    lbl = tk.Label(frame, text=subtitle, fg=TITLE_FONT_COLOR, font=SUBTITLE_FONT_STYLE, bg=BACKGROUND_COLOR)
    return lbl

# Checks if num is a positive number
def is_positive_number(num):
    try:
        return int(num) > 0
    except:
        return False


# Main app
class TextSummarizationApp(tk.Tk):

    def __init__(self):
        global statusbar
        self.tk = tk.Tk()
        self.tk.attributes("-fullscreen", True)
        self.tk.configure(bg=BACKGROUND_COLOR)

        # Menu bar
        menu_bar = tk.Menu(self)
        #menu_bar.add_command(label="Main", command=lambda: self.switch_frame(MainFrame))
        menu_bar.add_command(label="Instructions", command=self.popup_instructions)
        menu_bar.add_command(label="Contact", command=self.popup_contact)
        menu_bar.add_command(label="About", command=self.popup_about)
        menu_bar.add_command(label="Exit", command=self.tk.destroy)
        self.tk.configure(menu=menu_bar)

        statusbar = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=STATUSBAR_FONT)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)


        self.current_frame = None
        self.switch_frame(MainFrame)

    # Popups instructions
    def popup_instructions(self):
        instructions_string = "This experiment contains 5 stages:\n\n" \
                              "1.\tText Reading - Reading a short text in English\n\n" \
                              "2.\tText Summarization - Summarize the text in own words,between 3-5 sentences seperated by new line\n\n" \
                              "3.\tHighlighting - Highlight 5 important sentences in the text\n\n" \
                              "4.\tRanking - Rank the 5 highlighted sentences from the text\n\n" \
                              "5.\tQuestions - Answer 3 multiple choice questions for each text\n\n\n\n" \
                              "There are 4 texts total.\n\n" \
                              "The 5 stages must be repeated for each text."

        popup("Instructions", instructions_string)

    # Popups contact
    def popup_contact(self):
        contact_string = "Project Managers:\n\n" \
                         "\tDr. Meirav Maimom\t\tmeiravta@bgu.ac.il\n\n" \
                         "\tProf. Mark Last\t\t\tmlast@bgu.ac.il\n\n\n\n" \
                         "Masterant:\n\n" \
                         "\tAleksandr Romanovskii\t\tromaleks@post.bgu.ac.il\n\n\n\n" \
                         "Project Members:\n\n" \
                         "\tIdo Kestenbaum\t\t\tidokest@post.bgu.ac.il\n\n" \
                         "\tMatan Shushan\t\t\tmatanshu@post.bgu.ac.il\n\n" \
                         "\tAdir Biran\t\t\tadir.biran@gmail.com\n\n"

        popup("Contact", contact_string)

    # Popups about
    def popup_about(self):
        about_string = "This system was created for a Text Summarization experiment.\n\n" \
                       "In this experiment we will collect eye-tracking data while the participants read and interact with texts.\n\n" \
                       "This data will be used to create a text summarization model based on natural interaction of the user with the text.\n\n" \
                       "SISE\n" \
                       "December 2020\n\n"

        popup("About", about_string)

    # Switching frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()


# Main Frame
class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, APP_NAME).pack(side="top", fill="x", pady=10)

        # Introduction
        intro = "Welcome to " + APP_NAME + "!\n\n" \
                "A text summarization experiment based on the eye-movements of the participants\n" \
                "The experiment is estimated to take between 1-1.5 hours.\n\n\n" \
                "In this experiment there are 5 steps:\n" \
                "\t1. Read a short text\n" \
                "\t2. Summarize the text\n" \
                "\t3. Highlight important sentences in the text\n" \
                "\t4. Rank the highlighted sentences\n" \
                "\t5. Answer 3 multiple choice questions\n\n" \
                "These 5 steps will be repeated for each of the 4 texts in the experiment.\n"

        tk.Label(self, text=intro, bg=BACKGROUND_COLOR, font=TEXT_FONT, justify="left").pack(pady=50)

        # Start button
        new_button(self, "Start", self.start).pack()

    # Starting the app
    def start(self):
        self.master.switch_frame(NewParticipantFrame)

# New Participant frame
class NewParticipantFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "New Participant")

        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # String Variables
        self.id_var = tk.StringVar(self)
        self.first_name_var = tk.StringVar(self)
        self.last_name_var = tk.StringVar(self)
        self.age_var = tk.StringVar(self)
        self.gender_var = tk.StringVar(self)
        self.gender_var.set("Select")
        self.department_var = tk.StringVar(self)
        self.department_var.set("Select")

        # Just for tests
        # self.id_var.set("123456789")
        # self.first_name_var.set("Demo")
        # self.last_name_var.set("Demo")
        # self.age_var.set("30")
        # self.gender_var.set("Male")
        # self.department_var.set("Software Engineering")

        # Sizes
        pad_x, pad_y = 40, 20
        entry_width = 30

        # ID
        tk.Label(inner_frame, text="ID", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=0, column=0, sticky="w")
        tk.Entry(inner_frame, width=entry_width, textvariable=self.id_var, font=TEXT_FONT).grid(row=0, column=1, padx=pad_x, pady=pad_y)
        self.id_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.id_error.grid(row=0, column=2)

        # First Name
        tk.Label(inner_frame, text="First Name", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=1, column=0, sticky="w")
        tk.Entry(inner_frame, width=entry_width, textvariable=self.first_name_var, font=TEXT_FONT).grid(row=1, column=1, padx=pad_x, pady=pad_y)
        self.first_name_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.first_name_error.grid(row=1, column=2)

        # Last Name
        tk.Label(inner_frame, text="Last Name", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=2, column=0, sticky="w")
        tk.Entry(inner_frame, width=entry_width, textvariable=self.last_name_var, font=TEXT_FONT).grid(row=2, column=1, padx=pad_x, pady=pad_y)
        self.last_name_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.last_name_error.grid(row=2, column=2)

        # Gender
        tk.Label(inner_frame, text="Gender", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=3, column=0, sticky="w")
        gender_menu = tk.OptionMenu(inner_frame, self.gender_var, "Select", "Male", "Female")
        gender_menu.config(font=TEXT_FONT, bg=BACKGROUND_COLOR)
        gen_menu = self.nametowidget(gender_menu.menuname)
        gen_menu.config(font=TEXT_FONT)
        gender_menu.grid(row=3, column=1, padx=pad_x, pady=pad_y)
        self.gender_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.gender_error.grid(row=3, column=2)

        # Department
        tk.Label(inner_frame, text="Department", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=4, column=0, sticky="w")
        department_menu = tk.OptionMenu(inner_frame, self.department_var, "Select", "Information Systems Engineering", "Software Engineering")
        department_menu.config(font=TEXT_FONT, bg=BACKGROUND_COLOR)
        dep_menu = self.nametowidget(department_menu.menuname)
        dep_menu.config(font=TEXT_FONT)
        department_menu.grid(row=4, column=1, padx=pad_x, pady=pad_y)
        self.department_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.department_error.grid(row=4, column=2)


        # Age
        tk.Label(inner_frame, text="Age", font=TEXT_FONT, bg=BACKGROUND_COLOR, justify="left").grid(row=5, column=0, pady=pad_y, sticky="w")
        tk.Entry(inner_frame, width=entry_width, textvariable=self.age_var, font=TEXT_FONT).grid(row=5, column=1, padx=pad_x, pady=pad_y)
        self.age_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.age_error.grid(row=5, column=2)

        # Continue Button
        new_button(inner_frame, "Continue", self.new_participant).grid(row=6, column=1, pady=(pad_y, 100))

        inner_frame.pack(anchor="s", side="bottom")

    # Adds new participant
    def new_participant(self):

        # Clean Error Labels
        self.id_error['text'] = ""
        self.first_name_error['text'] = ""
        self.last_name_error['text'] = ""
        self.gender_error['text'] = ""
        self.age_error['text'] = ""
        self.department_error['text'] = ""

        # Form Inputs
        id = self.id_var.get().strip()
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        gender = self.gender_var.get().strip()
        department = self.department_var.get().strip()
        age = self.age_var.get().strip()

        valid = True

        # ID Check
        if id == "":
            self.id_error['text'] = "ID is empty"
            valid = False
        elif not is_positive_number(id):
            self.id_error['text'] = "ID must be positive number"
            valid = False

        # First Name Check
        if first_name == "":
            self.first_name_error['text'] = "First Name is empty"
            valid = False

        # Last Name Check
        if last_name == "":
            self.last_name_error['text'] = "Last Name is empty"
            valid = False

        # Gender Check
        if gender == "Select":
            self.gender_error['text'] = "Gender is not chosen"
            valid = False

        # Department Check
        if department == "Select":
            self.department_error['text'] = "Department is not chosen"
            valid = False

        # Age Check
        if age == "":
            self.age_error['text'] = "Age is empty"
            valid = False
        elif not is_positive_number(age):
            self.age_error['text'] = "Age must be positive number"
            valid = False

        # All fields are valid
        if valid:
            global participant_id
            participant_id = id
            controller.add_new_participant(id, first_name, last_name, gender, department, age)
            init_texts()
            self.master.switch_frame(TextReadingInstructions)

# Demo / Experiment Frame
class DemoExperimentFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Demo / Experiment")

        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        pad_x, pad_y = 100, 50

        # Demo label
        demo_label = new_subtitle(self.inner_frame, "Demo")
        demo_label.grid(row=0, column=0, pady=pad_y)

        # Experiment label
        experiment_label = new_subtitle(self.inner_frame, "Experiment")
        experiment_label.grid(row=0, column=1, pady=pad_y, padx=pad_x)

        # Demo Description
        demo_label_description = tk.Label(self.inner_frame, text="Trying the system for 1 demo text", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        demo_label_description.grid(row=1, column=0, pady=pad_y, padx=pad_x)

        # Experiment Description
        experiment_label_description = tk.Label(self.inner_frame, text="Starting the experiment", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        experiment_label_description.grid(row=1, column=1, pady=pad_y, padx=pad_x)

        # Demo Button
        demo_button = new_button(self.inner_frame, "Start Demo", self.start_demo)
        demo_button.grid(row=2, column=0, pady=(pad_y, 400), padx=pad_x)

        # Experiment Button
        experiment_button = new_button(self.inner_frame, "Start Experiment", self.start_experiment)
        experiment_button.grid(row=2, column=1, pady=(pad_y, 400), padx=pad_x)

        self.inner_frame.pack(side="bottom")

    # Starting demo mode
    def start_demo(self):
        global demo
        demo = True
        init_texts()
        self.master.switch_frame(TextReadingInstructions)

    def start_experiment(self):
        init_texts()
        self.master.switch_frame(TextReadingInstructions)


# Text Reading Instructions
class TextReadingInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Text Reading Instructions")

        instructions = "In this step, you will have to read a short text.\n\nThis step has a minimum time of " + str(int(MIN_TEXT_READING_TIME/60)) + " minutes.\n\nBy the end of the time the Next button will appear on the bottom-right side."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=100)
        new_button(self, "Click here to continue", self.start_reading_text).pack()


    # Start text reading
    def start_reading_text(self):
        global timer_text_reading
        self.master.switch_frame(TextSummarizationInstructions)

        global statusbar, current_text_title, current_text_id
        statusbar["text"] = "Text: " + str(current_text_id) + ", " + current_text_title

        timer_text_reading = start_eye_tracking(current_text, participant_id, current_text_id, current_text_title)

# Text Summarizing Instructions
class TextSummarizationInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Text Summarizing Instructions")

        instructions = "In this step, you will have to summarize the text you read in the last step in your own words.\n\nThe summarization length's is between 3-5 sentences, seperated by new line (Enter)."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=100)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(TextSummarizationFrame)).pack()


# Text Summarization Frame
class TextSummarizationFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Start time for timer
        self.start_time = time.time()

        new_title(self, "Text Summarization")

        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # Text box
        self.user_text_summary = tk.Text(self.inner_frame, height="20", width="100", font=TEXT_FONT)
        self.user_text_summary.grid(row=1, column=0)

        self.words_count = tk.IntVar()
        self.words_count.set(0)

        # Next button
        self.words_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        self.words_count_lbl = tk.Label(self.words_frame, text="Words Count:", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        self.words_count_lbl.pack(side="left")
        self.counter = tk.Label(self.words_frame, textvariable=self.words_count, bg=BACKGROUND_COLOR, font=TEXT_FONT)
        self.counter.pack(side="left")

        self.words_count_error = tk.Label(self.words_frame, text="", fg="red", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        self.words_count_error.pack(side="right")

        next_btn = new_button(self.inner_frame, btn_text="Next", btn_command=self.next)
        next_btn.grid(row=3, column=0, pady=20)


        self.inner_frame.pack(side="bottom")
        self.words_frame.pack(side="left", fill="x")

        self.update_words_counter()

    def update_words_counter(self):
        text_summary = self.user_text_summary.get("1.0", 'end-1c')
        text_split = [elem for elem in text_summary.strip().split("\n") if len(elem) > 0]

        self.words_count.set(len(text_split))

        self.words_count_lbl["text"] = "Sentences Count:"

        self.words_count_error["text"] = ""

        self.after(2000, self.update_words_counter)

    # Next button
    def next(self):
        global text_summary, timer_text_summarization
        text_summary = self.user_text_summary.get("1.0", 'end-1c')
        text_split = [elem for elem in text_summary.strip().split("\n") if len(elem) > 0]

        self.words_count.set(len(text_split))
        if self.words_count.get() >= 3 and self.words_count.get() <= 5:
            timer_text_summarization = round(time.time() - self.start_time, 1)
            self.words_count_error["text"] = ""
            self.master.switch_frame(HighlightingInstructions)
        else:
            self.words_count.set("")
            self.words_count_lbl["text"] = ""
            self.words_count_error["text"] = "Summarization is not between 3 and 5 sentences"
            #self.master.switch_frame(HighlightingInstructions)


# Highlighting Instructions
class HighlightingInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Highlighting Instructions")

        instructions = "In this step, you will have to highlight the 5 most important sentences from the text.\n\nThen you have to rank the highlighted sentences between 1-5."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=100)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(HighlightingFrame)).pack()


# Highlighting Frame
class HighlightingFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        self.title = tk.Label(self, text="Highlighting", fg=TITLE_FONT_COLOR, font=TITLE_FONT_STYLE, bg=BACKGROUND_COLOR)
        self.title.pack(side="top", fill="x", pady=10)


        # Start time for timer
        self.start_time = time.time()

        # Current text's sentences
        # sentences = current_text.split(".")
        sentences = sent_tokenize(current_text)

        # Mapping buttons (words) to clusters (sentences)
        self.buttons_mapping = {}
        self.buttons = []

        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.buttons_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        btn_cluster = 0

        # Foreach sentence in text
        for sentence in sentences:

            sentence += "."

            # All words in sentence
            words = sentence.split(" ")
            words = list(filter(lambda x: x.strip() != "", words))

            # Foreach word in sentence
            for word in words:

                word_btn = tk.Button(self.buttons_frame, text=word, bg=BACKGROUND_COLOR)
                word_btn.configure(command=lambda btn=word_btn: self.change_color(btn))
                word_btn.config(highlightthickness=0, borderwidth=0)
                self.buttons.append(word_btn)
                self.buttons_mapping[word_btn] = btn_cluster

            rank_btn = tk.Button(self.buttons_frame, text="", bg=BACKGROUND_COLOR)
            self.buttons.append(rank_btn)
            self.buttons_mapping[rank_btn] = btn_cluster

            # All words from same sentence relate to same cluster
            btn_cluster += 1

        frame_width = self.winfo_screenwidth() * 0.7
        current_width = 0

        # Temp frame for each set of buttons
        tmp_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        i = 0

        # Foreach button (word)
        for btn in self.buttons:

            # Gets button's width
            btn.update_idletasks()
            btn_width = btn.winfo_reqwidth()

            # Copy button to another frame
            if btn['text'] == "":
                btn_replicate = tk.Button(tmp_frame, text=btn["text"], bg=BACKGROUND_COLOR, font=("David", 13, "underline", "bold"))
            else:
                btn_replicate = tk.Button(tmp_frame, text=btn["text"], bg=BACKGROUND_COLOR, font=("David", 13))
            btn_replicate.configure(command=lambda btn=btn_replicate: self.change_color(btn))
            btn_replicate.config(highlightthickness=0, borderwidth=0)



            if i == 0:
                btn_replicate["text"] = "\t" + btn_replicate["text"]
                i = -1

            # If button fits to same line
            if current_width + btn_width < frame_width and btn_replicate["text"] != "@@":
                btn_replicate.pack(side="left")

            # Button fits to another line
            else:
                if btn_replicate["text"] == "@@":
                    btn_replicate["text"] = "\t"

                tmp_frame.pack(side="top", anchor="w", pady=3)
                tmp_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
                current_width = 0

                btn_replicate = tk.Button(tmp_frame, text=btn_replicate["text"], bg=BACKGROUND_COLOR, font=("David", 13))
                btn_replicate.configure(command=lambda btn_passed=btn_replicate: self.change_color(btn_passed))
                btn_replicate.config(highlightthickness=0, borderwidth=0)
                btn_replicate.pack(side="left")

            # Update data structures
            cl = self.buttons_mapping[btn]
            del self.buttons_mapping[btn]
            self.buttons_mapping[btn_replicate] = cl

            # Advancing current width
            current_width += btn_width + 4

        tmp_frame.pack(side="top", anchor="w", pady=5)

        # Next button
        self.next_btn = new_button(self.inner_frame, btn_text="Start Ranking", btn_command=self.start_ranking)
        self.next_btn.grid(row=btn_cluster+1, column=0, pady=20)
        self.buttons_frame.pack(side="top")
        self.inner_frame.pack(side="bottom")

    def start_ranking(self):
        buttons = [btn for btn in self.buttons_mapping]
        existed_clusters = []

        for btn in buttons:
            if btn["bg"] == HIGHLIGHTED_COLOR:

                # Current button's cluster
                cl = self.buttons_mapping[btn]

                # If buttons weren't added already
                if cl not in existed_clusters:
                    existed_clusters.append(cl)


        if len(existed_clusters) != 5:
            error_popup("Please highlight exactly 5 sentences")
        else:

            global timer_highlighting, timer_ranking
            timer_highlighting = round(time.time() - self.start_time, 1)
            timer_ranking = time.time()

            self.title["text"] = "Ranking"

            buttons = [btn for btn in self.buttons_mapping]
            for btn in buttons:
                btn.configure(command=lambda butn=btn: self.change_color_ranking(butn))

            self.next_btn["text"] = "Next"
            self.next_btn.configure(command=self.next)

    # Next button
    def next(self):

        global timer_ranking, highlighted_sentences, highlighted_sentences_scores, ranking_dict
        timer_ranking = round(time.time() - timer_ranking, 1)
        flag_continue = True
        buttons = [btn for btn in self.buttons_mapping]
        existed_clusters = []

        highlighted_sentences = []
        highlighted_sentences_scores = []

        # Foreach button (word)
        for btn in buttons:
            if btn["bg"] == HIGHLIGHTED_COLOR:

                # Current button's cluster
                cl = self.buttons_mapping[btn]

                # If buttons weren't added already
                if cl not in existed_clusters:
                    highlighted_buttons = [btn["text"] for btn in self.buttons_mapping if self.buttons_mapping[btn] == cl]
                    existed_clusters.append(cl)
                    highlighted_sentence = ' '.join(highlighted_buttons)
                    highlighted_sentence_val = highlighted_sentence[highlighted_sentence.rfind("[") + 1 : highlighted_sentence.rfind("]")]
                    try:
                        int(highlighted_sentence_val)
                        highlighted_sentence_fixed = highlighted_sentence[0: highlighted_sentence.rfind(" ")]
                        highlighted_sentences.append(highlighted_sentence_fixed)
                        highlighted_sentences_scores.append(highlighted_sentence_val)
                    except:
                        error_popup("Not all sentences were ranked")
                        flag_continue = False


        if flag_continue is True:

            for i in range(1, 6):
                ranking_dict[i] = "normal"

            self.master.switch_frame(QuestionsInstructions)


    # Highlighting method
    def change_color(self, btn):
        global opened_ranking_popup

        if opened_ranking_popup is False:

            # Current cluster (sentence)
            clust = self.buttons_mapping[btn]

            # List of buttons to change
            buttons_to_change = []

            # Foreach button with same cluster (in same sentence)
            for key in self.buttons_mapping:
                if clust == self.buttons_mapping[key]:
                    buttons_to_change.append(key)

            # Changing the button's color
            for button in buttons_to_change:
                if button["bg"] == BACKGROUND_COLOR:
                    button.config(bg=HIGHLIGHTED_COLOR)
                else:
                    button.config(bg=BACKGROUND_COLOR)


    # Ranking method
    def change_color_ranking(self, btn):
        global opened_ranking_popup

        if btn["bg"] == HIGHLIGHTED_COLOR:

            if opened_ranking_popup is False:

                # Current cluster (sentence)
                clust = self.buttons_mapping[btn]

                # List of buttons to change
                buttons_to_change = []

                # Foreach button with same cluster (in same sentence)
                for key in self.buttons_mapping:
                    if clust == self.buttons_mapping[key]:
                        buttons_to_change.append(key)

                flag_marked_already = False
                value_marked = 0

                for btn in buttons_to_change:
                    if "[" in btn["text"] and "]" in btn["text"]:
                        flag_marked_already = True
                        value_marked = int(btn["text"].replace("[", "").replace("]", ""))


                if flag_marked_already is False:
                    for btn in buttons_to_change:
                        btn["bg"] = RANKING_COLOR

                    val = ranking_popup()
                    ranking_dict[val] = "disabled"


                    # Changing the button's color
                    for button in buttons_to_change:
                        button["bg"] = HIGHLIGHTED_COLOR
                        if button['text'] == "":
                            button['text'] = "[" + str(val) + "]"
                else:
                    ranking_dict[value_marked] = "normal"
                    for button in buttons_to_change:
                        button["bg"] = HIGHLIGHTED_COLOR
                        if "[" in button['text'] and "]" in button['text']:
                            button['text'] = ""


# Questions Instructions
class QuestionsInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Questions Instructions")

        instructions = "In this step, you will have to answer 3 multiple choice questions about the text."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(QuestionsFrame)).pack()


# Questions Frame
class QuestionsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Current question
        self.question_num = 1

        # Title
        self.title = new_title(self, "Question " + str(self.question_num))

        # Start time for timer
        self.start_time = time.time()

        # Inner frames
        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.q_frame = tk.Frame(self.inner_frame, bg=BACKGROUND_COLOR)

        question = current_text_questions[self.question_num - 1]

        # Q Answers
        q_answers = current_text_answers
        current_q_number = 0

        self.radio_buttons = []

        # Questions labels
        self.question_lbl = tk.Label(self.q_frame, text=question, bg=BACKGROUND_COLOR, font=QUESTION_TEXT_FONT_BOLD)
        self.question_lbl.grid(row=1, column=0, pady=(50, 20))

        # Questions string vars
        self.q_var = tk.StringVar(self.inner_frame, 0)

        # Just for tests
        #self.q_var.set(2)

        # Q Answers
        for i in range(4):
            radio_btn = tk.Radiobutton(self.q_frame, text=q_answers[current_q_number], value=i + 1, bg=BACKGROUND_COLOR, variable=self.q_var, font=QUESTION_TEXT_FONT)
            current_q_number += 1
            self.radio_buttons.append(radio_btn)
            radio_btn.grid(row=i + 2, column=0, sticky="w", pady=20)

        # Q Error
        self.q_error = tk.Label(self.inner_frame, text="", fg="red", bg=BACKGROUND_COLOR, font=QUESTION_TEXT_FONT)
        self.q_error.grid(row=6, column=0)

        self.q_frame.grid(row=0, column=0, padx=50)

        # Next button
        new_button(self.inner_frame, "Next", self.next).grid(row=7, column=0, pady=50)

        self.inner_frame.pack(side="top")

    # Next Button
    def next(self):

        # Saving timers
        global timer_q1, timer_q2, timer_q3
        if self.question_num == 1:
            timer_q1 = round(time.time() - self.start_time, 1)
        elif self.question_num == 2:
            timer_q2 = round(time.time() - self.start_time, 1)
        elif self.question_num == 3:
            timer_q3 = round(time.time() - self.start_time, 1)

        # Clean Errors
        self.q_error["text"] = ""

        # Validity indicator
        valid = True

        # Q Check
        if self.q_var.get() == "0":
            self.q_error["text"] = "Please answer the question"
            valid = False

        # Question answered
        if valid:
            self.question_num += 1
            self.start_time = time.time()
            questions_answers.append(self.q_var.get())

            # All 3 questions answered
            if self.question_num == 4:

                # All 4 texts finished
                if next_text == 4:
                    self.master.switch_frame(EndFrame)
                else:

                    # If demo
                    if demo:
                        self.master.switch_frame(EndFrame)

                    # If still has texts
                    else:
                        self.master.switch_frame(NextTextFrame)

            # If still has questions
            else:
                self.next_question()

    # Next questions
    def next_question(self):

        # Updating next question
        self.q_var.set("0")
        self.question_lbl["text"] = "Question:   " + current_text_questions[self.question_num - 1]

        # Just for tests
        #self.q_var.set("2")

        for counter in range(len(self.radio_buttons)):
            self.radio_buttons[counter]["text"] = current_text_answers[counter + (4 * (self.question_num - 1))]

        self.title["text"] = "Question " + str(self.question_num)


# Next Text Frame
class NextTextFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Next Text")

        # Save results
        save_results()

        # Clear user results
        clear_user_results()

        # Initiate next text
        init_next_text()

        new_button(self, "Click to continue to the next text", lambda: self.master.switch_frame(TextReadingInstructions)).pack(pady=100)

        global statusbar
        statusbar["text"] = ""

# End Frame
class EndFrame(tk.Frame):
    def __init__(self, master):
        global demo
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "End")

        # Save results
        save_results()

        # Clear user results
        clear_user_results()

        # If demo - continue to real experiment
        if demo:
            demo = False
            init_texts()
            new_button(self, "Continue to Experiment", lambda: master.switch_frame(TextReadingInstructions)).pack(pady=100)

        # If experiment - finish
        else:
            new_button(self, "Return to main page", lambda: master.switch_frame(MainFrame)).pack(pady=100)


# Main function
if __name__ == "__main__":

    # Main App
    app = TextSummarizationApp()

    # App's title
    app.wm_title(APP_NAME)

    app.mainloop()
