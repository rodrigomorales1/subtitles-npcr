import utilities

def generate_ass_file(data_timestamps_sentences, do_color_words, keys_for_bottom_subtitles):
    import tempfile

    if do_color_words:
        utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin'] + keys_for_bottom_subtitles)
        chinese_characters_color = 'FFFFFF'
    else:
        utilities.remove_word_indicators_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin'] + keys_for_bottom_subtitles)
        chinese_characters_color = '00FFFF'

    temporary_file = tempfile.NamedTemporaryFile(suffix='.ass')

    with open(temporary_file.name, 'w') as f:
        if len(keys_for_bottom_subtitles) == 1:
            f.write(f"""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,             Fontname,                      Fontsize, Outline, PrimaryColour,                Spacing, Shadow, Bold, Alignment, MarginV
Style:  pinyin,           Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         56
Style:  zh-hans,          Noto Sans Mono CJK SC Regular, 32,       0,       &H{chinese_characters_color}, 2,       0,      1,    2,         25
Style:  subtitles_bottom, Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         6

[Events]
Format: Start, End, Style, Text""")
        elif len(keys_for_bottom_subtitles) == 2:
            f.write(f"""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,               Fontname,                      Fontsize, Outline, PrimaryColour,                Spacing, Shadow, Bold, Alignment, MarginV
Style:  pinyin,             Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         56
Style:  zh-hans,            Noto Sans Mono CJK SC Regular, 32,       0,       &H{chinese_characters_color}, 2,       0,      1,    2,         38
Style:  subtitles_bottom_1, Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         20
Style:  subtitles_bottom_2, Noto Sans,                     18,       0,       &HFFFFFF,                     0,       0,      0,    2,         2

[Events]
Format: Start, End, Style, Text""")

        for i in range(0, len(data_timestamps_sentences)):
            start_time = data_timestamps_sentences[i]['start']
            end_time = data_timestamps_sentences[i]['end']
            f.write(f"""
Dialogue: {start_time}, {end_time}, zh-hans, {data_timestamps_sentences[i]['zh-hans']}
Dialogue: {start_time}, {end_time}, pinyin, {data_timestamps_sentences[i]['pinyin']}""")
            if len(keys_for_bottom_subtitles) == 1:
                f.write(f"""
Dialogue: {start_time}, {end_time}, subtitles_bottom, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}""")
            elif len(keys_for_bottom_subtitles) == 2:
                f.write(f"""
Dialogue: {start_time}, {end_time}, subtitles_bottom_1, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}
Dialogue: {start_time}, {end_time}, subtitles_bottom_2, {data_timestamps_sentences[i][keys_for_bottom_subtitles[1]]}""")

    return temporary_file

def generate_video(file_path_media,
                   file_path_timestamps,
                   file_path_sentences,
                   file_path_output,
                   start_time,
                   end_time,
                   keys_for_bottom_subtitles,
                   show_subtitles_on_top_of_video,
                   height,
                   do_color_words):
    import subprocess
    import itertools

    if show_subtitles_on_top_of_video == None:
        show_subtitles_on_top_of_video = True
    if keys_for_bottom_subtitles == None:
        keys_for_bottom_subtitles = 'en'
    if do_color_words == None:
        do_color_words = True
    if height == None:
        height = '1080'

    keys_for_bottom_subtitles = keys_for_bottom_subtitles.split(',')

    data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(file_path_timestamps, file_path_sentences)

    ass_file = generate_ass_file(data_timestamps_sentences, do_color_words, keys_for_bottom_subtitles)

    height = int(height)
    # We use integer because a video can have float dimentions
    width = int(16 * (height/9))
    # We use int() because, apparently, drawbox only read integers
    if len(keys_for_bottom_subtitles) == 1:
        height_background_for_subtitles = int((height * 5)/18)
    elif len(keys_for_bottom_subtitles) == 2:
        height_background_for_subtitles = int((height * 17)/54)
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
            ['-filter_complex', (f'[1:v]scale=-1:{height if show_subtitles_on_top_of_video else height-height_background_for_subtitles} [ovrl]'
                                 + ',[0:v][ovrl]overlay=(main_w-overlay_w)/2:0:shortest=1'
                                 + f',drawbox=y=ih-{height_background_for_subtitles}:height={height_background_for_subtitles}:t=fill:color=black@0.8'
                                 + f',subtitles={ass_file.name}'),
             file_path_output]
        ] if x is not None]))

    subprocess.run(cmd)
