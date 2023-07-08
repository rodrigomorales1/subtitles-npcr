import subprocess
import argparse
import itertools

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p",
    dest = "prefix")

parser.add_argument(
    "-o",
    dest = "filename_output")

parser.add_argument(
    "-ss",
    dest = "start_time")

parser.add_argument(
    "-to",
    dest = "end_time")

args = parser.parse_args()

filename_prefix = args.prefix
filename_video = f'{filename_prefix}-timestamps.webm'
filename_subtitles_pinyin = f'{filename_prefix}.pinyin.vtt'
filename_subtitles_zh_hans = f'{filename_prefix}.zh-hans.vtt'
filename_subtitles_en = f'{filename_prefix}.en.vtt'
filename_output = args.filename_output if args.filename_output else None

subtitles=(f"subtitles={filename_subtitles_pinyin}:force_style='fontname=Noto Sans,fontsize=20,MarginV=56,Outline=0',"
           + f"subtitles={filename_subtitles_zh_hans}:force_style='fontname=Noto Sans Mono CJK SC Regular,fontsize=32,MarginV=25,Outline=0,PrimaryColour=&H0000FFFF,Bold=1,Spacing=3',"
           + f"subtitles={filename_subtitles_en}:force_style='fontname=Noto Sans,fontsize=19,MarginV=7,Outline=0'")

cmd = list(itertools.chain.from_iterable(
    [x for x in [['ffmpeg',
                  '-y',
                  '-f', 'lavfi',
                  '-i', 'color=c=black:s=1920x1080',
                  '-i', filename_video],
                 ['-ss', args.start_time, '-to', args.end_time] if args.start_time and args.end_time else None,
                 ['-filter_complex', f'[1:v]scale=-1:1080 [ovrl],[0:v][ovrl]overlay=(main_w-overlay_w)/2:0:shortest=1,drawbox=y=ih-300:height=300:t=fill:color=black@0.7,{subtitles}',
                  filename_output]] if x is not None]))

subprocess.run(cmd)
