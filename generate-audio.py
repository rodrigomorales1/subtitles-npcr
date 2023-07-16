import re
import argparse
import utilities

parser = argparse.ArgumentParser()

parser.add_argument(
    "--media",
    dest = "media",
    required = True)

parser.add_argument(
    "--sentences",
    dest = "sentences",
    required = True)

parser.add_argument(
    "--timestamps",
    dest = "timestamps",
    required = True)

parser.add_argument(
    "--output",
    dest = "output",
    required = True)

parser.add_argument(
    '--field-for-subtitles-in-third-line',
    dest = 'field_for_subtitles_in_third_line',
    default = 'en')

parser.add_argument(
    "--start-time",
    dest = "start_time")

parser.add_argument(
    "--end-time",
    dest = "end_time")

args = parser.parse_args()

def generate_metadata_file(data):
    import tempfile

    temporary_file = tempfile.NamedTemporaryFile(suffix='.txt')

    with open(temporary_file.name, 'w') as f:
        f.write(""";FFMETADATA1

[CHAPTER]
TIMEBASE=1/1000
START=0
END=0
title=空白\n""")

        for item in data:
            milliseconds_start = utilities.convert_timestamp_to_milliseconds(item['start'])
            milliseconds_end = milliseconds_start + 1
            title = utilities.remove_word_indicators_in_string(item['zh-hans'])
            f.write(f"""
[CHAPTER]
TIMEBASE=1/1000
START={milliseconds_start}
END={milliseconds_end}
title={title}
""")

    return temporary_file

def generate_ass_file(data_timestamps_sentences, field_for_subtitles_in_third_line):
    import tempfile

    utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', field_for_subtitles_in_third_line])

    temporary_file_1 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_2 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_3 = tempfile.NamedTemporaryFile(suffix='.ass')

    with (open(temporary_file_1.name, 'w') as t1,
          open(temporary_file_2.name, 'w') as t2,
          open(temporary_file_3.name, 'w') as t3):

        t1.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,               Fontname,                      Fontsize, Outline,     PrimaryColour, Shadow, Bold, Alignment, MarginV
Style:  group-1-pinyin,     Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         250
Style:  group-1-zh-hans,    Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         215
Style:  group-1-third-line, Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         195

[Events]
Format: Start, End, Style, Text""")

        t2.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,               Fontname,                      Fontsize, Outline,     PrimaryColour, Shadow, Bold, Alignment, MarginV
Style:  group-2-pinyin,     Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         145
Style:  group-2-zh-hans,    Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         120
Style:  group-2-third-line, Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         100

[Events]
Format: Start, End, Style, Text""")

        t3.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,               Fontname,                      Fontsize, Outline,     PrimaryColour, Shadow, Bold, Alignment, MarginV
Style:  group-3-pinyin,     Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         55
Style:  group-3-zh-hans,    Noto Sans Mono CJK SC Regular, 32,       0,           &HFFFFFF,      0,      0,    2,         30
Style:  group-3-third-line, Noto Sans,                     18,       0,           &HFFFFFF,      0,      0,    2,         10

[Events]
Format: Start, End, Style, Text""")

        for i in range(0, len(data_timestamps_sentences), 3):
            start_time = data_timestamps_sentences[i]['start']
            if i == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i]['end']
                t1.write(f"""
Dialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][field_for_subtitles_in_third_line]}""")
            elif i + 1 == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i+1]['end']
                t1.write(f"""
Dialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][field_for_subtitles_in_third_line]}""")
                t2.write(f"""
Dialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}
Dialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][field_for_subtitles_in_third_line]}""")
            else:
                end_time = data_timestamps_sentences[i+2]['end']
                t1.write(f"""
Dialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][field_for_subtitles_in_third_line]}""")
                t2.write(f"""
Dialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}
Dialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][field_for_subtitles_in_third_line]}""")
                t3.write(f"""
Dialogue: {start_time}, {end_time}, group-3-zh-hans, {data_timestamps_sentences[i+2]['zh-hans']}
Dialogue: {start_time}, {end_time}, group-3-pinyin, {data_timestamps_sentences[i+2]['pinyin']}
Dialogue: {start_time}, {end_time}, group-3-third-line, {data_timestamps_sentences[i+2][field_for_subtitles_in_third_line]}""")

    return [temporary_file_1, temporary_file_2, temporary_file_3]

def generate_video(media, output, start_time, end_time, field_for_subtitles_in_third_line):
    import subprocess
    import itertools

    data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(
        args.timestamps,
        args.sentences)

    # We create the metadata file before creating the ass_files
    # because when creating the ass_files, colors in hexadecimal
    # notation might be inserted in values in some keys in the
    # dictionary that contains all the data.
    metadata_file = generate_metadata_file(data_timestamps_sentences)
    ass_files = generate_ass_file(data_timestamps_sentences, field_for_subtitles_in_third_line)

    cmd = list(itertools.chain.from_iterable(
        [x for x in [
            ['ffmpeg',
             '-y',
             '-f', 'lavfi',
             '-i', 'color=c=black:s=1920x1080',
             '-i', media,
             '-i', metadata_file.name,
             '-map_metadata', '2'],
            ['-ss', start_time, '-to', end_time] if start_time and end_time else None,
            ['-vf', f'subtitles={ass_files[0].name},subtitles={ass_files[1].name},subtitles={ass_files[2].name},',
             '-c:a', 'copy',
             '-shortest',
             output]
        ] if x is not None]))

    subprocess.run(cmd)

generate_video(
    media = args.media,
    output = args.output,
    start_time = args.start_time,
    end_time = args.end_time,
    field_for_subtitles_in_third_line = args.field_for_subtitles_in_third_line)
