import numpy as np
import cv2
import os
import pytesseract
from typing import List
# import pygetwindow
from frame_analysis import postprocessframe
import PIL as PIL



def get_frame_filepaths_from_dir(dir: str='') -> List[str]:
    basedir = os.path.join('..', 'img')
    framepaths = [os.path.join(basedir, fname) for fname in os.listdir(basedir)
                  if os.path.isfile(os.path.join(basedir, fname))]
    return framepaths



def process_frames():
    framepath = get_frame_filepaths_from_dir()
    ds = []
    for fpath in framepath:
        d = postprocessframe(fpath)
        ds.append(d)


def main():
    print('SpaceXstreamAnalysis')

    cp = cv2.VideoCapture('../vid/Screen Recording 2024-11-09 at 19.41.37.mov')
    print(cp.isOpened())

    f = open('../data/data.csv', 'w')
    f.write('time (s),booster speed (km/s),booster altitude (m),ship speed (km/s),ship altitude (m),')
    
    # last_t = None
    c = -1
    while cp.isOpened():
        success, frame = cp.read()
        if not success:
            continue
        c += 1
        if c % 100 != 0:  # only process every 100 frames
            continue

        try:
            d = postprocessframe(frame)
            if d is None:
                continue
        except Exception as e:
            print(e)
            # c -= 1
            continue

        # if d.time_seconds == last_t:  # only sample at the start of each second (TODO: run at a higher rate later)
            # continue
        # last_t = d.time_seconds
        print(d.time_seconds)
        f.write(d.to_csvstring())

    f.close()


    


if __name__ == '__main__':
    main()
