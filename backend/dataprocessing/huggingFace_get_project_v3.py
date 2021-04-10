from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import GPT2Tokenizer
import torch
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.matcher import DependencyMatcher
import pandas as pd
from urllib.parse import urlparse
import numpy as np
import json
import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
keywords_list = ["project", "solution", "service", "product"]

nlp = spacy.load("en_core_web_sm")

def getSentence(keyword, context):
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrases = [keyword]
    patterns = [nlp(text) for text in phrases]
    phrase_matcher.add("keyword", None, *patterns) 

    doc = nlp(context)
    matches = phrase_matcher(doc)
    if(matches):
        for match_id, start, end in matches:
            span = doc[start:end]
            sent = span.sent.text
            return sent        
    
def huggingFace(keyword, context):
    question = "what " + keyword + " do you provide?"

    inputs = tokenizer(question, context, add_special_tokens=True, 
                        return_tensors='pt', max_length=512, truncation=True)
    input_ids = inputs['input_ids'].tolist()[0]

    outputs = model(**inputs)
    start = outputs.start_logits.detach().numpy()
    end = outputs.end_logits.detach().numpy()

    undesired_tokens = inputs['attention_mask']
    undesired_tokens_mask = undesired_tokens == 0.0

    start_ = np.where(undesired_tokens_mask, -10000.0, start)
    end_ = np.where(undesired_tokens_mask, -10000.0, end)

    start_ = np.exp(start_ - np.log(np.sum(np.exp(start_), axis=-1, keepdims=True)))
    end_ = np.exp(end_ - np.log(np.sum(np.exp(end_), axis=-1, keepdims=True)))

    outer = np.matmul(np.expand_dims(start_, -1), np.expand_dims(end_, 1))

    max_answer_len = 15
    candidates = np.tril(np.triu(outer), max_answer_len - 1)
    scores_flat = candidates.flatten()

    idx_sort = [np.argmax(scores_flat)]
    start, end = np.unravel_index(idx_sort, candidates.shape)[1:]
    end += 1
    score = candidates[0, start, end-1]
    start, end, score = start.item(), end.item(), score.item()

    answer = tokenizer.decode(input_ids[start:end])
    if(score < 0):
        return "", 0, "", context
    if("[CLS]" == answer or "[SEP]" == answer or question in answer):
        with open("fail_log.txt", "w", encoding="utf-8") as f:
            f.write(context+"\n\n\n\n\n\n")
        return "", 0, "", context

    context = tokenizer.decode(input_ids)
    sent = getSentence(answer, context)

    return answer, score, sent, context


def formaturl(url):
    urls = url.replace(" ", "").split(",")
    return [((urlparse(x).scheme if urlparse(x).scheme else 'http') + '://' + urlparse(x).netloc + urlparse(x).path).replace(" ", "") for x in urls]

def return_textjson_from_urls(urls):
    texts = []
    if not urls:
        return None
    for url in urls: #it will combines text from two website
        print("url: ", url)
        #windows
        #fileName = "WebScraping/scraping_data_json/" + urlparse(url).netloc.replace('www.', '').replace('/', '-').replace(":", "_").replace('.', '-') + ".txt"

        fileName = "WebScraping/scraping_data_json/" + urlparse(url).netloc.replace('www.', '').replace('/', '-').replace(":", "_").replace('.', '-') + ".txt"
        with io.open(fileName, encoding='utf-8') as f:
            mainContent_json = json.loads(f.read().replace(u'\xa0', u' ').replace(u'\\n', u' '))
            texts.append(mainContent_json)
    return texts

def return_pattern_sents(doc):
    matcher = Matcher(nlp.vocab)
    pattern = [{"lower": {"IN": [keyword for keyword in keywords_list]+[keyword+"s" for keyword in keywords_list]}, "POS":"NOUN"}]
    pattern_sents = {}
    for keyword in keywords_list:
        pattern_sents[keyword] = ""
    matcher.add("pattern1", [pattern])
    matches = matcher(doc)
    if(matches):
        for match_id, start, end in matches:
            span = doc[start:end]
            for keyword in keywords_list:
                if(keyword in span.text):
                    pattern_sents[keyword] += " " + span.sent.text
        return pattern_sents
    return None

def run(result_df, urls):
    try:
        textjsons = return_textjson_from_urls(urls)
    except Exception as e:
        print(e)
        return result_df
    
    if not textjsons:
        return result_df

    paragraphText_pattern_sents = {}
    for keyword in keywords_list:
        paragraphText_pattern_sents[keyword] = ""
    for textjson in textjsons:
        for key in textjson:
            text = str(textjson[key])
            doc = nlp(text)
            pattern_sents = return_pattern_sents(doc)
            if(pattern_sents):
                for keyword in keywords_list:
                    paragraphText_pattern_sents[keyword] += pattern_sents[keyword]
    if(paragraphText_pattern_sents == {}):
        return result_df
    try:
        if(not result_df['Website'].str.contains(urls[0]).any()):
            for keyword in keywords_list:
                if(paragraphText_pattern_sents[keyword]!=""):
                    answer, score, sent, context = huggingFace(keyword, paragraphText_pattern_sents[keyword])
                    if(answer):
                        result_df = result_df.append({'Website': urls[0], 'Answer' : answer , 'Score' : score, 'Sent':sent, 'Context':context} , ignore_index=True)
    except Exception as e:
        print('Error:', e) 
    return result_df

if __name__ == '__main__':

    list_it_df = pd.read_excel("WebScraping\Spacy\list_it_solutions.xlsx", sheet_name=0, engine='openpyxl')
    website_df = list_it_df[['Reference Code', 'Website']].dropna(subset=['Website']).drop_duplicates(subset=['Website'])
    result_df = pd.DataFrame(columns = ['Website' , 'Answer', 'Score'])
    i=0
    total = len(website_df)
    for index, row in website_df.iterrows():
        try:
            urls = formaturl(row['Website'])
            result_df = run(result_df, urls)
            i=i+1
            print(i,'/',total)

        except Exception as e:
            print(e)
    result_df.to_excel('website_project_df.xlsx', sheet_name='projects', index=False)
            