def get_data_timestamps_sentences_from_files(filename_timestamps, filename_sentences):
    import yaml
    import re

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
        data_sentences = yaml.safe_load(f)['sentences']

    # We iterate through the timestamps.
    #
    # We don't iterate through the sentences, because a given sentence
    # can be used twice.

    for data_item in data_timestamps_sentences:
        sentence  = next(item for item in data_sentences if item['id'] == data_item['id'])
        for key, value in sentence.items():
            if key == 'id':
                continue
            data_item[key] = value

    return data_timestamps_sentences

def remove_word_indicators_in_string(string):
    import re
    return re.sub(r'\([0-9]+:([^):]+)(:[0-9]+)?\)', lambda x: x.group(1), string)

def remove_word_indicators_in_keys(data, keys):
    import re
    for obj in data:
        for key in obj.keys():
            if key in keys:
                obj[key] = remove_word_indicators_in_string(obj[key])

colors = ['77CCDD', 'EECC88', '339999', 'CC9966', '99AA44', 'CC6677', 'CC6677', 'CC6677']

def insert_colors_in_string(string):
    import re
    return re.sub(r'\(([0-9]+):([^)]+)\)', lambda x: f'{{\\1c&H{colors[int(x.group(1))-1]}&}}{x.group(2)}{{\\c}}', string)

def get_string_with_underline_and_colors(match):
    if current_key == 'pinyin':
        numberings_of_groups_found_in_string.append(match.group(1))
    color = colors[int(match.group(1))-1]
    word = match.group(2)
    do_underline = True if match.group(1) in numberings_of_new_words else False
    return (r'{\u1}' if do_underline else "") + f"""{{\\1c&H{color}&}}{word}{{\\c}}""" + (r'{\u0}' if do_underline else "")

def replace_all_parentheses_groups_with_colors_and_underline(string, key):
    import re
    global numberings_of_groups_found_in_string, current_key
    numberings_of_groups_found_in_string = []
    current_key = key
    result = re.sub(r'\(([0-9]+):([^):]+)(:[0-9]+)?\)', get_string_with_underline_and_colors, string)
    if current_key == 'pinyin' and len(numberings_of_words) != len(numberings_of_groups_found_in_string):
        raise Exception(f'All numbers are not defined in line:  {string}')
    return result

def insert_colors_in_keys(data, keys):
    import re
    # Iterate through all gropus of subtitles
    for obj in data:
        # In each group, we get the numbers of the words that need to
        # be underlined in all fields but the special one. The special
        # one is the field that points out the words from the new
        # vocabulary
        #
        # We need to obtain the numberings before we start replacing
        # the value of the keys
        global numberings_of_new_words, numberings_of_words
        numberings_of_new_words = [x.group(1) for x in re.finditer('\(([0-9]+):[^:)]+:[0-9]+\)', obj['zh-hans'])]
        numberings_of_words = [x.group(1) for x in re.finditer('\(([0-9]+):[^:)]+(:[0-9]+)?\)', obj['zh-hans'])]
        for key in obj.keys():
            if key in keys:
                obj[key] = replace_all_parentheses_groups_with_colors_and_underline(obj[key], key)

def convert_timestamp_to_seconds(msf):
    hours, minutes, seconds = msf.split(':')
    seconds, milliseconds = seconds.split('.')
    # TODO: Why do we divide in 100? Are they really milliseconds? Are these centiseconds?
    milliseconds = int(milliseconds) / 100
    minutes, seconds = map(int, (minutes, seconds))
    return minutes * 60 + seconds + milliseconds

def convert_timestamp_to_milliseconds(msf):
    hours, minutes, seconds = msf.split(':')
    seconds, milliseconds = seconds.split('.')
    minutes, seconds, milliseconds = map(int, (minutes, seconds, milliseconds))
    return (minutes * 60 + seconds) * 1000 + milliseconds
