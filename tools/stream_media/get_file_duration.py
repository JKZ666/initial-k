# coding=utf-8
# Author=JKZ
import requests
import subprocess


def get_file_duration(filename):
    result = subprocess.Popen(["D:\\ffmpeg-3.3.1-win64-static\\bin\\ffprobe", filename], 
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lines = result.stderr.readlines()
    duration = 0
    for i in lines:
        if "Duration" in i:
            duration = i.split(",")[0][-11:]
    h, m, s = duration.strip().split(":")
    file_duration = int(h)*3600 + int(m)*60 + float(s)

    return file_duration

if __name__ == "__main__":
    file_url = "http://c23.myccdn.info/e1edddbc239c069d8a2378d9bcd598d6/5b14e012/mp4/Avatar_20Mbps.mp4"
    print get_file_duration(file_url)
