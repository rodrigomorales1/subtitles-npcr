import argparse
import ast
import subtitles_three_groups

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

parser.add_argument(
    "--highlight-background-of-sentence-being-read",
    type = ast.literal_eval,
    default = False)

parser.add_argument(
    "--height",
    dest = "height",
    default = "1080")

args = parser.parse_args()

subtitles_three_groups.generate_video(
    file_path_media = args.media,
    file_path_timestamps = args.timestamps,
    file_path_sentences = args.sentences,
    file_path_output = args.output,
    start_time = args.start_time,
    end_time = args.end_time,
    field_for_subtitles_in_third_line = args.field_for_subtitles_in_third_line,
    height = args.height,
    highlight_background_of_sentence_being_read = args.highlight_background_of_sentence_being_read)
