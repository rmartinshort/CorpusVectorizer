import pytest
from corpus_vectorizer.preprocessor import Preprocessor

class TestInitialize(object):
    """

    """

    def test_on_list_corpus(self):

        corpus = ["I am a document", "I am anohter document"]
        p = Preprocessor(corpus=corpus)

        assert p.text_type == "corpus"

    def test_on_document_corpus(self):

        document = "I am a document"
        p = Preprocessor(corpus=document)

        assert p.text_type == "document"
        assert isinstance(p.original_corpus,list)

    def test_to_lowercase(self):

        document = "This Is A Document WiTH Some UPPerCaSe"
        p = Preprocessor(corpus=document)
        lc_text = p.to_lowercase()[0]

        assert lc_text == "this is a document with some uppercase"

    def test_basic_word_tokenize(self):

        test_corpus = ["I am the first document. I have two sentences", "I am the second document"]
        p = Preprocessor(corpus=test_corpus)

        tokenized_no_puncs = p.tokenize_words(keep_sents=False,remove_puncts=True)
        assert tokenized_no_puncs == [["I","am","the","first","document","I","have","two","sentences"],["I","am","the","second","document"]]

    def test_stopwords_remove(self):

        test_corpus = ["I am the first document. I have two sentences", "I am the second document"]
        p = Preprocessor(corpus=test_corpus)

        stopwords_remove_corpus1 = p.remove_stopwords(keep_sents=True,tokenize=True)
        assert stopwords_remove_corpus1 == [['first', 'document.', 'two', 'sentences'],["second", "document"]]

        stopwords_remove_corpus2 = p.remove_stopwords(keep_sents=True,tokenize=False)
        assert stopwords_remove_corpus2 == ["first document. two sentences", "second document"]

        stopwords_remove_corpus3 = p.remove_stopwords(keep_sents=False,tokenize=False)
        assert stopwords_remove_corpus3 == ["first document . two sentences", "second document"]

    def test_keyword_extraction(self):

        test_corpus = ["This is a document with some key word candidates. We will use an algorithm to extract them"]
        p = Preprocessor(corpus=test_corpus)

        key_phrases = p.extract_keywords(algorithm="keybert")

        assert key_phrases == [['document key',
                                'key word',
                                'document key word',
                                'candidates use',
                                'use algorithm',
                                'word candidates',
                                'word candidates use',
                                'key word candidates',
                                'algorithm extract',
                                'candidates use algorithm',
                                'use algorithm extract']]





