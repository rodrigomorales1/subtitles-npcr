# Examples
#
# $ python3 generate-vtt.py -p 43-1 -f en,es,zh-hans,pinyin -o subtitles

import re
import yaml
import argparse
import logging
import sys

def generate_subtitle_for_field(directory,
                                filename_prefix,
                                field_name,
                                sentences_data,
                                vtt_lines):
    filename = f"{directory}/{filename_prefix}.{field_name}.vtt"
    with open(filename, 'w') as f:
        logging.info("""File "%s" has been created.""" % (filename))
        for line in vtt_lines:
            if re.search(r"^[0-9a-z]{32}$", line):
                segment_data = next(item for item in sentences_data if item['id'] == line)
                content = segment_data[field_name]
            else:
                content = line
            # If there's nothing stored in the field in the YAML file,
            # write an empty line. If this is not done, Python will
            # try to write "None" which throws an error.
            if content == None:
                content = ""
            f.write(content + '\n')

def generate_subtitle_for_fields(prefix_of_text, fields, output_directory):
    filename_timestamps = f"timestamps/{prefix_of_text}.vtt"
    filename_sentences = f"sentences/{prefix_of_text}.yaml"
    vtt_lines = []
    with open(filename_timestamps) as f:
        logging.info(f"""Reading contents of file "{filename_timestamps}".""")
        for line in f:
            vtt_lines.append(line.rstrip())
    logging.info("""Number of timestamps found in "%s": %s""" % (filename_timestamps, len([x for x in vtt_lines if re.search('-->', x)])))
    with open(filename_sentences) as f:
        logging.info(f"""Reading contents of file "{filename_sentences}".""")
        sentences_data = yaml.safe_load(f)
    logging.info("""Number of YAML objects found in "%s": %s""" % (filename_sentences, len(sentences_data)))
    for field in fields:
        generate_subtitle_for_field(output_directory, prefix_of_text, field, sentences_data, vtt_lines)

def check_regex_one_or_multiple_fields(arg_value, pat=re.compile(r"^[a-z-]+(,[a-z-]+)*$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid value")
    return arg_value

def check_regex_text_identifier(arg_value, pat=re.compile(r"^[0-9]{1,2}-(1|2)$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid value")
    return arg_value

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='[%(asctime)s.%(msecs)03d] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p",
    "--prefix",
    dest = "prefix",
    type = check_regex_text_identifier,
    help="Prefix that is used in the files *-sentences.yaml and *-timestamps.vtt")

parser.add_argument(
    "-o",
    "--output-directory",
    dest = "output_directory",
    help="Directory that will contain the output files.")

parser.add_argument(
    "-f",
    "--fields",
    dest = "fields",
    type = check_regex_one_or_multiple_fields,
    help="Name of fields in the *-sentences.yaml files. The values should be separated by comma.")

args = parser.parse_args()

generate_subtitle_for_fields(
    prefix_of_text = args.prefix,
    fields = args.fields.split(','),
    output_directory = args.output_directory if args.output_directory else '.')
