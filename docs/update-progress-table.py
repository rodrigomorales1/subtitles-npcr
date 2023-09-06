import requests
import json
import re
from urllib import parse

repo_owner="rdrg109"
repo_name="subtitles-npcr"
endpoint = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'

def search_issues_with_label(label):
    issues = []
    page_counter = 1
    is_last = False
    while not is_last:
        query = {
            'labels': label,
            'state': 'all',
            'per_page': 100,
            'sort': 'updated',
            'page': page_counter
        }
        url = f"{endpoint}?{parse.urlencode(query)}"
        print(url)
        headers = {
          "Accept": "application/vnd.github.golden-comet-preview+json"
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            exit()
        if response.links.get('next') == None:
            is_last = True
        parsed = json.loads(response.content)
        issues = issues + parsed
        # print(f'Found {len(parsed)} issues.')
        page_counter = page_counter + 1
    return issues

def compute_max_number_of_digits_chapter(issues):
    max_number_of_digits_chapter = 0
    for issue in issues:
        labels = [label['name'] for label in issue['labels']]
        text_id = next((x for x in labels if re.match('^[0-9]+-text(-[12])?$', x)), None)
        if text_id == None:
            raise Exception("This shouldn't happen")
        chapter = re.search('^[0-9]+', text_id)
        if len(chapter.group(0)) > max_number_of_digits_chapter:
            max_number_of_digits_chapter = len(chapter.group(0))
    return max_number_of_digits_chapter

def get_text_id(issue):
    labels = [label['name'] for label in issue['labels']]
    text_id = next((x for x in labels if re.match('^[0-9]+-text(-[12])?$', x)), None)
    if text_id == None:
        raise Exception("This shouldn't happen")
    return text_id

def get_text_id_padded_zeros(issue, max_number_of_digits_chapter):
    labels = [label['name'] for label in issue['labels']]
    text_id = next((x for x in labels if re.match('^[0-9]+-text(-[12])?$', x)), None)
    chapter = re.search('^[0-9]+', text_id).group(0)
    if len(chapter) < max_number_of_digits_chapter:
        text_id = text_id.zfill(len(text_id) + (max_number_of_digits_chapter - len(chapter)))
    return text_id

def build_url(issue):
   return 'https://github.com/rdrg109/subtitles-npcr/issues/' + str(issue['number'])

def format_link(label, url):
    return f"[[{url}][{label}]]"

def get_link_issue(issue):
    if issue['state'] == 'open':
        return f"[[{build_url(issue)}][(issue)]]"
    elif issue['state'] == 'closed':
        return f"[[{build_url(issue)}][DONE (issue)]]"
    else:
        raise Exception("This shouldn't happen")

def get_link_issues_with_label_text_id(issue, max_number_of_digits_chapter):
    text_id = get_text_id_padded_zeros(issue, max_number_of_digits_chapter)
    return format_link(
        label = text_id,
        url =  f'https://github.com/rdrg109/subtitles-npcr/blob/main/sentences/{text_id}.yaml')

def format_column(cells):
    return '|' + '|'.join(cells) + '|'

def separator_between_heading_and_table(number_of_columns):
    return f"|{'-+' * (number_of_columns-1)}-|"

def build_table():
    review = search_issues_with_label('review')
    add_groups = search_issues_with_label('add-groups')
    issues = review + add_groups
    max_number_of_digits_chapter = compute_max_number_of_digits_chapter(issues)
    issues = sorted(issues, key = lambda x: get_text_id_padded_zeros(x, max_number_of_digits_chapter))

    review_pinyin = []
    review_zh_hans = []
    review_en = []
    review_es = []
    add_groups_pinyin = []
    add_groups_zh_hans = []
    add_groups_en = []
    add_groups_es = []

    for issue in issues:
        labels = [label['name'] for label in issue['labels']]
        if 'review' in labels:
            if 'zh-hans' in labels: review_zh_hans.append(issue)
            elif 'pinyin' in labels: review_pinyin.append(issue)
            elif 'en' in labels: review_en.append(issue)
            elif 'es' in labels: review_es.append(issue)
            else: raise Exception("This shouldn't happen")
        elif 'add-groups' in labels:
            if 'zh-hans' in labels: add_groups_zh_hans.append(issue)
            elif 'pinyin' in labels: add_groups_pinyin.append(issue)
            elif 'en' in labels: add_groups_en.append(issue)
            elif 'es' in labels: add_groups_es.append(issue)
            else: raise Exception("This shouldn't happen")
        else: raise Exception("This shouldn't happen")

    headings = [
        'Text',
        format_link(
            'review zh-hans',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Areview+label%3Azh-hans'),
        format_link(
            'review pinyin',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Areview+label%3Apinyin'),
        format_link(
            'review en',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Areview+label%3Aen'),
        format_link(
            'review es',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Areview+label%3Aes'),
        format_link(
            'add-groups zh-hans',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Aadd-groups+label%3Azh-hans'),
        format_link(
            'add-groups pinyin',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Aadd-groups+label%3Apinyin'),
        format_link(
            'add-groups en',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Aadd-groups+label%3Aen'),
        format_link(
            'add-groups es',
            'https://github.com/rdrg109/subtitles-npcr/issues?q=is%3Aopen+label%3Aadd-groups+label%3Aes'),
    ]

    table = format_column(headings)
    table = table + '\n' + separator_between_heading_and_table(len(headings))

    for i in range(0, len(review_pinyin)):
        links = ([get_link_issues_with_label_text_id(review_pinyin[i], max_number_of_digits_chapter)]
                 + [get_link_issue(x) for x in [review_zh_hans[i],
                                                review_pinyin[i],
                                                review_en[i],
                                                review_es[i],
                                                add_groups_zh_hans[i],
                                                add_groups_pinyin[i],
                                                add_groups_en[i],
                                                add_groups_es[i]]])
        table = table + '\n' + format_column(links)

    return table

def update_table(table):
    with open('README.org', 'r') as f:
        old_content = f.read()

    start_indicator = '4e503f2a-ffbe-4704-9c03-153a4bd446ac-start'
    end_indicator = '4e503f2a-ffbe-4704-9c03-153a4bd446ac-end'

    new_content = (old_content[:old_content.find(start_indicator) + len(start_indicator)]
                   + '\n\n'
                   + table
                   + '\n\n# '
                   + old_content[old_content.find(end_indicator):])

    with open('README.org', 'w') as f:
        f.write(new_content)


table = build_table()
update_table(table)
