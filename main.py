import my_browser
import my_llm
import my_ocr
import pyautogui
import ollama
import easyocr
from PIL import ImageGrab


# INITIALIZE SETUP
screen_width, screen_height = pyautogui.size()
browser = ''
# USE IF BROWSER NOT SET UP:
# my_browser.setup_browser(screen_width, screen_height)
active_tab = ''
# GET ACTIVE TAB:
# active_tab = my_browser.get_tab()
# USE IF IDE NOT SET UP:
# my_browser.setup_ide(screen_width, screen_height)
reader = easyocr.Reader(['en'])
# USE COORD_FINDER.PY TO GET THE STATIC REGIONS FOR YOUR DEVICE
tabs = (115, 8, 838, 40)
address_bar = (135, 45, 657, 77)
browser_body_full = (5, 115, 941, 1027)
task = 'Click the last available job title.'


# PY FILES SETUP & COMMANDS
def run_decision(command):
    print(f'\n--LLM DECISION: {command}')
    if command == 'wait':
        print('--LLM WILL WAIT FOR NEXT TASK')
    else:
        my_ocr.check_word(region, word_coord, llm_output)

def run_ocr():
    global ocr_results, region, word_coord
    ocr_results = []
    region = browser_body_full
    image = ImageGrab.grab(bbox=region)
    word_coord = my_ocr.view_screen(reader, region, image)
    for word, coord in word_coord:
        ocr_results.append(word)

def run_llm():
    global llm_output

    prompt = (
        "You need to click a button or link. "
        f"Each context is located within the brackets: {ocr_results}. "
        f"{task} "
        "Which context do you chose in this scenario? "
        "Choose a context, or say 'wait' if no context is given. "
        "Only say the option you chose. "
        "/no_think" # /no_think for qwen3 use case
    )
    llm_output = my_llm.run_think(ocr_results, prompt)
    run_decision(llm_output)

run_ocr()
run_llm()