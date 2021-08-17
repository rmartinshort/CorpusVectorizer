
import string
import keybert
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize

class Preprocessor(object):

    def __init__(self, corpus):
        """

        Parameters
        ----------
        corpus
        """
        self.original_corpus = corpus
        # detect language option here?
        self.corpus_language = "english"
        self.kw_model = None

        if isinstance(self.original_corpus,list):
            self.text_type = "corpus"
        elif isinstance(self.original_corpus,str):
            self.text_type = "document"
            self.original_corpus = [self.original_corpus]
        else:
            raise ValueError("Inout corpus must be a single document string or a list")

        return

    def tokenize_words(self, keep_sents=False, remove_puncts=False):
        """

        Parameters
        ----------
        keep_sents
        remove_puncts

        Returns
        -------

        """

        if remove_puncts:
            corpus = [x.translate(str.maketrans('', '', string.punctuation)) for x in self.original_corpus]
        else:
            corpus = self.original_corpus

        return [word_tokenize(x,language=self.corpus_language,preserve_line=keep_sents) for x in corpus]

    def tokenize_sentences(self):
        """

        Returns
        -------

        """

        return [sent_tokenize(x) for x in self.original_corpus]

    def remove_stopwords(self,keep_sents=True,tokenize=False):
        """

        Parameters
        ----------
        keep_sents
        tokenize

        Returns
        -------

        """

        stopwords_remove_corpus = []
        stop_words = set(stopwords.words(self.corpus_language))

        for doc in self.original_corpus:
            words = [x for x in word_tokenize(doc,language=self.corpus_language,preserve_line=keep_sents) if x.lower() not in stop_words]
            if tokenize:
                stopwords_remove_corpus.append(words)
            else:
                stopwords_remove_corpus.append(" ".join(words))

        return stopwords_remove_corpus

    def to_lowercase(self):
        """

        Returns
        -------

        """

        return [x.lower() for x in self.original_corpus]

    def extract_keywords(self, algorithm):
        """

        Parameters
        ----------
        algorithm

        Returns
        -------

        """

        assert algorithm in ["rake","keybert"]

        if algorithm == "keybert":

            key_phrases = self._extract_phrases_keybert()

        return key_phrases

    def _extract_phrases_keybert(self):

        if isinstance(self.kw_model,keybert._model.KeyBERT):

            pass

        elif self.corpus_language == "english":

            self.kw_model = keybert.KeyBERT()
            input_stop_words = "english"

        else:

            self.kw_model = keybert.KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")
            input_stop_words = None
            #ToDo write function to choose input stopwords

        kw_vec = []
        for doc in self.original_corpus:
            kws = self.kw_model.extract_keywords([doc],
                                         keyphrase_ngram_range=(2, 3),
                                         stop_words=input_stop_words,
                                         use_maxsum=True,
                                         nr_candidates=200,
                                         top_n=100)
            kw_vec.append([x[0] for x in kws[0]])

        return kw_vec



    def extact_default_entities(self, algorithm):
        """

        Parameters
        ----------
        algorithm

        Returns
        -------

        """

        assert algorithm in ["spacy"]

        return

