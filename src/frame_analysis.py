import numpy as np
import cv2
import pytesseract


class Data:
    def __init__(self, time_seconds: int|float, booster_speed: int|float, booster_altitude: int|float, ship_speed, ship_altitude):
        # note time is int|float (might implement fractional seconds by looking at how many frames)
        self.time_seconds = time_seconds
 
        self.booster_speed = booster_speed
        self.booster_altitude = booster_altitude
        self.booster_engines = None
        self.boster_orientation = None

        self.ship_speed = ship_speed
        self.ship_altitude = ship_altitude
        self.ship_engines = None
        self.ship_origintation = None

    def to_string(self) -> str:
        s = ''
        s += f'time = {self.time_seconds}\n'
        s += f'Booster speed = {self.booster_speed}\n'
        s += f'Booster altitude = {self.booster_altitude}\n'

        s += f'Ship speed = {self.ship_speed}\n'
        s += f'Ship altitude = {self.ship_altitude}\n'
        return s
    
    def to_csvstring(self) -> str:
        s = f'{self.time_seconds},{self.booster_speed},{self.booster_altitude},{self.ship_speed},{self.ship_altitude},\n'
        return s




def find_databar_location(self):
    '''
    the database has a grey transparent background and is always in the same location
    so it should be possible to auto find its location.
    '''

    # try taking the gradient
    #    the bar will have 2 parrall horizontal lines across the window.
    #     -> poll each column
    # try blur
    # try threshold


# post-process screen captures of F&A tool 
def extract_text(img) -> str:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format, so need to convert from BGR to RGB format/mode:
    return pytesseract.image_to_string(img_rgb)


def extract_time_seconds(img) -> int:
    # TODO: estimate fractional seconds by looking at frames (how many seconds per frame * frame number in current second)

    # Take threshold so only text is visible (we know text is always white)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('../out/time_grey.png', gray)
    # _,thresh = cv2.threshold(gray, 240, 256, cv2.THRESH_BINARY)
    # cv2.imwrite('../out/time_threshold.png', thresh)

    img = gray

    data_str = extract_text(img)
    data_lines = data_str.split('\n')

    is_minus = data_lines[0][1] == '-'
    els = data_lines[0][2:].split(':')

    hours = int(els[0])
    minutes = int(els[1])
    seconds = int(els[2])

    duration_seconds = seconds + (60 * minutes) + (3600*hours)
    if is_minus:
        duration_seconds *= -1
    return duration_seconds


def replace_with_zeros(s: str) -> str:
    alts = ['o', 'O', 'Q', 'Q']
    for a in alts:
        s = s.replace(a, '0')
    return s

def extract_telem_data(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('../out/telem_grey.png', gray)

    _,thresh = cv2.threshold(gray, 230, 256, cv2.THRESH_BINARY)
    cv2.imwrite('../out/telem_threshold.png', thresh)

    img = thresh

    data_str = extract_text(img)

    lines = data_str.split('\n')
    if len(lines) < 2:
        return None, None
    
    speed_str = replace_with_zeros(lines[0])
    altitude_str = replace_with_zeros(lines[1])

    speed = int(speed_str.split(' ')[1])
    altitude = int(altitude_str.split(' ')[1])
    
    return speed, altitude

def processframe_fromfile(filepath: str) -> Data:
    print('***********************')
    print(f'Processing: {filepath}')
    print('***********************')

    img = cv2.imread(filepath)
    if img is None:
        print(f'image does not exist: {filepath}')
        return None
    
    print(img.shape)
    return postprocessframe(img)


def postprocessframe(img) -> Data:
    height = img.shape[0]
    width = img.shape[1]

    h0 = 2048
    w0 = 2732

    hf = height / h0
    wf = width / w0

    # data bar
    y0 = int(1530 * hf) + 120
    dy = int(260 * hf) + 20
    db = img[y0:y0+dy, :, :]
    cv2.imwrite('../out/dp.png', db)

    # Booster engines
    x1 = int(280 * wf)
    booster_engines_img = db[:, :x1, :]
    cv2.imwrite('../out/booster_engines.png', booster_engines_img)

    # Booster data
    x2 = int(x1 + 500 * wf)
    booster_data_img = db[:, x1:x2, :]
    cv2.imwrite('../out/booster_data_img.png', booster_data_img)

    booster_speed, booster_altitude = extract_telem_data(booster_data_img)

    # Booster orination
    x3 = int(x2 + 280 * wf)
    booster_orientation_img = db[:, x2:x3]
    cv2.imwrite('../out/booster_orientation_img.png', booster_orientation_img)

    # Time 
    x3 += int(100 * wf)
    x4 = int(x3 + 400 * wf)
    time_img = db[:, x3:x4]
    cv2.imwrite('../out/time_img.png', time_img)

    time_s = extract_time_seconds(time_img)

    # Ship  orintation
    x4 += int(70 * wf)
    x5 = int(x4 + 330 * wf)
    ship_orintation_img = db[:, x4:x5]
    cv2.imwrite('../out/ship_orintation_img.png', ship_orintation_img)

    # ship data 
    x6 = int(x5 + 500 * wf)
    ship_data_img = db[:, x5:x6]
    cv2.imwrite('../out/ship_data_img.png', ship_data_img)

    # ship telemtry
    ship_telemtry_img = ship_data_img[15:140,:,:]
    cv2.imwrite('../out/ship_telemtry_img.png', ship_telemtry_img)
    
    ship_speed, ship_altitude = extract_telem_data(ship_telemtry_img)

    # ship engines
    ship_engines_img = db[:, x6:]
    cv2.imwrite('../out/ship_engines_img.png', ship_engines_img)

    return Data(time_s, booster_speed, booster_altitude, ship_speed, ship_altitude)
    

