import argparse
import ast
import datetime
import subprocess
import subtitles_single_group_below

parser = argparse.ArgumentParser()

parser.add_argument(
    "--text-id",
    dest = "text_id",
    required = True)

parser.add_argument(
    '-c',
    '--do-color-words',
    dest='do_color_words',
    type = ast.literal_eval)

parser.add_argument(
    '--show-subtitles-on-top-of-video',
    dest = 'show_subtitles_on_top_of_video',
    type = ast.literal_eval)

parser.add_argument(
    '--keys-for-bottom-subtitles',
    dest = 'keys_for_bottom_subtitles')

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

parser.add_argument(
    "--file-path-output",
    dest = "file_path_output")

args = parser.parse_args()

text_id = args.text_id
file_path_sentences = f'sentences/{text_id}.yaml'
file_path_timestamps = f'timestamps/videos/{text_id}.vtt'
file_path_media = f'videos/{text_id}.webm'

if args.file_path_output:
    file_path_output = args.file_path_output
else:
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d-%H-%M-%S-%Z')
    commit_hash = subprocess.getoutput('git --no-pager log -n1 --pretty=format:%h')
    file_path_output = f'{text_id}_video_{commit_hash}_{date}.mp4'

subtitles_single_group_below.generate_video(
    file_path_media = file_path_media,
    file_path_output = file_path_output,
    file_path_timestamps = file_path_timestamps,
    file_path_sentences = file_path_sentences,
    start_time = args.start_time,
    end_time = args.end_time,
    show_subtitles_on_top_of_video = args.show_subtitles_on_top_of_video,
    do_color_words = args.do_color_words,
    keys_for_bottom_subtitles = args.keys_for_bottom_subtitles,
    height = args.height)
