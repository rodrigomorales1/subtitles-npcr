import argparse
import ast
import subtitles_single_group_below

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
    '-c',
    '--do-color-words',
    dest='do_color_words',
    type = ast.literal_eval)

parser.add_argument(
    '--field-for-subtitles-in-third-line',
    dest = 'field_for_subtitles_in_third_line')

parser.add_argument(
    "-ss",
    "--start-time",
    dest = "start_time")

parser.add_argument(
    "-to",
    "--end-time",
    dest = "end_time")

parser.add_argument(
    "--height",
    dest = "height")

args = parser.parse_args()

subtitles_single_group_below.generate_video(
    file_path_media = args.media,
    file_path_output = args.output,
    file_path_timestamps = args.timestamps,
    file_path_sentences = args.sentences,
    start_time = args.start_time,
    end_time = args.end_time,
    do_color_words = args.do_color_words,
    field_for_subtitles_in_third_line = args.field_for_subtitles_in_third_line,
    height = args.height)
