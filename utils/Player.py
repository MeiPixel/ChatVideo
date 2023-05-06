import re
import subprocess
import os


def gat_id2time(file_path):
    with open(file_path, encoding='utf8') as f:
        list_dic = []
        for i in f:
            if i.startswith('- [ ] ['):
                list_dic.append(re.search('\[(\d+),(\d+:\d+)\]', i).groups())

    return dict(list_dic)


# 将时间长度转换为秒钟数
def to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


# 将秒钟数转换为分钟和秒钟的形式
def to_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return '{:02d}:{:02d}'.format(minutes, seconds)


# 计算时间差
def get_time(start_time, end_time):
    start_seconds = to_seconds(start_time)
    end_seconds = to_seconds(end_time)
    total_seconds = end_seconds - start_seconds
    # 将总秒钟数转换为分钟和秒钟的形式
    result = to_time(total_seconds)
    return result



def play_video(path, play_info):
    video_path = os.path.join(path, play_info['video_name'])
    print(f'开始播放{video_path}视频中，{play_info["knowledge"]}知识点')
    md_path, _ = os.path.splitext(video_path)
    id2time = gat_id2time(md_path + '.md')
    start_time = id2time[str(play_info['start_id'])]
    end_time = id2time[str(play_info['end_id'] + 1)]
    duration = get_time(start_time, end_time)
    cmd = ['ffplay', '-ss', start_time, '-t', duration, '-i', video_path, '-vf', 'scale=500:500']
    subprocess.call(cmd)
