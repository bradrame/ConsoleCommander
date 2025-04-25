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
bbody_full = (5, 115, 941, 1027)


# PY FILES SETUP & COMMANDS
def run_ocr():
    global ocr_results
    ocr_results = []
    region = bbody_full
    image = ImageGrab.grab(bbox=region)
    word_coord = my_ocr.view_screen(reader, region, image)
    for word, coord in word_coord:
        ocr_results.append(word)
    #my_ocr.check_word(region, word_coord, '66')


def run_llm():
    options = [f'{ocr_results}', 'wait']
    prompt = (
        "You have a list of words and options. "
        f"The words in the brackets are {ocr_results}. "
        f"Your options are {options}. "
        "You need to check the weather. "
        "Which word do you chose in this scenario? "
        "Only say the option you chose."
    )
    my_llm.run_think(ocr_results, options, prompt)

run_ocr()
run_llm()