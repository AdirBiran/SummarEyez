import tkinter as tk
import time
import pandas as pd
import pyautogui
from Settings import *
import numpy as np
from pointGUI import pointGUI
import datetime
from nltk.tokenize import sent_tokenize

class Create_text(tk.Tk):
    def __init__(self, participant_id, text, text_id, eye_tracker=True, see_rectangle=True
                 , points=False, verbose=True):
        super().__init__()
        self.text_size = 16
        self.space_size = 4
        self.start_time = time.time()
        self.config(cursor='circle red')
        self.participant_id = participant_id
        self.text_id = text_id
        self.text = text
        self.see_rectangle = see_rectangle
        self.points = points
        self.verbose = verbose
        self.title("SummerEyes")
        self.width = self.winfo_screenwidth()  # get display width
        self.height = self.winfo_screenheight()  # get display height
        self.attributes('-fullscreen', True)
        self.font = ("helvetica", self.text_size)  # font
        self.canvas_background = "white"  # background color
        self.canvas = tk.Canvas(self, bg=self.canvas_background, width=self.width, height=self.height)
        self.canvas.pack()  # necessarily
        self.eye_tracker = eye_tracker  # if x,y coordinates from 0 to 1 set eye_tracker=True to convert them to px
        self.start_position_x = 40  # start text position (x)
        self.start_position_y = 40  # start text position (y)
        self.fixation_number = 0
        self.previous_fixation = None
        self.bbox_info = None
        self.exit = False
        self.word_bbox_info = {}
        self.word_previous_fixation = None
        self.word_fixation_number = 0
        self.print_text()
        self.keep_tracking = True
        self.read_time = -1

    def print_text(self):
        self.button_save = tk.Button(self, text="Next", command=self.quit, font=self.font, anchor="e")
        self.button_save.place(relx=0.9, rely=0.9)
        index_word = 1

        """indexing each sentence in asecnding order"""
        bbox_info = {}
        sentences = sent_tokenize(self.text)
        for index, sentenсe in enumerate(sentences):
        # for index, sentenсe in enumerate(self.text.split(".")):
            if len(sentenсe) == 0:
                continue
            sentenсe = sentenсe.lstrip()
            positions = []
            for number, word in enumerate(sentenсe.split(" ")):
                if len(word) == 0:
                    continue
                # id for specify word
                sent_id = self.canvas.create_text(self.start_position_x, self.start_position_y, text=word + ' ',
                                                  font=self.font, justify="left", fill="black", anchor="nw")
                # if number == len(sentenсe.split(" ")) - 1:
                #     suffix = '. '  # including suffix '.' as the word area
                # else:
                #     suffix = ' '  # including suffix space as the word area
                # sent_id = self.canvas.create_text(self.start_position_x, self.start_position_y,  # id for specify word
                #                                   text=word + suffix, font=self.font,
                bbox = self.canvas.bbox(sent_id)  # X1,Y1,X2,Y2 coordinates for a rectangle which encloses word item

                x_left_delta = 0
                x_right_delta = 0
                y_up_delta = 20
                y_down_delta = 20

                bbox = (bbox[0], bbox[1] - y_up_delta, bbox[2], bbox[3] + y_down_delta)

                if self.see_rectangle == True:
                    self.canvas.create_rectangle(bbox, outline="black")  # draw word rectangles
                width = self.start_position_x + bbox[2] - bbox[0] + 5  # calculate word width
                x_left = self.start_position_x
                x_right = self.start_position_x + bbox[2] - bbox[0]
                y_up = bbox[1]
                y_down = self.start_position_y + bbox[3] - bbox[1]
                if width + 120 < self.width:
                    self.start_position_x += bbox[2] - bbox[0]
                else:
                    self.start_position_x = 40
                    self.start_position_y += self.space_size * self.text_size
                position = [x_left, x_right, y_up, y_down]
                positions.append(position)
                self.word_bbox_info[tuple(position)] = [word, 0, [], {}, index_word]
                index_word += 1
            bbox_info[index + 1] = [sentenсe, positions, 0, [], {}]
            """ define for each word in specific sentence her borders coordinates, for example:
                x1, x2, y1, y2 ['Pulvinar elementum integer enim neque volutpat', 
                [[1183, 1263, 40, 63], [1263, 1370, 40, 63], [1370, 1439, 40, 63], [1439, 1490, 40, 63],
                [1490, 1554, 40, 63], [1554, 1638, 40, 63]], 0, []]"""
            self.bbox_info = bbox_info
            self.update()

    def draw_point(self, x, y):
        try:
            self.canvas.delete(self.point)
        except:
            pass
        x0 = x - 5
        y0 = y - 5
        x1 = x + 5
        y1 = y + 5
        # self.point=self.canvas.create_oval(x-10, y-10, x, y, outline="#2541f4",width=5)
        self.point = self.canvas.create_oval(x0, y0, x1, y1, outline="#2541f4", width=5)
        self.update()

    def quit(self):
        self.finish_time = time.time()
        self.read_time = round(self.finish_time - self.start_time, 1)
        self.get_output(save=True)  # for sentences
        self.words_get_output(save=True)  # for words
        #messagebox.showinfo('File was saved', 'File was saved/n You read {} sec'.format(self.read_time))
        self.keep_tracking = False
        self.destroy()

    def get_bbox(self, x, y):
        if self.eye_tracker == True:
            # pass
            x = (x * self.width)
            y = (y * self.height)
            # print(x)
            # print(y)
        if self.points == True:
            self.draw_point(x, y)
        for key, value in self.bbox_info.items():
            positions = value[1]
            for i, position in enumerate(positions):
                x_left = position[0]
                x_right = position[1]
                y_up = position[2]
                y_down = position[3]

                if x_left <= x <= x_right and y_up <= y <= y_down:
                    self.update_info_on_word(x_left, x_right, y_up, y_down)
                    index = key
                    sentence = value[0]
                    positions = value[1]
                    fixations = value[2] + 1
                    print(sentence)
                    # count_fixation_sentence = value[4]
                    if self.previous_fixation != index:
                        self.fixation_number += 1
                    self.previous_fixation = index
                    if self.fixation_number in value[4].keys():
                        value[4][self.fixation_number] += 1
                    else:
                        value[4][self.fixation_number] = 1
                    order = value[3]
                    order.append(self.fixation_number)
                    self.bbox_info[index] = [sentence, positions, fixations, order, value[4]]
                    # if self.verbose == True:
                        # print('Number sentence:{}, Sentence:{}, Order sentence:{}'.format(index, sentenсe,
                        #                                                                   self.fixation_number))
                    self.update()
                    break

    def update_info_on_word(self, x_left, x_right, y_up, y_down):
        tuple_coordinates = tuple([x_left, x_right, y_up, y_down])
        word_info = self.word_bbox_info[tuple_coordinates]
        index = word_info[4]
        if self.word_previous_fixation != index:
            self.word_fixation_number += 1
        self.word_previous_fixation = index
        fixations = word_info[1] + 1
        if self.word_fixation_number in word_info[3].keys():
            word_info[3][self.word_fixation_number] += 1
        else:
            word_info[3][self.word_fixation_number] = 1
        order = word_info[2]
        order.append(self.word_fixation_number)
        word_info[1] = fixations
        word_info[2] = order
        self.word_bbox_info[tuple_coordinates] = word_info

    def words_get_output(self, save):  # create dataframe from bbox_info
        self.output = pd.DataFrame([(b[4], b[0], b[2], b[3], b[1])
                                    for a, b in self.word_bbox_info.items()],
                                   columns=['index', 'word', 'fixation_order',
                                            'duration_fixation', 'total_duration_fixation'])
        self.output['count_letters'] = self.output['word'].apply(lambda x: len(x))
        self.output['count_fixation_normalized'] = self.output['total_duration_fixation'] / self.output['count_letters']
        self.output['fixation_order'] = self.output['fixation_order'].apply(lambda x: list(set(x)))

        if save == True:
            path = os.path.join (RESULTS_MAIN_PATH, self.participant_id, 'Words', "{}_{}.csv")
            self.output.to_csv(path.format(self.participant_id, self.text_id), index=False)

    def get_output(self, save):  # create dataframe from bbox_info
        self.output = pd.DataFrame([(a, b[0], b[3], b[4], b[2]) for a, b in self.bbox_info.items()],
                                   columns=['index', 'sentenсe', 'fixation_order', 'duration_fixation',
                                            'total_duration_fixation'])
        self.output['count_words'] = self.output['sentenсe'].apply(lambda x: len(x.split(' ')))
        self.output['count_fixation_normalized'] = self.output['total_duration_fixation'] / self.output['count_words']
        self.output['fixation_order'] = self.output['fixation_order'].apply(lambda x: list(set(x)))

        if save == True:
            path = os.path.join(RESULTS_MAIN_PATH, self.participant_id, 'Sentences', "{}_{}.csv")
            self.output.to_csv(path.format(self.participant_id, self.text_id), index=False)
            # display(self.output)

def start_eye_tracking(text, participant_id, current_text_id):
    eye_tracker = False
    experiment_screen = Create_text(participant_id, text, current_text_id,
                                    points=True, eye_tracker=eye_tracker, verbose=True, see_rectangle=True)

    if eye_tracker == False:
        while experiment_screen.keep_tracking is True:
            # need to change to specific time or exit button
            x = pyautogui.position().x
            y = pyautogui.position().y

            try:
                experiment_screen.get_bbox(x, y)
                time.sleep(0.25)
            except:
                print('TclError')
                break
        return experiment_screen.read_time
    else:
        return eye_tracking(participant_id, text, current_text_id)


def eye_tracking(participant_id, text, current_text_id):
    ######################################################################################
    # GazepointAPI.py - Example Client
    # Written in 2013 by Gazepoint www.gazept.com
    #
    # To the extent possible under law, the author(s) have dedicated all copyright
    # and related and neighboring rights to this software to the public domain worldwide.
    # This software is distributed without any warranty.
    #
    # You should have received a copy of the CC0 Public Domain Dedication along with this
    # software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

    ######################################################################################

    import socket
    # from pointGUI import pointGUI
    import time
    import math
    # from eyetrackergui import *
    # Host machine IP
    HOST = '127.0.0.1'
    # Gazepoint Port
    PORT = 4242
    ADDRESS = (HOST, PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)
    s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
    # s.send(str.encode('<SET ID="CALIBRATE_START" STATE="1" />\r\n'))
    # s.send(str.encode('<SET ID="CALIBRATE_SHOW" STATE="1" />\r\n'))

    # try:
    #     # first_screen = First_screen()
    #     first_screen.mainloop()
    #
    #     user_name = first_screen.user_name
    #     text_name = first_screen.user_text_name
    #     user_age = first_screen.user_age
    #     user_gender = first_screen.user_sex
    #     user_text = first_screen.user_text
    #     user_points = first_screen.points
    # except:
    #     pass

    AP = pointGUI()
    prevX = 1000
    prevY = 1000
    prevT = 0.0
    coordinate_list = []
    timeSum = 0
    start = 0.0
    end = 0.0
    experiment_screen = Create_text(participant_id, text, current_text_id,
                                    points=True, eye_tracker=True, verbose=True, see_rectangle=False)
    # x_list = []
    # y_list = []
    while experiment_screen.keep_tracking is True:
        if timeSum >= 0.8 and len(coordinate_list) > 0:
            # print(timeSum)
            # print(coordinate_list)
            xAvg = np.average([float(tpl[0]) for tpl in coordinate_list])
            yAvg = np.average([float(tpl[1]) for tpl in coordinate_list])
            xStd = np.std([float(tpl[0]) for tpl in coordinate_list])
            yStd = np.std([float(tpl[1]) for tpl in coordinate_list])
            # print('Std: '+str(xStd)+'  '+str(yStd))
            # print('Std average: '+str(np.average([xStd,yStd])))
            std_avarage = np.average([xStd, yStd])
            if (std_avarage < 0.1):
                AP.clearCanvas()
                AP.draw(xAvg, yAvg)
            timeSum = 0
            coordinate_list = []

        start = datetime.datetime.now()
        # print(start)

        rxdat = s.recv(1024)
        records = bytes.decode(rxdat).split("<")
        for el in records:
            if ('REC' in el):
                # print(el)
                coords = el.split("\"")

                try:
                    coordinate_list.append((coords[3], coords[5]))
                    #experiment_screen.get_bbox(xAvg, yAvg)


                except:
                    break
                    # oclidDis = math.sqrt(math.pow(float(coords[3]) - prevX, 2) + math.pow(float(coords[5]) - prevY, 2))
                    # timeThresh = float(coords[1]) - prevT
                    # print(oclidDis)
                    # print(coords[1])
                    # if  abs(prevX - float(coords[3])) > 0.01 and abs(prevY - float(coords[5]) > 0.01):
                    # print("TIME: " + coords[1] + " X:" + coords[3] + "  Y:" + coords[5])
                    # if oclidDis > 0.5:
            end = datetime.datetime.now()
            timeSum += (end - start).total_seconds()


    s.close()


                    # x = float(coords[3])
                    # y = float(coords[5])
                    # x_list.append(x)
                    # y_list.append(y)
                    # if timeThresh > 2:
                    #
                    #     # print(timeThresh, prevT)
                    #     x = np.mean(x_list)
                    #     y = np.mean(y_list)
                    #     print("x size", len(x_list))
                    #     print("y size", len(y_list))
                    #
                    #     # print("x is ",x)
                    #     # print("ys is ",y)
                    #     # x = float(coords[3])
                    #     # y = float(coords[5])
                    #     x_list = []
                    #     y_list = []
                        # print(x)
                        # print(y)
                        #     try:
                        #         experiment_screen.get_bbox(x, y)
                        #     except tk.TclError:
                        #         break
                            # AP.clearCanvas()
                        # AP.draw(float(coords[3]), float(coords[5]))
                        # print(float(coords[3]), float(coords[5]))
                        # prevX = float(coords[3])
                        # prevY = float(coords[5])
    #                     prevT = float(coords[1])
    #             except:
    #                 pass
    #
    # s.close()
    # return experiment_screen.read_time
    # # except AttributeError:
    # #
    # #     print('AttributeError')
    #     pass

    # In[ ]:
