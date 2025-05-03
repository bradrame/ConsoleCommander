import my_llm
import my_ocr
import pyautogui
import pygetwindow as gw
import re
import ollama
import easyocr
from PIL import ImageGrab


# INITIALIZED SETUP
screen_width, screen_height = pyautogui.size()
reader = easyocr.Reader(['en'])
# USE COORD_FINDER.PY TO GET THE STATIC REGIONS FOR YOUR DEVICE
tabs = (115, 8, 838, 40)
address_bar = (135, 45, 657, 77)
browser_full = (5, 115, 941, 1027)
browser_top = (5, 115, 941, 628)
browser_bottom = (5, 628, 941, 1027)
browser_left = (5, 115, 474, 1027)
browser_right = (474, 115, 941, 1027)

# FUNCTIONS SETUP
def get_tab():
    browser = gw.getWindowsWithTitle('edge')
    for app_title in browser:
        active_tab = app_title.title

        # IF MULTIPLE TABS ARE OPEN
        if ' and' in active_tab:
            return re.sub(r' and.*', '', active_tab)

        # IF ONE TAB IS OPEN
        elif '- Personal' in active_tab:
            return re.sub(r' - Personal.*', '', active_tab)
    else:
        return '--NO BROWSER DETECTED'

def run_ocr():
    global ocr_results, region, word_coord
    ocr_results = []
    region = browser_top
    image = ImageGrab.grab(bbox=region)
    word_coord = my_ocr.view_screen(reader, region, image)
    for word, coord in word_coord:
        ocr_results.append(word)

def run_decision(command):
    print(f'\n--LLM DECISION: {command}')
    if command == 'wait':
        print('--LLM WILL WAIT FOR NEXT TASK')
    else:
        my_ocr.check_word(region, word_coord, llm_output)

def run_llm(action, prompt):
    global llm_output
    if action == 'click':
        action = (
            "You need to choose a context related to the task. "
            f"Each context is located within the brackets: {ocr_results}.\n"
            f"Here's your task: '{prompt}.'\n"
            "Choose a context related to the task, or "
            "If the context doesn't match the task, say 'wait'. "
            "Only say the context you chose. "
            "/no_think" # /no_think for qwen3 use case
        )
        llm_output = my_llm.run_think(ocr_results, action)
        run_decision(llm_output)
    if action == 'adjust':
        action = (
            "Your task is to correct a mistake or "
            "fragmented result within the results. "
            f"Here are the results: {ocr_results}.\n"
            "Make the corrections and complete the results "
            "but don't say anything else. "
            "/no_think" # /no_think for qwen3 use case
        )
        llm_output = my_llm.run_think(ocr_results, action)
        print(ocr_results)
        print(llm_output)

# RUN THE PROGRAM HERE
run_ocr()
run_llm('click', 'check cart')