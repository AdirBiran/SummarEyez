#!/usr/bin/env python
# coding: utf-8
from EyeTracking import *
import pyautogui

# In[3]:


user_name = "aaa"
user_text = "word "*50
text_name = "Test"
user_gender = "Male"
user_age = 18
user_points = True



experiment_screen = Create_text(user_name, user_text, text_name, user_gender,
                                user_age, points=user_points, eye_tracker=False, verbose=True, see_rectangle=True)
for i in range(150):  # need to change to specific time or exit button
    x = pyautogui.position().x
    y = pyautogui.position().y
    print(i)
    # x=random.random()
    # y=random.random()
    # print("x is: " + str(x))
    # print("y is: " + str(y))
    try:
        experiment_screen.get_bbox(x, y)
        time.sleep(0.25)
    except:
        print('TclError')
        break
# except AttributeError:
#
#     print('AttributeError')
#     pass


# In[ ]:




