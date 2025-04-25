import threading
import keyboard
import pyautogui
import tkinter as tk
from tkinter import Toplevel
import re

# INITIALIZE
screen_width, screen_height = pyautogui.size()
print(f'Computer resolution: {screen_width}x{screen_height}')
button_color = '#E0E0E0'
thread_running = False
index = 0
max_history = 5
current_coord = ''
previous_coord = []
current_region = ''
previous_region = []

# OVERLAY SETUP (cheated here by using ai for a more streamlined approach)
class SelectionOverlay:
    def __init__(self, root):
        self.overlay = Toplevel(root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes('-alpha', 0.3)  # 30% transparency
        self.overlay.attributes('-topmost', True)
        self.overlay.configure(bg='#3498db')  # Blue color
        self.overlay.withdraw()  # Hide initially

    def show(self, x1, y1, x2, y2):
        """Show overlay rectangle from (x1,y1) to (x2,y2)"""
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        x = min(x1, x2)
        y = min(y1, y2)

        self.overlay.geometry(f'{width}x{height}+{x}+{y}')
        self.overlay.deiconify()

    def hide(self):
        self.overlay.withdraw()

# MAIN MENU CONFIG
def main_menu():
    app = tk.Tk()
    app.title('Coordinate Capture')
    def app_placement():
        window_width = app.winfo_width()
        window_height = app.winfo_height()
        window_x = (screen_width - window_width) - 12
        window_y = 2
        app.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
    placement_thread = threading.Thread(target=app_placement)
    placement_thread.start()
    font_bold = ('Helvetica', 10, 'bold')
    font_normal = ('Helvetica', 10)
    info_label = tk.Label(app, text='\n\n'
                                    'This app collects (x, y) coordinates.\n'
                                    'Click \'Get Coords\' and then press\n'
                                    'shift to get the (x, y) coord values.\n\n'
                                    'Press and hold shift to get a region\n'
                                    'of coordinates: (x1, y1) and (x2, y2).\n',
                          font=font_bold)
    info_label.pack(padx=20, pady=5)

# BUTTONS SETUP
    coords_button = tk.Button(app, text='Get Coords', command=lambda: button_press('Get'), width=30, height=2, bg=button_color)
    coords_button.pack(pady=5)
    tk.Button(app, text='Quit', command=lambda: button_press('Quit'), width=30, height=2, bg=button_color).pack(pady=5)
    keyboard.add_hotkey('ctrl+q', lambda: button_press('Quit'))

# MANUAL OVERLAY SETUP
    manually_label = tk.Label(app, text='Write the region parameters in\n'
                                        'the text box below to manually\n'
                                        'check for that region location.')
    manually_label.pack(pady=5)
    manually_entry = tk.Entry(app, width=30)
    manually_entry.pack(pady=5)
    check_label = tk.Label(app, text='Example: (5, 10, 10, 15)\n'
                                      'Press enter to check.',
                           fg='gray', font=font_bold)
    check_label.pack(pady=5)
    manual_overlay = SelectionOverlay(app)
    def show_manual_region(event):
        input_text = manually_entry.get()
        numbers = re.findall(r'\d+', input_text)
        if len(numbers) >= 4:
            try:
                x1, y1, x2, y2 = map(int, numbers[:4])
                manual_overlay.show(x1, y1, x2, y2)
                app.after(1000, manual_overlay.hide)
            except ValueError:
                print('--INVALID COORDINATES ENTERED')
        else:
            print('--ERROR: MANUAL OVERLAY')
    manually_entry.bind('<Return>', show_manual_region)

# COORDINATE / REGION HISTORY
    coords_label = tk.Label(app, text='\nCollected Coordinates:', font=font_bold)
    coords_label.pack(pady=5)
    currentCoord_label = tk.Label(app, text=current_coord,
                                  font=font_normal)
    currentCoord_label.pack(pady=1)
    previousCoord_label = tk.Label(app, text=previous_coord,
                                   font=font_normal, fg='gray',
                                   height=5, anchor='nw', justify='left')
    previousCoord_label.pack(pady=1)
    regions_label = tk.Label(app, text='Collected Regions:', font=font_bold)
    regions_label.pack(pady=5)
    currentRegion_label = tk.Label(app, text=current_region,
                                   font=font_normal)
    currentRegion_label.pack(pady=1)
    previousRegion_label = tk.Label(app, text=previous_region,
                                    font=font_normal, fg='gray',
                                    height=5, anchor='nw', justify='left')
    previousRegion_label.pack(pady=1)

# BUTTONS CONFIG
    def button_press(button):
        global thread_running, task_thread
        if button == 'Get':
            print('\n--TASK STARTED\n')
            thread_running = True
            coords_button.config(text='End Task', command=lambda: button_press('End'))
            task_thread = threading.Thread(target=get_coords, daemon=True)
            task_thread.start()
        if button == 'End':
            thread_running = False
            coords_button.config(text='PRESS SHIFT TO CONFIRM', bg='#FFA07A')
        if button == 'Quit':
            app.destroy()

# COORDINATE / REGION CAPTURE
    def get_coords():
        global index, current_coord, previous_coord, current_region, previous_region
        overlay = SelectionOverlay(app)
        while thread_running:
            keyboard.wait('shift')
            start_x, start_y = pyautogui.position()
            while keyboard.is_pressed('shift'):
                current_x, current_y = pyautogui.position()
                overlay.show(start_x, start_y, current_x, current_y)
            overlay.hide()
            end_x, end_y = pyautogui.position()
            if thread_running:
                index += 1
                if start_x == end_x and start_y == end_y:
                    previous_coord.insert(0, current_coord)
                    previous_coord = previous_coord[:max_history]
                    current_coord = f'[{index}] ({start_x}, {start_y})'
                    currentCoord_label.config(text=current_coord)
                    previousCoord_label.config(text='\n'.join(previous_coord))
                    print(f'[{index}] ({start_x}, {start_y})')
                else:
                    previous_region.insert(0, current_region)
                    previous_region = previous_region[:max_history]
                    current_region = f'[{index}] ({start_x}, {start_y}, {end_x}, {end_y})'
                    currentRegion_label.config(text=current_region)
                    previousRegion_label.config(text='\n'.join(previous_region))
                    print(f'[{index}] ({start_x}, {start_y}, {end_x}, {end_y})')


        print('\n--TASK ENDED')
        coords_button.config(text='Get Coords', command=lambda: button_press('Get'), bg=button_color)

    app.mainloop()

# INITIALIZE APP MENU
main_menu()
print('\n--ENDED SESSION')