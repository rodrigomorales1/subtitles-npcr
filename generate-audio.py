import re
import json
import yaml
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-a",
    dest = "path_audio",
    required = True)

parser.add_argument(
    "-t",
    dest = "path_timestamps",
    required = True)

parser.add_argument(
    "-s",
    dest = "path_sentences",
    required = True)

parser.add_argument(
    "-o",
    dest = "path_output",
    required = True)

args = parser.parse_args()

colors = ['77CCDD', 'EECC88', '339999', '99AA44', 'CC9966']

def insert_colors_in_values(value):
    regex = r'{([0-9]+):([^}]+)}'
    return re.sub(regex, lambda x: f'{{\\1c&H{colors[int(x.group(1))-1]}&}}{x.group(2)}{{\\c}}', value)

def generate_ass_file(data_timestamps_sentences):
    import tempfile

    temporary_file = tempfile.NamedTemporaryFile(suffix='.ass')

    with open(temporary_file.name, 'w') as f:
        f.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,      Fontname,                      Fontsize, Outline,     PrimaryColour, Shadow, Bold, Alignment, MarginV
Style:  1-pinyin,    Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 250
Style:  1-zh-hans,   Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2, 215
Style:  1-en,        Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 195
Style:  2-pinyin,    Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 145
Style:  2-zh-hans,   Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2, 120
Style:  2-en,        Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 100
Style:  3-pinyin,    Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 55
Style:  3-zh-hans,   Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2, 30
Style:  3-en,        Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2, 10

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

def generate_video(path_audio, path_output, ass_file):
    import subprocess
    cmd = ['ffmpeg',
           # '-v', 'error',
           '-y',
           '-f', 'lavfi',
           '-i', 'color=c=black:s=1280x720',
           '-i', path_audio,
           # '-ss', '00:00:40',
           # '-to', '00:00:50',
           '-vf', f'subtitles={ass_file}',
           '-c:a', 'copy',
           '-shortest',
           path_output]
    subprocess.run(cmd)

def collect_timestamps_sentences(filename_timestamps, filename_sentences):
    data_timestamps_sentences = []

    with open(filename_timestamps, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if results := re.search(r"^([0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2})[0-9] --> ([0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2})[0-9]", lines[i]):
                start = results.group(1)
                end = results.group(2)
                id = lines[i+1].rstrip()
                data_timestamps_sentences.append({
                    'id': id,
                    'start': start,
                    'end': end,
                })

    with open(filename_sentences) as f:
        data_sentences = yaml.safe_load(f)

    # We iterate through the timestamps.
    #
    # We don't iterate through the sentences, because a given sentence
    # can be used twice.

    for data_item in data_timestamps_sentences:
        sentence  = next(item for item in data_sentences if item['id'] == data_item['id'])
        for key, value in sentence.items():
            if key == 'id':
                continue
            if re.search(r'{[0-9]+:[^}]+}', value):
                data_item[key] = insert_colors_in_values(value)
            else:
                data_item[key] = value

    return data_timestamps_sentences

data_timestamps_sentences = collect_timestamps_sentences(
    args.path_timestamps,
    args.path_sentences)

temporary_file = generate_ass_file(data_timestamps_sentences)

generate_video(
    args.path_audio,
    args.path_output,
    temporary_file.name)
