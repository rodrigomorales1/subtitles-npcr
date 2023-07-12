import re
import argparse
import utilities

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

args = parser.parse_args()

def generate_ass_file(data_timestamps_sentences):
    import tempfile

    utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', 'es', 'es'])

    temporary_file = tempfile.NamedTemporaryFile(suffix='.ass')

    with open(temporary_file.name, 'w') as f:
        f.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,      Fontname,                      Fontsize, Outline,     PrimaryColour, Shadow, Bold, Alignment, MarginV
Style:  1-pinyin,  Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         250
Style:  1-zh-hans, Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         215
Style:  1-en,      Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         195
Style:  2-pinyin,  Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         145
Style:  2-zh-hans, Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         120
Style:  2-en,      Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         100
Style:  3-pinyin,  Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         55
Style:  3-zh-hans, Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         30
Style:  3-en,      Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         10

[Events]
Format: Start, End, Style, Text""")
        for i in range(0, len(data_timestamps_sentences), 3):
            start_time = data_timestamps_sentences[i]['start']
            if i == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i]['end']
                f.write(f"""
Dialogue: {start_time}, {end_time}, 1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, 1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, 1-en, {data_timestamps_sentences[i]['es']}""")
            elif i + 1 == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i+1]['end']
                f.write(f"""
Dialogue: {start_time}, {end_time}, 1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, 1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, 1-en, {data_timestamps_sentences[i]['es']}
Dialogue: {start_time}, {end_time}, 2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}
Dialogue: {start_time}, {end_time}, 2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}
Dialogue: {start_time}, {end_time}, 2-en, {data_timestamps_sentences[i+1]['es']}""")
            else:
                end_time = data_timestamps_sentences[i+2]['end']
                f.write(f"""
Dialogue: {start_time}, {end_time}, 1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, 1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, 1-en, {data_timestamps_sentences[i]['es']}
Dialogue: {start_time}, {end_time}, 2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}
Dialogue: {start_time}, {end_time}, 2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}
Dialogue: {start_time}, {end_time}, 2-en, {data_timestamps_sentences[i+1]['es']}
Dialogue: {start_time}, {end_time}, 3-zh-hans, {data_timestamps_sentences[i+2]['zh-hans']}
Dialogue: {start_time}, {end_time}, 3-pinyin, {data_timestamps_sentences[i+2]['pinyin']}
Dialogue: {start_time}, {end_time}, 3-en, {data_timestamps_sentences[i+2]['es']}""")

    return temporary_file

def generate_video(path_audio, path_output, ass_file, start_time=None, end_time=None):
    import subprocess
    import itertools

    cmd = list(itertools.chain.from_iterable(
        [x for x in [
            ['ffmpeg',
             '-y',
             '-f', 'lavfi',
             '-i', 'color=c=black:s=1920x1080',
             '-i', path_audio],
            ['-ss', start_time, '-to', end_time] if start_time and end_time else None,
            ['-vf', f'subtitles={ass_file}',
             '-c:a', 'copy',
             '-shortest',
             path_output]
        ] if x is not None]))

    subprocess.run(cmd)

data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(
    args.timestamps,
    args.sentences)

temporary_file = generate_ass_file(data_timestamps_sentences)

import shutil

shutil.copy(temporary_file.name, '/home/rdrg/e/a.ass')

if args.start_time and args.end_time:
    generate_video(args.media, args.output, temporary_file.name, args.start_time, args.end_time)
else:
    generate_video(args.media, args.output, temporary_file.name)
