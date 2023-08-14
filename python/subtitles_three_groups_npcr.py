import argparse
import ast
import datetime
import subtitles_three_groups

parser = argparse.ArgumentParser()

parser.add_argument(
    "--text-id",
    dest = "text_id",
    required = True)

parser.add_argument(
    '--field-for-subtitles-in-third-line',
    dest = 'field_for_subtitles_in_third_line')

parser.add_argument(
    "--start-time",
    dest = "start_time")

parser.add_argument(
    "--end-time",
    dest = "end_time")

parser.add_argument(
    "--highlight-background-of-sentence-being-read",
    type = ast.literal_eval,
    default = True)

parser.add_argument(
    "--height",
    dest = "height",
    default = "1080")

parser.add_argument(
    "--file-path-output",
    dest = "file_path_output")

parser.add_argument(
    '--keys-for-bottom-subtitles',
    dest = 'keys_for_bottom_subtitles')

args = parser.parse_args()

text_id = args.text_id
file_path_sentences = f'sentences/{text_id}.yaml'
file_path_timestamps = f'timestamps/audios/{text_id}.vtt'
file_path_media = f'audios/{text_id}.flac'

if args.file_path_output:
    file_path_output = args.file_path_output
else:
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d-%Z')
    file_path_output = f'{text_id}_audio_{date}.mp4'

subtitles_three_groups.generate_video(
    file_path_media = file_path_media,
    file_path_timestamps = file_path_timestamps,
    file_path_sentences = file_path_sentences,
    file_path_output = file_path_output,
    start_time = args.start_time,
    end_time = args.end_time,
    keys_for_bottom_subtitles = args.keys_for_bottom_subtitles,
    height = args.height,
    highlight_background_of_sentence_being_read = args.highlight_background_of_sentence_being_read)
