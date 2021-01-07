import tkinter as tk
import time
from Controller import Controller
from Settings import *
from EyeTracking import start_eye_tracking

TITLE_FONT_STYLE = ("David", 24, "bold")
SUBTITLE_FONT_STYLE = ("David", 20, "bold")
TEXT_FONT = ("David", 16)
TEXT_FONT_BOLD = ("David", 16, "bold")
TITLE_FONT_COLOR = 'DarkBlue'
BACKGROUND_COLOR = "azure2"

controller = Controller()

# Texts
texts = []
current_text_id = ""
current_text = ""
current_text_questions = []
current_text_answers = []
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

demo = False

opened_popups = []

def init_texts():
    global texts, current_text_id, current_text, current_text_questions, current_text_answers, next_text, demo
    if demo:
        texts = controller.get_demo_texts()
    else:
        texts = controller.get_demo_texts()
    current_text_id = texts[0][0]
    current_text = texts[0][1]
    current_text_questions = texts[0][2]
    current_text_answers = texts[0][3]
    next_text = 1


def init_next_text():
    global texts, current_text_id, current_text, current_text_questions, current_text_answers, next_text
    current_text_id = texts[next_text][0]
    current_text = texts[next_text][1]
    current_text_questions = texts[next_text][2]
    current_text_answers = texts[next_text][3]
    next_text += 1


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

def save_results():
    # Do we care which user? assign userid?
    if not demo:
        times = [timer_text_reading, timer_text_summarization, timer_highlighting, timer_ranking, timer_q1, timer_q2, timer_q3]
        controller.save_text_results(current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)

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

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    popup_width = 700
    popup_height = 400

    x_coordinate = int((screen_width / 2) - (popup_width / 2))
    y_coordinate = int((screen_height / 2) - (popup_height / 2))

    win.geometry("{}x{}+{}+{}".format(popup_width, popup_height, x_coordinate, y_coordinate))
    new_title(win, title)
    tk.Label(win, text=content, bg=BACKGROUND_COLOR, justify=justify).pack()

    opened_popups.append(win)


def new_title(frame, title):
    title = tk.Label(frame, text=title, fg=TITLE_FONT_COLOR, font=TITLE_FONT_STYLE, bg=BACKGROUND_COLOR)
    title.pack(side="top", fill="x", pady=10)
    return title

def new_button(frame, btn_text, btn_command):
    btn = tk.Button(frame, text=btn_text, command=btn_command, fg="white", bg="darkblue", font=("David", 14, "bold"))
    return btn

def new_subtitle(frame, subtitle):
    lbl = tk.Label(frame, text=subtitle, fg=TITLE_FONT_COLOR, font=SUBTITLE_FONT_STYLE, bg=BACKGROUND_COLOR)
    return lbl


def is_positive_number(num):
    try:
        return int(num) > 0
    except:
        return False


class TextSummarizationApp(tk.Tk):

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.attributes("-fullscreen", True)

        menu_bar = tk.Menu(self)
        menu_bar.add_command(label="Main", command=lambda: self.switch_frame(MainFrame))
        menu_bar.add_command(label="Instructions", command=self.popup_instructions)
        menu_bar.add_command(label="Contact", command=self.popup_contact)
        menu_bar.add_command(label="About", command=self.popup_about)
        menu_bar.add_command(label="Exit", command=self.tk.destroy)

        self.tk.configure(menu=menu_bar)
        self.tk.configure(bg=BACKGROUND_COLOR)

        self.current_frame = None
        self.switch_frame(MainFrame)

    def popup_instructions(self):
        instructions_string = "This experiment contains 5 stages:\n\n" \
                              "1.\tText Reading - Reading a short text in English\n\n" \
                              "2.\tText Summarization - Summarize the text in own words\n\n" \
                              "3.\tHighlighting - Highlight important sentences in the text\n\n" \
                              "4.\tRanking - Rank the highlighted sentences from the text\n\n" \
                              "5.\tQuestions - Answer 3 multiple choice questions for each text\n\n\n\n" \
                              "There are 4 texts total.\n\n" \
                              "The 5 stages must be repeated for each text."

        popup("Instructions", instructions_string)

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

    def popup_about(self):
        about_string = "This system was created for a Text Summarization experiment.\n\n" \
                       "In this experiment we will collect eye-tracking data while the participants read and interact with texts.\n\n" \
                       "This data will be used to create a text summarization model based on natural interaction of the user with the text.\n\n" \
                       "SISE\n" \
                       "December 2020\n\n"

        popup("About", about_string)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()


class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, APP_NAME).pack(side="top", fill="x", pady=10)

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

        new_button(self, "Start", self.start).pack()



    def start(self):
        init_texts()
        self.master.switch_frame(NewParticipantFrame)


class NewParticipantFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "New Participant")

        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        pad_x, pad_y = 40, 40

        # String Variables
        self.id_var = tk.StringVar(self)
        self.first_name_var = tk.StringVar(self)
        self.last_name_var = tk.StringVar(self)
        self.age_var = tk.StringVar(self)
        self.gender_var = tk.StringVar(self)
        self.gender_var.set("Select")

        # Just for tests
        self.id_var.set("4")
        self.first_name_var.set("aaa")
        self.last_name_var.set("bbb")
        self.age_var.set("5")
        self.gender_var.set("Male")

        # ID
        tk.Label(inner_frame, text="ID", font=TEXT_FONT, bg=BACKGROUND_COLOR).grid(row=0, column=0)
        tk.Entry(inner_frame, width="60", textvariable=self.id_var).grid(row=0, column=1, padx=pad_x, pady=pad_y)
        self.id_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.id_error.grid(row=0, column=2)

        # First Name
        tk.Label(inner_frame, text="First Name", font=TEXT_FONT, bg=BACKGROUND_COLOR).grid(row=1, column=0)
        tk.Entry(inner_frame, width="60", textvariable=self.first_name_var).grid(row=1, column=1, padx=pad_x, pady=pad_y)
        self.first_name_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.first_name_error.grid(row=1, column=2)

        # Last Name
        tk.Label(inner_frame, text="Last Name", font=TEXT_FONT, bg=BACKGROUND_COLOR).grid(row=2, column=0)
        tk.Entry(inner_frame, width="60", textvariable=self.last_name_var).grid(row=2, column=1, padx=pad_x, pady=pad_y)
        self.last_name_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.last_name_error.grid(row=2, column=2)

        # Gender
        tk.Label(inner_frame, text="Gender", font=TEXT_FONT, bg=BACKGROUND_COLOR).grid(row=3, column=0)
        tk.OptionMenu(inner_frame, self.gender_var, "Select", "Male", "Female").grid(row=3, column=1, padx=pad_x, pady=pad_y)
        self.gender_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.gender_error.grid(row=3, column=2)

        # Age
        tk.Label(inner_frame, text="Age", font=TEXT_FONT, bg=BACKGROUND_COLOR).grid(row=4, column=0, pady=pad_y)
        tk.Entry(inner_frame, width="60", textvariable=self.age_var).grid(row=4, column=1, padx=pad_x, pady=pad_y)
        self.age_error = tk.Label(inner_frame, text="", font=TEXT_FONT, fg="red", bg=BACKGROUND_COLOR)
        self.age_error.grid(row=4, column=2)

        # Continue Button
        new_button(inner_frame, "Continue", self.new_participant).grid(row=5, column=1, pady=(pad_y, 100))

        inner_frame.pack(anchor="s", side="bottom")

    def new_participant(self):

        # Clean Error Labels
        self.id_error['text'] = ""
        self.first_name_error['text'] = ""
        self.last_name_error['text'] = ""
        self.gender_error['text'] = ""
        self.age_error['text'] = ""

        # Form Inputs
        id = self.id_var.get().strip()
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        gender = self.gender_var.get().strip()
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
            controller.add_new_participant(id, first_name, last_name, gender, age)
            self.master.switch_frame(DemoExperimentFrame)


class DemoExperimentFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Demo / Experiment")

        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        pad_x, pad_y = 100, 30
        demo_label = new_subtitle(self.inner_frame, "Demo")
        demo_label.grid(row=0, column=0, pady=pad_y)

        experiment_label = new_subtitle(self.inner_frame, "Experiment")
        experiment_label.grid(row=0, column=1, pady=pad_y, padx=pad_x)

        demo_label_description = tk.Label(self.inner_frame, text="Trying the system for 1 demo text", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        demo_label_description.grid(row=1, column=0, pady=pad_y, padx=pad_x)

        experiment_label_description = tk.Label(self.inner_frame, text="Starting the experiment", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        experiment_label_description.grid(row=1, column=1, pady=pad_y, padx=pad_x)

        demo_button = new_button(self.inner_frame, "Start Demo", self.start_demo)
        demo_button.grid(row=2, column=0, pady=(pad_y, 300), padx=pad_x)

        experiment_button = new_button(self.inner_frame, "Start Experiment", lambda: self.master.switch_frame(TextReadingInstructions))
        experiment_button.grid(row=2, column=1, pady=(pad_y, 300), padx=pad_x)

        self.inner_frame.pack(side="bottom")

    def start_demo(self):
        global demo
        demo = True
        self.master.switch_frame(TextReadingInstructions)


class TextReadingInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Text Reading Instructions")

        instructions = "In this step, you will have to read a short text."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", self.start_reading_text).pack()


    def start_reading_text(self):
        global timer_text_reading
        self.master.switch_frame(TextSummarizationInstructions)
        timer_text_reading = start_eye_tracking(current_text)

class TextSummarizationInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Text Summarizing Instructions")

        instructions = "In this step, you will have to summarize the text you read in the last step."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(TextSummarizationFrame)).pack()


class TextSummarizationFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Start time for timer
        self.start_time = time.time()

        new_title(self, "Text Summarization")
        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # Text box
        self.user_text_summary = tk.Text(self.inner_frame, height="30", width="100", font=TEXT_FONT)
        self.user_text_summary.grid(row=1, column=0)

        # Next button
        next_btn = new_button(self.inner_frame, btn_text="Next", btn_command=self.next)
        next_btn.grid(row=3, column=0, pady=20)

        # Timer
        tk.Label(self.inner_frame, text="Time Left:", bg=BACKGROUND_COLOR).grid(row=3, column=1, pady=20)
        self.timer_label = tk.Label(self.inner_frame, text="", bg=BACKGROUND_COLOR)
        self.timer_label.grid(row=3, column=2)

        self.inner_frame.pack(side="bottom")

        self.update_timer()

    def next(self):
        global text_summary, timer_text_summarization
        text_summary = self.user_text_summary.get("1.0", 'end-1c')
        timer_text_summarization = round(time.time() - self.start_time, 1)
        self.master.switch_frame(HighlightingInstructions)




    def update_timer(self):
        time_passed = time.time() - self.start_time
        time_left = SUMMARIZATION_TIMER - int(time_passed)

        # More than a minute
        if time_left > 60:
            time_left_minutes = str(int(time_left / 60))
            time_left_seconds = int(time_left % 60)

            # Add zero if less than 10 seconds (visualization)
            if time_left_seconds < 10:
                time_left_seconds = "0" + str(time_left_seconds)

            self.timer_label.configure(text=time_left_minutes+":"+str(time_left_seconds))

        # Less than a minute
        else:
            self.timer_label.configure(text=time_left)

        # Updating every second (1000 ms)
        self.after(1000, self.update_timer)


class HighlightingInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Highlighting Instructions")

        instructions = "In this step, you will have to highlight important sentences from the text."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(HighlightingFrame)).pack()


class HighlightingFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Highlighting")

        # Start time for timer
        self.start_time = time.time()

        sentences = current_text.split(".")

        self.buttons = []
        idx = 0
        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        for sentence in sentences:
            sentence += "."
            sen_btn = tk.Button(self.inner_frame, text=sentence, bg=BACKGROUND_COLOR)
            sen_btn.configure(command=lambda btn=sen_btn: self.change_color(btn))
            sen_btn.config(highlightthickness=0, borderwidth=0)
            sen_btn.grid(row=idx, column=0, sticky="w", pady=10)
            idx += 1
            self.buttons.append(sen_btn)


        # Next button
        next_btn = new_button(self.inner_frame, btn_text="Next", btn_command=self.next)
        next_btn.grid(row=idx+1, column=0, pady=20)

        # Timer
        tk.Label(self.inner_frame, text="Time Left:", bg=BACKGROUND_COLOR).grid(row=idx+1, column=1, pady=20)
        self.timer_label = tk.Label(self.inner_frame, text="", bg=BACKGROUND_COLOR)
        self.timer_label.grid(row=idx+1, column=2)

        self.inner_frame.pack(side="bottom")
        self.update_timer()

    def next(self):
        global timer_highlighting
        timer_highlighting = round(time.time() - self.start_time, 1)

        for btn in self.buttons:
            if btn["bg"] == HIGHLIGHTED_COLOR:
                highlighted_sentences.append(btn["text"])

        self.master.switch_frame(RankingInstructions)

    def change_color(self, lbl):
        if lbl["bg"] == BACKGROUND_COLOR:
            lbl.config(bg=HIGHLIGHTED_COLOR)
        else:
            lbl.config(bg=BACKGROUND_COLOR)

    def update_timer(self):
        time_passed = time.time() - self.start_time
        time_left = HIGHLIGHTING_TIMER - int(time_passed)

        # More than a minute
        if time_left > 60:
            time_left_minutes = str(int(time_left / 60))
            time_left_seconds = int(time_left % 60)

            # Add zero if less than 10 seconds (visualization)
            if time_left_seconds < 10:
                time_left_seconds = "0" + str(time_left_seconds)

            self.timer_label.configure(text=time_left_minutes+":"+str(time_left_seconds))

        # Less than a minute
        else:
            self.timer_label.configure(text=time_left)

        # Updating every second (1000 ms)
        self.after(1000, self.update_timer)


class RankingInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Ranking Instructions")

        instructions = "In this step, you will have to rank the highlighted sentences from the last step."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(RankingFrame)).pack()


class RankingFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Ranking")

        # Start time for timer
        self.start_time = time.time()

        scores = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        tk.Label(self.inner_frame, text="Sentences / Scores", bg=BACKGROUND_COLOR, font=TEXT_FONT).grid(row=1, column=0)

        # Scores
        for i in range(len(scores)):
            tk.Label(self.inner_frame, text=scores[i], bg=BACKGROUND_COLOR, justify="left", font=TEXT_FONT).grid(row=1, column=i+2, padx=10, pady=5, sticky="w")

        self.string_vars = []
        self.error_vars = []

        # Sentences
        for i in range(len(highlighted_sentences)):
            self.st_var = tk.StringVar(self.inner_frame, 0)
            tk.Message(self.inner_frame, text=highlighted_sentences[i], bg=BACKGROUND_COLOR, justify="left", width=500).grid(row=i+2, column=0, pady=5)
            error = tk.Label(self.inner_frame, text="", fg="red", bg=BACKGROUND_COLOR)
            error.grid(row=i+2, column=1, pady=20)

            # Radio buttons
            for j in range(len(scores)):
                tk.Radiobutton(self.inner_frame, value=scores[j], text=" ", variable=self.st_var, bg=BACKGROUND_COLOR).grid(row=i+2, column=j+2, padx=10, pady=5)

            # String vars
            self.string_vars.append(self.st_var)
            self.error_vars.append(error)

        # Just for tests
        for var in self.string_vars:
            var.set("2")

        # Next button
        next_btn = new_button(self.inner_frame, btn_text="Next", btn_command=self.next)
        next_btn.grid(row=len(highlighted_sentences)+3, column=0, pady=20)


        # Timer
        tk.Label(self.inner_frame, text="Time Left:", bg=BACKGROUND_COLOR).grid(row=len(highlighted_sentences)+3, column=1, pady=20)
        self.timer_label = tk.Label(self.inner_frame, text="", bg=BACKGROUND_COLOR)
        self.timer_label.grid(row=len(highlighted_sentences)+3, column=2)

        self.inner_frame.pack(side="bottom")

        self.update_timer()

    def next(self):
        global timer_ranking
        timer_ranking = round(time.time() - self.start_time, 1)

        for err in self.error_vars:
            err["text"] = ""

        valid = True

        for i in range(len(self.string_vars)):
            if self.string_vars[i].get() == "0":
                self.error_vars[i]["text"] = "*"
                valid = False

        if valid:
            for var in self.string_vars:
                highlighted_sentences_scores.append(var.get())
            self.master.switch_frame(QuestionsInstructions)

    def update_timer(self):
        time_passed = time.time() - self.start_time
        time_left = RANKING_TIMER - int(time_passed)

        # More than a minute
        if time_left > 60:
            time_left_minutes = str(int(time_left / 60))
            time_left_seconds = int(time_left % 60)

            # Add zero if less than 10 seconds (visualization)
            if time_left_seconds < 10:
                time_left_seconds = "0" + str(time_left_seconds)

            self.timer_label.configure(text=time_left_minutes+":"+str(time_left_seconds))

        # Less than a minute
        else:
            self.timer_label.configure(text=time_left)

        # Updating every second (1000 ms)
        self.after(1000, self.update_timer)

class QuestionsInstructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        new_title(self, "Questions Instructions")

        instructions = "In this step, you will have to answer 3 multiple choice questions about the text."

        tk.Label(self, text=instructions, bg=BACKGROUND_COLOR, font=TEXT_FONT).pack(pady=50)
        new_button(self, "Click here to continue", lambda: self.master.switch_frame(QuestionsFrame)).pack()


class QuestionsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

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
        self.question_lbl = tk.Label(self.q_frame, text="Question:   " + question, bg=BACKGROUND_COLOR, font=TEXT_FONT_BOLD)
        self.question_lbl.grid(row=1, column=0, pady=(50, 20))

        # Questions string vars
        self.q_var = tk.StringVar(self.inner_frame, 0)

        # Just for tests
        self.q_var.set(2)

        # Q Answers
        for i in range(4):
            radio_btn = tk.Radiobutton(self.q_frame, text=q_answers[current_q_number], value=i + 1, bg=BACKGROUND_COLOR, variable=self.q_var, font=TEXT_FONT)
            current_q_number += 1
            self.radio_buttons.append(radio_btn)
            radio_btn.grid(row=i + 2, column=0, sticky="w", pady=20)

        # Q Error
        self.q_error = tk.Label(self.inner_frame, text="", fg="red", bg=BACKGROUND_COLOR, font=TEXT_FONT)
        self.q_error.grid(row=6, column=0)

        self.q_frame.grid(row=0, column=0, padx=50)

        # Next button
        new_button(self.inner_frame, "Next", self.next).grid(row=7, column=1, pady=50)

        # Timer
        tk.Label(self.inner_frame, text="Time Left:", bg=BACKGROUND_COLOR).grid(row=7, column=2, pady=20)
        self.timer_label = tk.Label(self.inner_frame, text="", bg=BACKGROUND_COLOR)
        self.timer_label.grid(row=7, column=3)

        self.inner_frame.pack(side="top")

        self.update_timer()

    def next(self):

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

        if valid:
            self.question_num += 1
            self.start_time = time.time()
            questions_answers.append(self.q_var.get())

            if self.question_num == 4:
                if next_text == 4:
                    self.master.switch_frame(EndFrame)
                else:
                    if demo:
                        self.master.switch_frame(EndFrame)
                    else:
                        self.master.switch_frame(NextTextFrame)

            else:
                self.next_question()


    def next_question(self):
        self.q_var.set("0")
        self.question_lbl["text"] = "Question:   " + current_text_questions[self.question_num - 1]

        # Just for tests
        self.q_var.set("2")

        for counter in range(len(self.radio_buttons)):
            self.radio_buttons[counter]["text"] = current_text_answers[counter]

        self.title["text"] = "Question " + str(self.question_num)

    def update_timer(self):
        time_passed = time.time() - self.start_time
        time_left = QUESTIONS_TIMER - int(time_passed)

        # More than a minute
        if time_left > 60:
            time_left_minutes = str(int(time_left / 60))
            time_left_seconds = int(time_left % 60)

            # Add zero if less than 10 seconds (visualization)
            if time_left_seconds < 10:
                time_left_seconds = "0" + str(time_left_seconds)

            self.timer_label.configure(text=time_left_minutes+":"+str(time_left_seconds))

        # Less than a minute
        else:
            self.timer_label.configure(text=time_left)

        # Updating every second (1000 ms)
        self.after(1000, self.update_timer)


class NextTextFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Next Text")
        save_results()
        clear_user_results()
        init_next_text()

        new_button(self, "Click to continue to the next text", lambda: self.master.switch_frame(TextReadingInstructions)).pack(pady=100)



class EndFrame(tk.Frame):
    def __init__(self, master):
        global demo
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "End")
        save_results()
        clear_user_results()
        if demo:
            demo = False
            init_texts()
            new_button(self, "Continue to Experiment", lambda: master.switch_frame(TextReadingInstructions)).pack(pady=100)
        else:
            new_button(self, "Return to main page", lambda: master.switch_frame(MainFrame)).pack(pady=100)


if __name__ == "__main__":
    app = TextSummarizationApp()
    app.wm_title(APP_NAME)
    app.mainloop()