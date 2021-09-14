import os 

def runyolo(video_repo_path, video_name, exp_train, save_name, nosave=True):
    if nosave == True:
        dosave = '--nosave'
    else: 
        dosave = ''
    detect_cmd = f'python detect.py --weights runs/train/{exp_train}/weights/last.pt --conf 0.5 --max-det=2 --save-txt {dosave} --name "{save_name}" --line-thickness=1 --source {video_repo_path}/"{video_name}"'
    command = 'cd ../yolov5' + ' & ' + detect_cmd

    print(command)

    os.system(command)
    os.system('cls')