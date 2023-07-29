import utilities

def generate_ass_file(data_timestamps_sentences, do_color_words, field_for_subtitles_in_third_line):
    import tempfile

    if do_color_words:
        utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', field_for_subtitles_in_third_line])
        chinese_characters_color = 'FFFFFF'
    else:
        utilities.remove_word_indicators_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin', field_for_subtitles_in_third_line])
        chinese_characters_color = '00FFFF'

    temporary_file = tempfile.NamedTemporaryFile(suffix='.ass')

    with open(temporary_file.name, 'w') as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,             Fontname,                      Fontsize, Outline, PrimaryColour,                Spacing, Shadow, Bold, Alignment, MarginV
Style:  pinyin,           Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         56
Style:  zh-hans,          Noto Sans Mono CJK SC Regular, 32,       0,       &H{chinese_characters_color}, 2,       0,      1,    2,         25
Style:  subtitles_bottom, Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         6

[Events]
Format: Start, End, Style, Text""")
        for i in range(0, len(data_timestamps_sentences)):
            start_time = data_timestamps_sentences[i]['start']
            end_time = data_timestamps_sentences[i]['end']
            f.write(f"""
Dialogue: {start_time}, {end_time}, zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, pinyin, {data_timestamps_sentences[i]['pinyin']}
Dialogue: {start_time}, {end_time}, subtitles_bottom, {data_timestamps_sentences[i][field_for_subtitles_in_third_line]}""")

    return temporary_file

def generate_video(file_path_media,
                   file_path_timestamps,
                   file_path_sentences,
                   file_path_output,
                   start_time,
                   end_time,
                   field_for_subtitles_in_third_line,
                   height,
                   do_color_words):
    import subprocess
    import itertools

    if not field_for_subtitles_in_third_line:
        field_for_subtitles_in_third_line = 'en'
    if not do_color_words:
        do_color_words = True
    if not height:
        height = '1080'

    data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(file_path_timestamps, file_path_sentences)

    ass_file = generate_ass_file(data_timestamps_sentences, do_color_words, field_for_subtitles_in_third_line)

    height = int(height)
    # We use integer because a video can have float dimentions
    width = int(16 * (height/9))
    # We use int() because, apparently, drawbox only read integers
    height_background = int((height * 5)/18)

    cmd = list(itertools.chain.from_iterable(
        [x for x in [
            ['ffmpeg',
             '-y',
             '-f', 'lavfi',
             # TODO: Accept resolution as parameters
                      '-i', f'color=c=black:s={width}x{height}',
             '-i', file_path_media],
            ['-ss', start_time, '-to', end_time] if start_time and end_time else None,
            # TOOD: The scale should be equal to the
            # resolution of the background.
            #
            # TODO: It should be possible to show subtitles
            # as close as possible so as to give as much as
            # freedom to the user. Currently, when trying to
            # overlap subtitles, one of the subtitles is
            # automatically moved away.
            ['-filter_complex', f'[1:v]scale=-1:{height} [ovrl],[0:v][ovrl]overlay=(main_w-overlay_w)/2:0:shortest=1,drawbox=y=ih-{height_background}:height={height_background}:t=fill:color=black@0.7,subtitles={ass_file.name}',
             file_path_output]
        ] if x is not None]))

    subprocess.run(cmd)
