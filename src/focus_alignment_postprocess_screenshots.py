import os
import numpy as np
import cv2
import pytesseract
from typing import List, Tuple


# post-process screen captures of F&A tool 
def extract_text(img) -> str:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format, so need to convert from BGR to RGB format/mode:
    return pytesseract.image_to_string(img_rgb)


def get_filepaths_for_chassis_dir(chassis_dir: str) -> List[str]:
    all_filenames = [filename for filename in os.listdir(chassis_dir)
                 if os.path.isfile(os.path.join(chassis_dir, filename)) and os.path.splitext(filename)[1] == '.png']
    filepaths = [os.path.join(chassis_dir, filename) for filename in all_filenames]
    return filepaths


def get_image_filepaths_from_dirs(all_dirs: List[str]) -> Tuple[List[str], List[str], List[int]]:
    '''
    For each given dir, get all alignment screenshot pngs
    returns:
     - all_filepaths: List[str]
     - all_stages: List[str]
     - all_csns: List[int]
    '''
    all_filepaths: List[str] = []
    all_stages: List[str] = []
    all_csns: List[int] = []

    print('-- All Chassis dirs in just-captures')
    for cdir in all_dirs:
        # get all png filenames 
        filenames = [filename for filename in os.listdir(cdir) 
                     if os.path.isfile(os.path.join(cdir, filename)) and os.path.splitext(filename)[1] == '.png']
        
        # only extract filepaths with the correct format 
        for fname in filenames:
            if len(fname.split('.')) != 2:
                continue            
            name = fname.split('.')[0]

            if len(name.split('-')) != 2:
                continue
            name_split = name.split('-')
            csn = int(name_split[0])
            stage = name_split[1].strip()
            
            filepath = os.path.join(cdir, fname)           
            
            if stage in ['E', 'L', 'I']:
                all_filepaths.append(filepath)
                all_stages.append(stage)
                all_csns.append(csn)      
           
    return all_filepaths, all_stages, all_csns


def get_image_filepaths_from_chassis_dirs(dirs: List[str]) -> Tuple[List[str], List[int], List[str]]:
    '''
    Gets all chassis dirs and then all alignment images from each chassis dir.
    '''
    basedir = os.path.join('..', 'data', 'Focus+Alignment', 'just_captures')
    
    all_chassis_dirs = [os.path.join(basedir, chassis_dir) for chassis_dir in os.listdir(basedir) 
                        if os.path.isdir(os.path.join(basedir, chassis_dir))]

    return get_image_filepaths_from_dirs(all_chassis_dirs)
    

def post_process_captures(all_filepaths: List[str], all_stages: List[str], all_csns: List[str]):
    outdata_basedir = os.path.join('..', 'data', 'Focus+Alignment', 'processed')
    if not os.path.exists(outdata_basedir):
        os.makedirs(outdata_basedir)

    for i in range(len(all_filepaths)):        
        print(all_stages[i], all_csns[i], all_filepaths[i])
        filepath = all_filepaths[i]
        
        csn_int = all_csns[i]
        stage = all_stages[i]

        img_cv = cv2.imread(filepath)

        y = 0
        x_left = 0
        x_right = 1400
        h = 120 
        w = 1200
        left_img = img_cv[y:y+h, x_left:x_left+w]
        right_img = img_cv[y:y+h, x_right:x_right+w]
        #cv2.imshow("left", left_img)
        cv2.imwrite(f'left_{csn_int}_{stage}.png', left_img)
        cv2.imwrite(f'right_{csn_int}_{stage}.png', right_img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # cv2.imshow("right", right_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        left_text = extract_text(left_img)
        right_text = extract_text(right_img)
        
        print(left_text)
        print(right_text)

        left_text = left_text.replace(u"\xA3", 'f')
        left_text = left_text.replace("#", 'f')
        
        right_text = right_text.replace(u"\xA3", 'f')
        right_text = right_text.replace("#", 'f')
        
        left_score_line = left_text.split('\n')[1].strip()
        right_score_line = right_text.split('\n')[1].strip()

        out_str =  f'CSN,{csn_int}\n'
        out_str += 'Timestamp,01-01-23_00-00-00\n'

        for t in left_score_line.split(','):
            t = t.strip()
            out_str += f'cam0_{t[:2]},{t[4:]}\n'

        for t in right_score_line.split(','):
            t = t.strip()
            out_str += f'cam1_{t[:2]},{t[4:]}\n'
            
        if stage == 'E':
            stage = 'G'
        
        out_filename = f'{csn_int} - {stage}.csv'
        out_filepath = os.path.join(outdata_basedir, out_filename)
        
        print('-----')
        print(out_filepath)
        print('---')
        print(out_str)
        print('-----')

        f = open(out_filepath, 'w')
        f.write(out_str)
        f.close()
        print('=========================')
        

def post_process():
    print('post processing')
    
    basedir = os.path.join('..', 'data', 'Focus+Alignment', 'all_csv')
    filepaths, stages, csns = get_image_filepaths_from_dirs([basedir])
    #filepaths = ['../data/Focus+Alignment/nice/170 - L.png']
    #stages = ['L']
    #csns = [170]

    post_process_captures(filepaths, stages, csns)


if __name__ == '__main__':
    post_process()
