# Examples
#
# $ python3 generate-video.py -p 43-1 -i ./timestamps/43-1.vtt -ss 00:00:10 -to 00:00:20 -o output.mp4

import subprocess
import argparse
import itertools
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p",
    dest = "prefix",
    required = True)

parser.add_argument(
    "-i",
    dest = "filename_input",
    required = True)

parser.add_argument(
    "-o",
    dest = "filename_output",
    required = True)

parser.add_argument(
    "-ss",
    dest = "start_time")

parser.add_argument(
    "-to",
    dest = "end_time")

args = parser.parse_args()

filename_prefix = args.prefix
filename_subtitles_pinyin = f'subtitles/{filename_prefix}.pinyin.vtt'
filename_subtitles_zh_hans = f'subtitles/{filename_prefix}.zh-hans.vtt'
filename_subtitles_en = f'subtitles/{filename_prefix}.en.vtt'

files_that_should_exist = [
    filename_subtitles_pinyin,
    filename_subtitles_zh_hans,
    filename_subtitles_en,
    args.filename_input,
]

for f in files_that_should_exist:
    if not os.path.isfile(f):
        raise Exception(f"The following file doesn't exist: {f}.")

subtitles=(f"subtitles={filename_subtitles_pinyin}:force_style='fontname=Noto Sans,fontsize=20,MarginV=56,Outline=0',"
           + f"subtitles={filename_subtitles_zh_hans}:force_style='fontname=Noto Sans Mono CJK SC Regular,fontsize=32,MarginV=25,Outline=0,PrimaryColour=&H0000FFFF,Bold=1,Spacing=3',"
           + f"subtitles={filename_subtitles_en}:force_style='fontname=Noto Sans,fontsize=19,MarginV=7,Outline=0'")

cmd = list(itertools.chain.from_iterable(
    [x for x in [['ffmpeg',
                  '-y',
                  '-f', 'lavfi',
                  '-i', 'color=c=black:s=1920x1080',
                  '-i', args.filename_input],
                 ['-ss', args.start_time, '-to', args.end_time] if args.start_time and args.end_time else None,
                 ['-filter_complex', f'[1:v]scale=-1:1080 [ovrl],[0:v][ovrl]overlay=(main_w-overlay_w)/2:0:shortest=1,drawbox=y=ih-300:height=300:t=fill:color=black@0.7,{subtitles}',
                  args.filename_output]] if x is not None]))

subprocess.run(cmd)
