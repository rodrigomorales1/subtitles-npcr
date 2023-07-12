# Examples
#
# $ python3 generate-video.py -p 46-1 -i ./timestamps/46-1.webm -o output.mp4

import argparse
import utilities
import ast

parser = argparse.ArgumentParser()

parser.add_argument(
    "-m",
    "--media",
    dest = "media",
    required = True)

parser.add_argument(
    "-s",
    "--sentences",
    dest = "sentences",
    required = True)

parser.add_argument(
    "-t",
    "--timestamps",
    dest = "timestamps",
    required = True)

parser.add_argument(
    "-o",
    "--output",
    dest = "output",
    required = True)

parser.add_argument(
    "-ss",
    "--start-time",
    dest = "start_time")

parser.add_argument(
    "-to",
    "--end-time",
    dest = "end_time")

parser.add_argument(
    '-c',
    '--do-color-words',
    dest='do_color_words',
    type = ast.literal_eval)

args = parser.parse_args()

def generate_ass_file(data_timestamps_sentences, do_color_words):
    import tempfile

    if do_color_words:
        utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', 'es', 'es'])
        chinese_characters_color = 'FFFFFF'
    else:
        utilities.remove_word_indicators_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', 'es', 'es'])
        chinese_characters_color = '00FFFF'

    temporary_file = tempfile.NamedTemporaryFile(suffix='.ass')

    with open(temporary_file.name, 'w') as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,      Fontname,                      Fontsize, Outline,     PrimaryColour, Spacing, Shadow, Bold, Alignment, MarginV
Style:  pinyin,    Noto Sans,                     20,       0,           &HFFFFFF,      0,       0,      0,    2,         56
Style:  zh-hans,   Noto Sans Mono CJK SC Regular, 32,       0,           &H{chinese_characters_color},      2,       0,      1,    2,         25
Style:  es,        Noto Sans,                     19,       0,           &HFFFFFF,      0,       0,      0,    2,         6

[Events]
Format: Start, End, Style, Text""")
        for i in range(0, len(data_timestamps_sentences)):
            start_time = data_timestamps_sentences[i]['start']
            end_time = data_timestamps_sentences[i]['end']
            f.write(f"""
Dialogue: {start_time}, {end_time}, zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, es, {data_timestamps_sentences[i]['es']}""")

    return temporary_file

def generate_video(media, output, start_time, end_time, do_color_words=True):
    import subprocess
    import itertools

    data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(
        args.timestamps,
        args.sentences)

    ass_file = generate_ass_file(data_timestamps_sentences, do_color_words)

    cmd = list(itertools.chain.from_iterable(
        [x for x in [
            ['ffmpeg',
             '-y',
             '-f', 'lavfi',
             # TODO: Accept resolution as parameters
                      '-i', 'color=c=black:s=1920x1080',
             '-i', media],
            ['-ss', start_time, '-to', end_time] if start_time and end_time else None,
            # TOOD: The scale should be equal to the
            # resolution of the background.
            #
            # TODO: It should be possible to show subtitles
            # as close as possible so as to give as much as
            # freedom to the user. Currently, when trying to
            # overlap subtitles, one of the subtitles is
            # automatically moved away.
            ['-filter_complex', f'[1:v]scale=-1:1080 [ovrl],[0:v][ovrl]overlay=(main_w-overlay_w)/2:0:shortest=1,drawbox=y=ih-300:height=300:t=fill:color=black@0.7,subtitles={ass_file.name}',
             output]
        ] if x is not None]))

    subprocess.run(cmd)

generate_video(
    media = args.media,
    output = args.output,
    start_time = args.start_time,
    end_time = args.end_time,
    do_color_words = args.do_color_words)
