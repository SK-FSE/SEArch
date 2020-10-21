from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
import string
import nltk
import json
import pickle
import tqdm
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi, BM25
from pathlib import Path

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import abc
import re
import warnings
warnings.filterwarnings('ignore')

class BM25Okapi_custom(BM25Okapi):
    def __init__(self, corpus = None, path = None, tokenizer=None, df = None, preprocessed_texts = None,  datasets = None, c = None, k1=1.5, b=0.75, n = 10, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.df = df
        self.datasets = datasets
        self.n = 10
        self.preprocessed_texts = preprocessed_texts
        if path is None:
            super().__init__(corpus, tokenizer)
        else:
            self.load_model(path)

    def load_model(self, path):
        self.doc_freqs = json.load(Path(f'{path}/doc_freqs.json').open('r'))
        self.doc_len = json.load(Path(f'{path}/doc_len.json').open('r'))
        self.idf = json.load(Path(f'{path}/idf.json').open('r')) 
        self.corpus_size = json.load(Path(f'{path}/corpus_size.json').open('r')) 
        self.avgdl = json.load(Path(f'{path}/avgdl.json').open('r')) 
        try:
          with open(f'{path}/dataset.txt', 'rb') as f:
            self.datasets = pickle.load(f)
          self.preprocessed_texts = json.load(Path(f'{path}/preprocessed_texts.json').open('r')) 
          self.df = pd.read_csv(f'{path}/df.csv')
        except Exception as e:
          print(e)
          self.datasets = None
          self.preprocessed_texts = None
          self.df = None

    def save_model(self, path):
        json.dump(self.doc_freqs, Path(f'{path}/doc_freqs.json').open('w'))
        json.dump(self.doc_len, Path(f'{path}/doc_len.json').open('w'))
        json.dump(self.idf, Path(f'{path}/idf.json').open('w'))
        json.dump(self.corpus_size, Path(f'{path}/corpus_size.json').open('w'))
        json.dump(self.avgdl, Path(f'{path}/avgdl.json').open('w'))
        with open(Path(f'{path}/dataset.txt'), 'wb') as f:
          pickle.dump(self.datasets, f)
        self.df.to_csv(f'{path}/df.csv')
        json.dump(self.preprocessed_texts, Path(f'{path}/preprocessed_texts.json').open('w'))

    def get_top_n_indices(self, query, documents, n=5):

        assert self.corpus_size == len(documents), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return top_n

    def paper_search(self, query, n = 10):
        texts, titles = get_text_title(self.df)

        prep_query = QueryPreprocessing(query)
        indexes = self.get_top_n_indices(prep_query.get_preprocessed(), self.preprocessed_texts, n=10)
        response = list()
        for index in indexes:
          title = titles[index]
          year = self.df[self.df['title'] == title]['year'].tolist()[0]
          authors = self.df[self.df['title'] == title]['name'].tolist()[0]
          prep_paper = PaperPreprocessing(texts[index])
          paper_model = BM25Okapi_custom(path=f"papers_models/{'_'.join(title.lower().split())}")
          indeces = paper_model.get_top_n_indices(prep_query.get_preprocessed(), 
                                            prep_paper.get_preprocessed(), n=3)
          interesting_parts = prep_paper.get_context(indeces, left=1, right=2)

          response.append((str(index), title, str(year), authors, interesting_parts))
        return response

    def dataset_search(self, query):
        texts, titles = get_text_title(self.df)
        result1, indexes_bm = query_bm(query, self, self.datasets, self.preprocessed_texts, titles)
        result2, indexes_query = query_table(query, self.df)
        final_result = []
        indexes = []
        for x, ind in zip(result1, indexes_bm):
            final_result.append(x)
            indexes.append(ind)
        final_result = final_result + [y for y in result1 if y not in final_result]
        final_result = final_result + [y for y in result2 if y not in final_result]

        return [(str(ind), str(self.df[self.df['title']==x].year.values[0]), self.df[self.df['title']==x].name.values[0], x) for x, ind in zip(final_result, indexes)]
            
        

class Preprocessing(metaclass=abc.ABCMeta):
    
    def __init__(self, content, trash=None):
        self.content = content
        if trash == None:
            self.trash = r'[^A-Za-z0-9 ]+'
        else:
            self.trash = r'[{}]+'.format(trash)
        self.sw_set = set(stopwords.words('english'))
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.data = None
    
    @abc.abstractmethod
    def get_preprocessed(self):
        pass
    
    def lemmatize_sentence(self, sentence):
        return [self.wordnet_lemmatizer.lemmatize(d, pos='v') for d in sentence]
    
    def remove_stopwords(self, sentence):
        return [t for t in sentence if t not in self.sw_set]
    
    def tokenize_and_lowercase(self, doc):
        return doc.lower().split(" ")
    
    def remove_trash(self, text):
        text = text.replace("\n", " ")
        return re.sub(self.trash, '', text)
        
        
        
class PaperPreprocessing(Preprocessing):
    
    def get_preprocessed(self):
        data = [self.remove_trash(data) for data in sent_tokenize(self.content)]
        self.data = data
        
        corpus_lowercase = [self.tokenize_and_lowercase(doc) for doc in data]
        
        corpus_without_sw = [self.remove_stopwords(sentence) for sentence in corpus_lowercase]
        
        sentences = [self.lemmatize_sentence(sentence) for sentence in corpus_without_sw]
        
        return sentences
    
    def get_context(self, indeces, left=2, right=2):
        assert self.data != None, "get_preprocessed should be called first"
        return [". ".join(self.data[index - left:index + right]) for index in indeces]
    
class CorpusPreprocessing(Preprocessing):
    
    def get_preprocessed(self):
        
        corpus = [' '.join([self.remove_trash(data) \
                            for data in sent_tokenize(p)]) \
                            for p in self.content]
        corpus_lowercase = [self.tokenize_and_lowercase(doc) for doc in corpus]
        corpus_without_sw = [self.remove_stopwords(doc) for doc in corpus_lowercase]
        docs = [self.lemmatize_sentence(doc) for doc in corpus_without_sw] 
        return docs
    
class QueryPreprocessing(Preprocessing):
    
    def get_preprocessed(self):
        data = self.remove_trash(self.content)
        tokenized = self.tokenize_and_lowercase(data)
        tokenized_without_sw = self.remove_stopwords(tokenized)
        return self.lemmatize_sentence(tokenized_without_sw)


def get_text_title(df):
    texts = df['paper_text'].tolist()
    titles = df['title'].tolist()
    return texts, titles

def map_datasets(dataset_list, wiki_datasets):
    result = []
    if dataset_list != dataset_list:
      return 'not found'
    if len(dataset_list) > 0 and dataset_list[0] != 'not found':
        for x in dataset_list:
            t = []
            for y in wiki_datasets:
                t.append((fuzz.ratio(x, y), y))
            result.append(sorted(t, key=lambda x: x[0], reverse=True)[0][1])
        return result
    else:
        return 'not found'

# dataset search functions
def prepare_datasets_name_from_table(df):
    for i in range(df.shape[0]):
        if type(df.datasets[i]) == str:
            if (',' in df.datasets[i]):
                df.datasets[i] = df.datasets[i].replace(" ", "").split(',')
            else:
                df.datasets[i] = df.datasets[i].replace(" ", "").split()
        elif type(df.datasets[i]) == list:
            continue
        else:
            df.datasets[i] = []

def changing_for_right_query(query, f, treshhold = 90):
    for line in f:
      if fuzz.WRatio(query,line) >= treshhold:
        query = line
        break
    return query

def query_bm(query, model, f, preprocessed_texts, titles, n = 10):
    """
    Gives list of names of the articles which contain name of the dataset in its text
    """
    changing_for_right_query(query, f, 90)
    prep_query = QueryPreprocessing(query) 
    indexes = model.get_top_n_indices(prep_query.get_preprocessed(), preprocessed_texts, n=10)
    result = ([titles[i] for i in indexes], indexes)
    return result

def query_table(query, df):
    """"
    Gives list of names of the articles whose tables contain name of the dataset.
    """
    query = query.lower().replace(" ","")
    result = []
    indexes = []
    for i in range(df.shape[0]):
        if query in [x.lower() for x in df.datasets[i].split("'")[1::2]]:
            result.append(df.title[i])
            indexes.append(i)
    return (result, indexes)   

def load_data(PATH):
  authors = pd.read_csv(f'{PATH}authors.csv')
  paper_authors = pd.read_csv(f'{PATH}paper_authors.csv')
  papers = pd.read_csv(f'{PATH}papers19.csv')

  authors_to_merge = pd.merge(paper_authors, authors, how='left', left_on='author_id', right_on='id')
  authors_to_merge.drop(columns=['id_x', 'id_y', 'author_id'], axis=1, inplace=True)
  papers = pd.merge(papers, authors_to_merge.groupby('paper_id').aggregate(lambda x: list(x)), how='left', left_on='id', right_on='paper_id')

  f = open(f'{PATH}datasets.txt', 'r', encoding='utf-8', errors='ignore')
  f = list(f.readlines())
  f = [i.rstrip('\n') for i in f]
  wiki_datasets = []
  wiki_datasets.extend([re.sub('\n', '', x) for x in f])
  papers.datasets = papers.datasets.apply(lambda x: map_datasets(x, wiki_datasets))
  
  return papers, f

def train_models(papers):
  texts, titles = get_text_title(papers)
  # create and save model for each paper 
  Path("papers_models").mkdir(parents=True, exist_ok=True) 
  for text, title in tqdm.tqdm(zip(texts, titles)):
      try:
          prep_text = PaperPreprocessing(text)
          preprocessed = prep_text.get_preprocessed()
          bm25 = BM25Okapi_custom(preprocessed)
          name = '_'.join(title.lower().split())
          Path(f"papers_models/{name}").mkdir(parents=True, exist_ok=True)
          bm25.save_model(f'papers_models/{name}')
      except:
          continue
  
def train_search_model(papers, f):
  texts, titles = get_text_title(papers)
  corpus_prep = CorpusPreprocessing(texts)
  preprocessed_texts = corpus_prep.get_preprocessed()

  Path("papers_search").mkdir(parents=True, exist_ok=True) 
  bm25 = BM25Okapi_custom(corpus = preprocessed_texts,
                        df = papers, 
                        preprocessed_texts = preprocessed_texts,
                        datasets = f)
  bm25.save_model(f'papers_search')






