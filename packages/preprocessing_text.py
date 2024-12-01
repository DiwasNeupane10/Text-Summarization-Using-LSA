from nltk.tokenize import word_tokenize,sent_tokenize 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

def preprocessor_for_sentence(sent):
    lematizer=WordNetLemmatizer()
    #tokenize the sentence into words
    tokenized_words=word_tokenize(sent)
    stop_words =set(stopwords.words("english"))#define the stopwords
    first_clean = [re.sub(r'[^a-zA-Z\s]', '', word) for word in tokenized_words]
    '''
    iterates over the tokenized_words as word and re.sub checks whether it matches the expression 
    if not then replaces it with a space
    '''
    filtered_words=[word for word in first_clean if word.casefold() not in stop_words and word.strip()]
    '''
        iterates over the first_clean list as word
        casefold() is used for ignoring the case of the word then
        if the word is not in stop_words and removing whitespacces
    '''
    lematized_words=[lematizer.lemmatize(word) for word in filtered_words]
    return ' '.join(lematized_words),lematized_words


# def preprocessor(text):
#     tokenized_sentence=sent_tokenize(text)
#     preprocessed_sentences=[preprocessor_for_sentence(sent) for sent in tokenized_sentence]
#         # print(preprocessed_sentences)
#         # print(tokenized_sentence)
#     return preprocessed_sentences,tokenized_sentence

def preprocessor(text):
    tokenized_sentence=sent_tokenize(text)
    # for i,ts in enumerate(tokenized_sentence):
        # print(f'tokenized sentence at index{i}: {ts}' )
        # print("XX")
    # print("----"*50)
    preprocessed_sentences=[]
    tokenized_words=[]
    index_map=[]
    word_position=0
    word_index_map=[]
    for i,sent in enumerate(tokenized_sentence):
        preprocessed_sentence,list_words=preprocessor_for_sentence(sent)
        if preprocessed_sentence and preprocessed_sentence!=" ":
            # print(f"preprocessed sentence at index {i}:{preprocessed_sentence}")
            # print("XX")
            preprocessed_sentences.append(preprocessed_sentence)
            index_map.append(i)
            # print(list_words)
            for word in list_words:
                tokenized_words.append(word)
                word_index_map.append(word_position)
                word_position+=1
    # print(tokenized_words)
           
    # print("tokenized_Sentences",len(tokenized_sentence))        
    # print("preprocessed_Sentences",preprocessed_sentences)

    # print(index_map)
    return preprocessed_sentences,tokenized_sentence,index_map,tokenized_words,word_index_map