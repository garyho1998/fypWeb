import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import DependencyMatcher
import pandas as pd
from urllib.parse import urlparse
import json
import io

nlp = spacy.load("en_core_web_sm")

founded_pattern = [{'SPEC': {'NODE_NAME': 'established'}, "PATTERN": {'LOWER': {"IN": ["established", "incorporated", "founded", "inception", "born"]}}},
                   {'SPEC': {'NODE_NAME': 'in', 'NBOR_RELOP': '>',
                             'NBOR_NAME': 'established'}, 'PATTERN': {'DEP': 'prep'}},
                   {'SPEC': {'NODE_NAME': 'in_year', 'NBOR_RELOP': '>', 'NBOR_NAME': 'in'}, 'PATTERN': {
                       'DEP': 'pobj', 'POS': 'NUM', 'LENGTH': 4, 'LIKE_NUM': True}}
                   ]
since_pattern = [{'SPEC': {'NODE_NAME': 'since'}, 'PATTERN': {'LOWER': 'since'}},
                 {'SPEC': {'NODE_NAME': 'since_year', 'NBOR_RELOP': '>', 'NBOR_NAME': 'since'},
                     'PATTERN': {'DEP': 'pobj', 'POS': 'NUM', 'LENGTH': 4, 'LIKE_NUM': True}}
                 ]

matcher = DependencyMatcher(nlp.vocab)
matcher.add("pattern1", None, founded_pattern)
matcher.add("pattern2", None, since_pattern)


def formaturl(url):
    urls = url.replace(" ", "").split(",")
    return [((urlparse(x).scheme if urlparse(x).scheme else 'http') + '://' + urlparse(x).netloc + urlparse(x).path).replace(" ", "") for x in urls]


def start(row):
    matched_sents = []
    matched_years = []
    urls = formaturl(row['Website'])
    if not urls:
        return None
    for url in urls:
        print("url: ", url)
        fileName = "WebScraping/scraping_data_json/" + urlparse(url).netloc.replace(
            'www.', '').replace('/', '-').replace(":", "_").replace('.', '-') + ".txt"
        with io.open(fileName, encoding='utf-8') as f:
            mainContent_json = json.loads(f.read().replace(
                u'\xa0', u' ').replace(u'\\n', u' '))
            for key in mainContent_json:
                doc = nlp(str(mainContent_json[key]))
                match_patterns = matcher(doc)
                for match_pattern in match_patterns:
                    if(match_pattern[1]):
                        match_id, list_of_match_token = match_pattern
                        for match_token in list_of_match_token:
                            try:
                                *_, last = match_token
                                span = doc[last]  # Matched span
                                sent = span.sent  # Sentence containing matched span
                                match_ents = [
                                    {"token": span, "label": "MATCH", }]
                                if(sent.text not in matched_sents):
                                    matched_years.append(span)
                                    matched_sents.append(sent.text)
                            except Exception as e:
                                print(e)
        row['year'] = matched_years
        row['match_sent'] = matched_sents
        return row


if __name__ == '__main__':
    list_it_df = pd.read_excel(
        "WebScraping/WebScraping_test_v1/list_it_solutions.xlsx", sheet_name=0, engine='openpyxl')
    website_df = list_it_df[['Reference Code', 'Website']].dropna(subset=['Website']).drop_duplicates(subset=['Website'])

    info_dict = {}
    for index, row in website_df.iterrows():
        try:
            if(row['Website'] not in info_dict):
                info_dict[row['Website']] = start(row)
        except Exception as e:
            print(e)

    row_list = []
    for index, row in website_df.iterrows():
        try:
            row_list.append(info_dict[row['Website']])
        except Exception as e:
            print(e)
    result_df = pd.DataFrame(row_list)
    result_df.to_excel('website_df.xlsx', sheet_name='sheet1', index=False)
