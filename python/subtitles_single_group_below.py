import utilities

def generate_ass_file(data_timestamps_sentences, do_color_words, keys_for_bottom_subtitles):
    import tempfile

    if do_color_words:
        utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin'] + keys_for_bottom_subtitles)
        chinese_characters_color = 'FFFFFF'
    else:
        utilities.remove_word_indicators_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin'] + keys_for_bottom_subtitles)
        chinese_characters_color = '00FFFF'

    temporary_files = []
    for i in range(0, len(keys_for_bottom_subtitles) + 2):
        temporary_files.append(tempfile.NamedTemporaryFile(suffix='.ass'))

    temporary_files_opened = [open(x.name, 'w') for x in temporary_files]

    for t in temporary_files_opened:
        t.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,                     Fontname, Fontsize, Outline, BorderStyle, PrimaryColour, OutlineColour
Style:     1-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HF4D442
Style:     2-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H4B19E6
Style:     3-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &H000000,      &H19E1FF
Style:     4-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &HD86343
Style:     5-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HC3FFAA
Style:     6-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H909946
Style:     7-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HE632F0
Style:     8-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H3182F5
Style:     9-pinyin,      Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HD4BEFA
Style:     10-pinyin,     Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H000080
Style:     1-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &H000000,      &HF4D442
Style:     2-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &HFFFFFF,      &H4B19E6
Style:     3-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &H000000,      &H19E1FF
Style:     4-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &HFFFFFF,      &HD86343
Style:     5-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &H000000,      &HC3FFAA
Style:     6-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &HFFFFFF,      &H909946
Style:     7-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &H000000,      &HE632F0
Style:     8-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &HFFFFFF,      &H3182F5
Style:     9-zh-hans,     Noto Sans CJK SC,       32,       1,           3,      &H000000,      &HD4BEFA
Style:     10-zh-hans,    Noto Sans CJK SC,       32,       1,           3,      &HFFFFFF,      &H000080
Style:     1-third-line,  Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HF4D442
Style:     2-third-line,  Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H4B19E6
Style:     3-third-line,  Noto Sans CJK SC,       18,       1,           3,      &H000000,      &H19E1FF
Style:     4-third-line,  Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &HD86343
Style:     5-third-line,  Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HC3FFAA
Style:     6-third-line,  Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H909946
Style:     7-third-line,  Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HE632F0
Style:     8-third-line,  Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H3182F5
Style:     9-third-line,  Noto Sans CJK SC,       18,       1,           3,      &H000000,      &HD4BEFA
Style:     10-third-line, Noto Sans CJK SC,       18,       1,           3,      &HFFFFFF,      &H000080
Format: Name, Fontname, Fontsize, Outline, PrimaryColour, Spacing, Shadow, Bold, Alignment, MarginV""")

    if len(keys_for_bottom_subtitles) == 1:
        temporary_files_opened[0].write("""\nStyle:  pinyin,           Noto Sans,                     18, 0, &HFFFFFF,                     0, 0, 0, 2, 56""")
        temporary_files_opened[1].write(f"""\nStyle: zh-hans,          Noto Sans Mono CJK SC Regular, 32, 0, &H{chinese_characters_color}, 2, 0, 1, 2, 25""")
        temporary_files_opened[2].write("""\nStyle:  subtitles_bottom, Noto Sans,                     18, 0, &HFFFFFF,                     0, 0, 0, 2, 6""")
    elif len(keys_for_bottom_subtitles) == 2:
        temporary_files_opened[0].write("""\nStyle:  pinyin,             Noto Sans,                     18, 0, &HFFFFFF,                     0, 0, 0, 2, 70""")
        temporary_files_opened[1].write(f"""\nStyle: zh-hans,            Noto Sans Mono CJK SC Regular, 32, 0, &H{chinese_characters_color}, 2, 0, 1, 2, 38""")
        temporary_files_opened[2].write("""\nStyle:  subtitles_bottom_1, Noto Sans,                     18, 0, &HFFFFFF,                     0, 0, 0, 2, 20""")
        temporary_files_opened[3].write("""\nStyle:  subtitles_bottom_2, Noto Sans,                     18, 0, &HFFFFFF,                     0, 0, 0, 2, 2""")

    for t in temporary_files_opened:
        t.write("""\n[Events]
Format: Start, End, Style, Text""")

    for i in range(0, len(data_timestamps_sentences)):
        start_time = data_timestamps_sentences[i]['start']
        end_time = data_timestamps_sentences[i]['end']
        temporary_files_opened[0].write(f"""\nDialogue: {start_time}, {end_time}, pinyin, {data_timestamps_sentences[i]['pinyin']}""")
        temporary_files_opened[1].write(f"""\nDialogue: {start_time}, {end_time}, zh-hans, {data_timestamps_sentences[i]['zh-hans']}""")
        if len(keys_for_bottom_subtitles) == 1:
            temporary_files_opened[2].write(f"""\nDialogue: {start_time}, {end_time}, subtitles_bottom, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}""")
        elif len(keys_for_bottom_subtitles) == 2:
            temporary_files_opened[2].write(f"""\nDialogue: {start_time}, {end_time}, subtitles_bottom_1, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}""")
            temporary_files_opened[3].write(f"""\nDialogue: {start_time}, {end_time}, subtitles_bottom_2, {data_timestamps_sentences[i][keys_for_bottom_subtitles[1]]}""")

    return temporary_files

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

    data_timestamps_sentences = utilities.get_data_timestamps_sentences(file_path_timestamps, file_path_sentences)
    utilities.ensure_timestamps_have_two_decimals(data_timestamps_sentences)

    ass_files = generate_ass_file(data_timestamps_sentences, do_color_words, keys_for_bottom_subtitles)
    subtitles = ','.join([f'subtitles={x.name}' for x in ass_files])

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
                                 + f',{subtitles}'),
             file_path_output]
        ] if x is not None]))

    subprocess.run(cmd)
