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
#my_browser.setup_browser(screen_width, screen_height)
active_tab = ''
#active_tab = my_browser.get_tab()
#my_browser.setup_ide(screen_width, screen_height)
reader = easyocr.Reader(['en'])
tabs = (115, 8, 838, 40)
address_bar = (135, 45, 657, 77)
browser_body_full = (5, 115, 941, 1027)


# PY FILES SETUP & COMMANDS
def run_decision(command):
    print(f'\n--LLM DECISION: {command}')
    if command == 'wait':
        print('--LLM WILL WAIT FOR NEXT TASK')
    elif command == 'Weather':
        print('Success!')
        quit()
    else:
        print('--COMMAND ERROR')

def run_ocr():
    global ocr_results, region, word_coord
    ocr_results = []
    region = browser_body_full
    image = ImageGrab.grab(bbox=region)
    word_coord = my_ocr.view_screen(reader, region, image)
    for word, coord in word_coord:
        ocr_results.append(word)

def run_llm():
    prompt = (
        "You need to click a button or link. "
        f"Each context is located within the brackets: {ocr_results}. "
        "You need to check the weather. "
        "Which context do you chose in this scenario? "
        "Choose a context, or say 'wait' if no context is given. "
        "Only say the option you chose. "
        "/no_think" # /no_think for qwen3 use case
    )
    llm_output = my_llm.run_think(ocr_results, prompt)
    if llm_output != 'wait':
        my_ocr.check_word(region, word_coord, llm_output)
    run_decision(llm_output)

run_ocr()
run_llm()