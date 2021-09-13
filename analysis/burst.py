import yaml 
import glob 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

class Burst:
    # self.get_stim_on_frames() 메소드를 통해 언제 stimulation이 on/off 되었는지 n_frame, stim을 field로 dataframe을 return
    def __init__(self, video_name):
        self.video_name = video_name
        self.read_video_info() 
        self.check_video_name()
    
    def read_video_info(self):
        file_path = "D:\Research\SC\DATA\Eye_Movement\VideoInfo.csv"
        self.video_info = pd.read_csv(file_path)

    def check_video_name(self):
        bursts = self.video_info[self.video_info['Frequency'] == 20]
        bursts_video_names = bursts['VideoName']
        if (bursts_video_names.str.contains(self.video_name).any()) == True:
            print(f"{self.video_name} is found.")
            self.this_info = self.video_info.loc[self.video_info['VideoName'] == self.video_name, :]
        else: 
            raise Exception(f"There is no file named {self.video_name} as 20Hz 5ms.")

    def get_startend_frame(self):
        start_frame = int(self.this_info['StartFrame'])
        end_frame = int(self.this_info['EndFrame'])

        return start_frame, end_frame

    def get_stim_startend_frame(self):
        stim_start_frame = int(self.this_info['StimulationStartFrame'])
        stim_end_frame = int(self.this_info['StimulationEndFrame'])

        return stim_start_frame, stim_end_frame 
    
    def get_stim_on_frames(self):
        stim_start_frame, stim_end_frame = self.get_stim_startend_frame()
        finterval = int(stim_end_frame - stim_start_frame) # frame interval
        start_frame, end_frame = self.get_startend_frame()
        
        # finterval 나눈 나머지로 on/off 판단
        (q, r) = divmod(stim_start_frame, finterval) # q 몫, r 나머지
        stim_on_flag = q % 2

        frames = np.arange(start_frame, end_frame+1)
        shifted_frames = frames - r
        flags = shifted_frames // finterval 
        flags = flags % 2

        onoff = [frames, flags]

        df_onoff = pd.DataFrame(onoff, index=['n_frame', 'stim']).transpose()

        if stim_on_flag == 1:
            df_onoff['stim'].replace({1:'on'}, inplace=True)
            df_onoff['stim'].replace({0:'off'}, inplace=True)
        elif stim_on_flag == 0:
            df_onoff['stim'].replace({0:'on'}, inplace=True)
            df_onoff['stim'].replace({1:'off'}, inplace=True)

        return df_onoff

            

