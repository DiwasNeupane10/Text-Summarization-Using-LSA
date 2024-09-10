from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
def preprocessor(text):
    lematizer=WordNetLemmatizer()
    tokenized_words=word_tokenize(text)
    #tokenize the text
    stop_words =set(stopwords.words("english"))#define the stopwords
    first_clean = [re.sub(r'[^a-zA-Z\s]', '', word) for word in tokenized_words]
    '''
    iterates over the tokenized_words as word and re.sub checks whether it matches the expression 
    if not then replaces it with a space
    '''
    filtered_list=[word for word in first_clean if word.casefold() not in stop_words and word.strip()]
    '''
        iterates over the first_clean list as word
        casefold() is used for ignoring the case of the word then
        if the word is not in stop_words and removing whitespacces
    '''
    lematized_list=[lematizer.lemmatize(word) for word in filtered_list]
    return lematized_list


    
