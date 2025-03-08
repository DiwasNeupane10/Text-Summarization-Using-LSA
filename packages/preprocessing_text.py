from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

class TextPreProcessor:
    def __init__(self):
        self.__word_net_lematizer=WordNetLemmatizer()
        self.__stopwords=set(stopwords.words("english"))
        self.sentence_to_indices = {}
        
    def first_cleaner(self,sent):
        # tokenize the sentence into words
        tokenized_words=word_tokenize(sent)
        """
            iterates over the tokenized_words as word and re.sub checks whether it matches the expression 
            if not then replaces it with a space
        """
        first_cleaned_words=[re.sub(r"[^a-zA-Z\s]", "", word) for word in tokenized_words]
        return first_cleaned_words
    
    def filterer(self,first_cleaned_words):
        """
            iterates over the first_clean list as word
            casefold() is used for ignoring the case of the word then
            if the word is not in stop_words and removing whitespacces
        """
        filtered_words = [
        word
        for word in first_cleaned_words
        if word.casefold() not in self.__stopwords and word.strip()
        ]
        return filtered_words
    
    def lematizer(self,filtered_words):
        lematized_words = [self.__word_net_lematizer.lemmatize(word) for word in filtered_words]
        return lematized_words
    
    def preprocessor_for_sentence(self,sent):
        first_cleaned_words=self.first_cleaner(sent)
        filtered_words=self.filterer(first_cleaned_words)
        lematized_words=self.lematizer(filtered_words)
        return " ".join(lematized_words)
    
    def preprocessor(self,text):
        tokenized_sentences = sent_tokenize(text)
        preprocessed_sentences = []
        index_map = []
        
        
        for i, sent in enumerate(tokenized_sentences):
            preprocessed_sentence= self.preprocessor_for_sentence(sent)
            if preprocessed_sentence and preprocessed_sentence != " ":
                preprocessed_sentences.append(preprocessed_sentence)
                index_map.append(i)
            
            if sent in self.sentence_to_indices:#if the sentence has already been seen previously
                self.sentence_to_indices[sent].append(i) #append the next index 
            else:#otherwise set to the currrent index
                self.sentence_to_indices[sent] = [i]

            
        return (preprocessed_sentences,tokenized_sentences,index_map)


        
   

   
    