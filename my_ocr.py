import numpy as np
import pyautogui


def view_screen(reader, region, image):
    global word_coord
    i = 1
    image_np = np.array(image)
    result = reader.readtext(image_np)
    word_coord = []
    words = []
    for (bbox, text, prob) in result:
        left_x = int(bbox[0][0])
        right_x = int(bbox[1][0])
        x_center = int((bbox[0][0] + bbox[2][0]) // 2)
        y_center = int((bbox[0][1] + bbox[2][1]) // 2)
        words.append((y_center, left_x, right_x, text))
        word_coord.append((text, (x_center, y_center)))
    words.sort(key=lambda k: (k[0], k[1]))
    lines = []
    if words:
        current_line = [words[0]]
        prev_y = words[0][0]
        for word in words[1:]:
            y = word[0]
            if abs(y - prev_y) <= 10:
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]
            prev_y = y
        lines.append(current_line)
    for line in lines:
        sorted_line = sorted(line, key=lambda x: x[1])
        segments = []
        current_segment = []
        prev_right = None
        horizontal_gap_threshold = 20
        for word in sorted_line:
            y, left, right, text = word
            if prev_right is not None and (left - prev_right) > horizontal_gap_threshold:
                segments.append(current_segment)
                current_segment = []
            current_segment.append(text)
            prev_right = right
        segments.append(current_segment)
        for segment in segments:
            line_text = ' '.join(segment)
            print(f'[{i}]: {line_text}')
            i += 1
    return word_coord

def check_word(region, word_coord, pattern):
    global coord, found
    found = False
    #view_screen(reader, region, image)
    for word, coord in word_coord:
        if pattern in word:
            found = True
            coord = ((coord[0] + region[0]), (coord[1] + region[1]))
            print(f'\n[ {pattern} ] FOUND HERE: {coord}')
            pyautogui.moveTo(coord)
            return coord
    if not found:
        print(f'\n[ {pattern} ] WAS NOT FOUND')
        return None