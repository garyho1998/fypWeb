import os
import re
import sys
# ----- for lemmatizing -----
import nltk
import numpy as np
import pandas as pd
# ----- for tranlate -----
# !pip install langdetect
# from langdetect import detect
# pd.set_option('display.max_colwidth', -1)
# !pip install git+https://github.com/BoseCorp/py-googletrans.git --upgrade
from googletrans import Translator

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
import string

from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

stop_words = set(stopwords.words("english"))
import pathlib
import sys
import time  # for timing

from sentence_transformers import CrossEncoder, SentenceTransformer, util


class DataPreprocessing: 
    _translator = Translator()
    def __init__(self,s):
        self.Busneed = s
    
    def translateToEn(self,s):
        if not s:
            return scon
        result = None
        # print("translate to en:",  str(s)[:10], end=' ')
        for _ in range(5):
            try:
                #print(_,end=' ')
                result = self._translator.translate(s,dest="en")
                break
            except (AttributeError, TypeError) as e:
                self._translator = Translator()
                s = s[:5000] # translate only ok for 5000 char
            

        # print("")
        if result is None:
            return s
        return result.text

    def dataprocessing(self,isTranslate=False,isRemoveStopWord=False,isRemovePunc=False):
        if isTranslate:
            Trans_ed = translateToEn(s)
            self.Busneed.Trans_ed
        if isRemoveStopWord:
            self.Busneed = TreebankWordDetokenizer().detokenize([w.lower() for w in word_tokenize(self.Busneed) if not w in stop_words ])
        if isRemovePunc: 
            self.Busneed = TreebankWordDetokenizer().detokenize([w.lower() for w in word_tokenize(self.Busneed) if not w in string.punctuation ])
        return self.Busneed
class large_roberta: 
    
    def __init__(self,input,modelName = "stsb-roberta-large"):
        self.BussNeed_input = input
        self._model = None 
        self._modelName = modelName
    
    def Generate_Score (self):

        if (self._model == None): 
            self._model = SentenceTransformer(self._modelName)
            self._model.max_seq_length = 512
        if (len(self.BussNeed_input)==0):
            # print('Input Erro!')
            return []
        busNeedEnCode = self._model.encode(self.BussNeed_input,show_progress_bar=True, batch_size=32)
        path = str(pathlib.Path(__file__).parent.absolute()) + '/1.list_it_solutions_modelEmbedding_model_stsb-roberta-large_numberOfWords_1000400_notLemmatize.pkl'
        itSol_df = pd.read_pickle(path)
        itSol_df['Cosine Similarity'] = itSol_df.loc[:,"Model Embedding"].apply(
            lambda x: util.pytorch_cos_sim(busNeedEnCode, x).item())
        itSol_df = itSol_df.sort_values(by='Cosine Similarity', ascending=False)
        itSol_df = itSol_df.loc[:,["Reference Code","Solution Name (Eng)","Solution Description","Cosine Similarity"]]
        itSol_df = itSol_df.iloc[:10]
        # itSol_df.to_json(r'.\ITSolList_model_stsb-roberta-large_notLemmatize_BiEncoder.json', orient='index')
        return itSol_df.to_json(orient='records')

if __name__ == '__main__':
    #Enter your new Business Need here 
    isTranslate = False
    isRemovePunc = False 
    isRemoveStopWord = False 
    #Select your data preprocessing options set to False as default
    #input = 'CCTV Video Analytic. Traditional Closed Circuit Television (CCTV) cameras are installed at strategic locations in Hong Kong to allow the Transport Department Emergency Transport Coordination Centre (ETCC) to monitor traffic condition and take remedial actions in case of emergency. There are around 1,000 fixed or pan-tilt-zoom cameras with different years of installation. At present, monitoring of camera images are performed manually by ETCC operators.  Proof of concept exercise would like to be conducted to study how Artificial Intelligence technologies could automatically monitor CCTV video and alert ETCC operators on any abnormal traffic condition.. 1) What type of abnormal traffic conditions can be discovered?'
    t0 = time.time()
    Pre_data = DataPreprocessing(sys.argv[1])
    text=Pre_data.dataprocessing(isTranslate,isRemoveStopWord,isRemovePunc)
    new = large_roberta(sys.argv[1])
    print(new.Generate_Score())
    sys.stdout.flush()
    sys.exit(0)

