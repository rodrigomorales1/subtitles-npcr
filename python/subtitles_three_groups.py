import utilities

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

def generate_ass_file_three_lines(data_timestamps_sentences, keys_for_bottom_subtitles):
    import tempfile
    temporary_file_1 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_2 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_3 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_4 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_5 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_6 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_7 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_8 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_9 = tempfile.NamedTemporaryFile(suffix='.ass')

    with (open(temporary_file_1.name, 'w') as t1,
          open(temporary_file_2.name, 'w') as t2,
          open(temporary_file_3.name, 'w') as t3,
          open(temporary_file_4.name, 'w') as t4,
          open(temporary_file_5.name, 'w') as t5,
          open(temporary_file_6.name, 'w') as t6,
          open(temporary_file_7.name, 'w') as t7,
          open(temporary_file_8.name, 'w') as t8,
          open(temporary_file_9.name, 'w') as t9):

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9]:
            t.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, Outline, PrimaryColour, Shadow, Bold, Alignment, MarginV""")

        t1.write("\nStyle: group-1-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 258")
        t2.write("\nStyle: group-1-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 223")
        t3.write("\nStyle: group-1-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 203")

        t4.write("\nStyle: group-2-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 164")
        t5.write("\nStyle: group-2-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 129")
        t6.write("\nStyle: group-2-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 109")

        t7.write("\nStyle: group-3-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 67")
        t8.write("\nStyle: group-3-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 32")
        t9.write("\nStyle: group-3-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 12")

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9]:
            t.write("""\n[Events]
Format: Start, End, Style, Text""")

        for i in range(0, len(data_timestamps_sentences), 3):
            start_time = data_timestamps_sentences[i]['start']
            if i == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i]['end']
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
            elif i + 1 == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i+1]['end']
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
                t4.write(f"\nDialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}")
                t5.write(f"\nDialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}")
                t6.write(f"\nDialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[0]]}")
            else:
                end_time = data_timestamps_sentences[i+2]['end']
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
                t4.write(f"\nDialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}")
                t5.write(f"\nDialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}")
                t6.write(f"\nDialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[0]]}")
                t7.write(f"\nDialogue: {start_time}, {end_time}, group-3-pinyin, {data_timestamps_sentences[i+2]['pinyin']}")
                t8.write(f"\nDialogue: {start_time}, {end_time}, group-3-zh-hans, {data_timestamps_sentences[i+2]['zh-hans']}")
                t9.write(f"\nDialogue: {start_time}, {end_time}, group-3-third-line, {data_timestamps_sentences[i+2][keys_for_bottom_subtitles[0]]}")

    return [temporary_file_1,
            temporary_file_2,
            temporary_file_3,
            temporary_file_4,
            temporary_file_5,
            temporary_file_6,
            temporary_file_7,
            temporary_file_8,
            temporary_file_9]

def generate_ass_file_four_lines(data_timestamps_sentences, keys_for_bottom_subtitles):
    import tempfile

    temporary_file_1 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_2 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_3 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_4 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_5 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_6 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_7 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_8 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_9 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_10 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_11 = tempfile.NamedTemporaryFile(suffix='.ass')
    temporary_file_12 = tempfile.NamedTemporaryFile(suffix='.ass')

    with (open(temporary_file_1.name, 'w') as t1,
          open(temporary_file_2.name, 'w') as t2,
          open(temporary_file_3.name, 'w') as t3,
          open(temporary_file_4.name, 'w') as t4,
          open(temporary_file_5.name, 'w') as t5,
          open(temporary_file_6.name, 'w') as t6,
          open(temporary_file_7.name, 'w') as t7,
          open(temporary_file_8.name, 'w') as t8,
          open(temporary_file_9.name, 'w') as t9,
          open(temporary_file_10.name, 'w') as t10,
          open(temporary_file_11.name, 'w') as t11,
          open(temporary_file_12.name, 'w') as t12):

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]:
            t.write("""[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, Outline, PrimaryColour, Shadow, Bold, Alignment, MarginV""")

        t1.write("\nStyle: group-1-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 267")
        t2.write("\nStyle: group-1-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 233")
        t3.write("\nStyle: group-1-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 215")
        t4.write("\nStyle: group-1-fourth-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 195")

        t5.write("\nStyle: group-2-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 172")
        t6.write("\nStyle: group-2-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 138")
        t7.write("\nStyle: group-2-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 120")
        t8.write("\nStyle: group-2-fourth-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 100")

        t9.write("\nStyle: group-3-pinyin, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 74")
        t10.write("\nStyle: group-3-zh-hans, Noto Sans Mono CJK SC Regular, 32, 0, &HFFFFFF, 0, 0, 2, 40")
        t11.write("\nStyle: group-3-third-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 22")
        t12.write("\nStyle: group-3-fourth-line, Noto Sans, 18, 0, &HFFFFFF, 0, 0, 2, 2")

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]:
            t.write("""\n[Events]
Format: Start, End, Style, Text""")

        for i in range(0, len(data_timestamps_sentences), 3):
            start_time = data_timestamps_sentences[i]['start']
            if i == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i]['end']
                # Group 1
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
                t4.write(f"\nDialogue: {start_time}, {end_time}, group-1-fourth-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[1]]}")
            elif i + 1 == len(data_timestamps_sentences) - 1:
                end_time = data_timestamps_sentences[i+1]['end']
                # Group 1
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
                t4.write(f"\nDialogue: {start_time}, {end_time}, group-1-fourth-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[1]]}")
                # Group 2
                t5.write(f"\nDialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}")
                t6.write(f"\nDialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}")
                t7.write(f"\nDialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[0]]}")
                t8.write(f"\nDialogue: {start_time}, {end_time}, group-2-fourth-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[1]]}")
            else:
                end_time = data_timestamps_sentences[i+2]['end']
                # Group 1
                t1.write(f"\nDialogue: {start_time}, {end_time}, group-1-pinyin, {data_timestamps_sentences[i]['pinyin']}")
                t2.write(f"\nDialogue: {start_time}, {end_time}, group-1-zh-hans, {data_timestamps_sentences[i]['zh-hans']}")
                t3.write(f"\nDialogue: {start_time}, {end_time}, group-1-third-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[0]]}")
                t4.write(f"\nDialogue: {start_time}, {end_time}, group-1-fourth-line, {data_timestamps_sentences[i][keys_for_bottom_subtitles[1]]}")
                # Group 2
                t5.write(f"\nDialogue: {start_time}, {end_time}, group-2-pinyin, {data_timestamps_sentences[i+1]['pinyin']}")
                t6.write(f"\nDialogue: {start_time}, {end_time}, group-2-zh-hans, {data_timestamps_sentences[i+1]['zh-hans']}")
                t7.write(f"\nDialogue: {start_time}, {end_time}, group-2-third-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[0]]}")
                t8.write(f"\nDialogue: {start_time}, {end_time}, group-2-fourth-line, {data_timestamps_sentences[i+1][keys_for_bottom_subtitles[1]]}")
                # Group 3
                t9.write(f"\nDialogue: {start_time}, {end_time}, group-3-pinyin, {data_timestamps_sentences[i+2]['pinyin']}")
                t10.write(f"\nDialogue: {start_time}, {end_time}, group-3-zh-hans, {data_timestamps_sentences[i+2]['zh-hans']}")
                t11.write(f"\nDialogue: {start_time}, {end_time}, group-3-third-line, {data_timestamps_sentences[i+2][keys_for_bottom_subtitles[0]]}")
                t12.write(f"\nDialogue: {start_time}, {end_time}, group-3-fourth-line, {data_timestamps_sentences[i+2][keys_for_bottom_subtitles[1]]}")

    return [temporary_file_1,
            temporary_file_2,
            temporary_file_3,
            temporary_file_4,
            temporary_file_5,
            temporary_file_6,
            temporary_file_7,
            temporary_file_8,
            temporary_file_9,
            temporary_file_10,
            temporary_file_11,
            temporary_file_12]

def generate_ass_file(data_timestamps_sentences, keys_for_bottom_subtitles):
    utilities.insert_colors_in_keys(data_timestamps_sentences, ['zh-hans', 'pinyin'] + keys_for_bottom_subtitles)

    if len(keys_for_bottom_subtitles) == 1:
        return generate_ass_file_three_lines(data_timestamps_sentences, keys_for_bottom_subtitles)

    if len(keys_for_bottom_subtitles) == 2:
        return generate_ass_file_four_lines(data_timestamps_sentences, keys_for_bottom_subtitles)

def generate_rectangle(data_timestamps_sentences, name_last_overlay, width, height):
    result =""
    times = []
    height_step = int(height/3)

    for i in data_timestamps_sentences:
        times.append({
            'start_time': utilities.convert_timestamp_to_seconds(i['start']),
            'end_time': utilities.convert_timestamp_to_seconds(i['end'])
        })

    # Compute position for each rectangle
    counter = 1
    for time in times:
        if counter == 1:
            time['position'] = 0
        elif counter == 2:
            time['position'] = height_step
        elif counter == 3:
            time['position'] = height_step * 2
        if counter == 3:
            counter = 1
        else:
            counter = counter + 1

    counter_rectangle = 1
    counter_overlay = 1

    for index, value in enumerate(times):
        if index == 0:
            name_current_overlay = f"[overlay{counter_overlay}]"
            name_previous_overlay = f"[{name_last_overlay}]"
        elif index == len(times) - 1:
            name_current_overlay = ""
            name_previous_overlay = f"[overlay{counter_overlay-1}]"
        else:
            name_current_overlay = f"[overlay{counter_overlay}]"
            name_previous_overlay = f"[overlay{counter_overlay-1}]"
        name_rectangle = f"[myline{counter_rectangle}]"
        start_time = value['start_time']
        end_time = value['end_time']

        result = result + (f""", color=white@0.3:{width}x{height_step} {name_rectangle},
{name_previous_overlay}{name_rectangle} overlay=0:{value['position']}:shortest=1:enable='between(t,{start_time},{end_time})' {name_current_overlay}""")

        counter_rectangle = counter_rectangle + 1
        counter_overlay = counter_overlay + 1

    return result

def group_separators(width, height):
    # Thickness must be an integer and greater and equal than
    # 2. Otherwise, ffmpeg complains.
    thickness = 2
    position_1 = height/3.0 - thickness/2.0
    position_2 = height/3.0 + height/3.0 - thickness/2.0

    return (f"color=white@1:{width}x{thickness} [my_group_separator_1]"
            + f",color=white@1:{width}x{thickness} [my_group_separator_2]"
            + f",[0:v][my_group_separator_1] overlay=0:{position_1}:shortest=1 [my_overlay_1]"
            + f",[my_overlay_1][my_group_separator_2] overlay=0:{position_2}:shortest=1")

def generate_video(file_path_media,
                   file_path_timestamps,
                   file_path_sentences,
                   file_path_output,
                   start_time,
                   end_time,
                   keys_for_bottom_subtitles,
                   height,
                   highlight_background_of_sentence_being_read):
    import subprocess
    import itertools

    if keys_for_bottom_subtitles == None:
        keys_for_bottom_subtitles = 'en'
    if highlight_background_of_sentence_being_read == None:
        highlight_background_of_sentence_being_read = True

    keys_for_bottom_subtitles = keys_for_bottom_subtitles.split(',')

    data_timestamps_sentences = utilities.get_data_timestamps_sentences_from_files(file_path_timestamps, file_path_sentences)

    # We create the metadata file before creating the ass_files
    # because when creating the ass_files, colors in hexadecimal
    # notation might be inserted in values in some keys in the
    # dictionary that contains all the data.
    metadata_file = generate_metadata_file(data_timestamps_sentences)
    ass_files = generate_ass_file(data_timestamps_sentences, keys_for_bottom_subtitles)
    subtitles = ','.join([f'subtitles={x.name}' for x in ass_files])

    height = int(height)
    width = int(16 * (height/9))

    cmd = list(itertools.chain.from_iterable(
        [x for x in [
            ['ffmpeg',
             '-y',
             '-f', 'lavfi',
             '-i', f'color=c=black:s={width}x{height}',
             '-i', file_path_media,
             '-i', metadata_file.name,
             '-map_metadata', '2'],
            ['-ss', start_time, '-to', end_time] if start_time and end_time else None,
            ['-filter_complex', (group_separators(width, height)
                                 + ('[foo]' + generate_rectangle(data_timestamps_sentences, 'foo', width, height) if highlight_background_of_sentence_being_read else "")
                                 + ',' + subtitles),
             '-c:a', 'copy',
             '-shortest',
             file_path_output]
        ] if x is not None]))

    subprocess.run(cmd)
