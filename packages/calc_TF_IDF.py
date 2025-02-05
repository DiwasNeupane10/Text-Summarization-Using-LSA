import pandas as pd
import math


def compute_tf_idf(preprocessed_sentences):
    no_of_sentences = len(preprocessed_sentences)
    dict1 = compute_total_words_in_sentence(no_of_sentences, preprocessed_sentences)
    dict2 = count_word_appear_in_sentence(no_of_sentences, preprocessed_sentences)
    tf = compute_tf(dict1, dict2)
    isf = compute_isf(no_of_sentences, preprocessed_sentences)
    tf_idf = tf * isf.iloc[0]
    # tf_idf = tf.multiply(isf['ISF'], axis=0)
    # return tf,isf,tf_idf.fillna(0)
    return tf_idf.fillna(0)


# function to calculate the total no of words in each sentence.stored in a dictionary
def compute_total_words_in_sentence(no_of_sentences, preprocessed_sentences):
    sentence_total_words_dict = {}
    for i in range(no_of_sentences):  # iterate over the sentences
        sentence_total_words_dict[i] = count_words(
            preprocessed_sentences[i]
        )  # at the index(sentence_no) the total words in that sentence is added.
    return sentence_total_words_dict


def word_split(sent):
    words = str(sent).split()  # splits the words of the sentences
    words = [
        word.strip() for word in words
    ]  # strips of any leading or trailing whitespaces
    return words


def count_words(sent):
    return len(word_split(sent))  # returns the total no of words


# function to calculate the total no of occurance of word in a sentence.stored in a nested dictionary
"""
Example:
word_occurance_dict={
    1:{'word1':2,
        'word2':1
    }
    2:{'word3':2,
        'word4':1
    },
    .
    .
    .
    }
"""


def count_word_appear_in_sentence(no_of_sentences, preprocessed_sentences):
    word_occurance_dict = {}
    for i in range(no_of_sentences):  # iterates over the total no of sentences
        word_count = (
            {}
        )  # dictionary to store word occurance without specifiying the sentence no
        words = word_split(preprocessed_sentences[i])  # total wordset
        for word in words:  # iterate over the words
            if (
                word in word_count
            ):  # checks if the word is alreaddy in the dictionary as a key
                word_count[word] += 1
            else:
                word_count[word] = 1
        word_occurance_dict[i] = (
            word_count  # addd the dictionary in the key(index) ie sentence no
        )
    # print(word_occurance_dict)
    return word_occurance_dict


# function to compute term frequency
def compute_tf(dict1, dict2):
    tf_dict = {}
    for (
        sentence_no,
        word_occurance,
    ) in dict2.items():  # iterates over the key value pairs of the word_occurance_dict
        tf_dict[sentence_no] = {}  # initializes a nested dictionary
        total_words = dict1[
            sentence_no
        ]  # gets the total word count from sentence_total_words dict
        for word, count in word_occurance.items():  # iterates over the dictionary
            tf_dict[sentence_no][word] = count / total_words
            # TF(t,s)=no of occurancce of the word in that sentence/no of words in that sentence
    term_frequency = pd.DataFrame.from_dict(tf_dict)  # create a DataFrame
    term_frequency = term_frequency.fillna(0).T
    # term_frequency=term_frequency.fillna(0)

    """
    fills the NaN vlaues with 0
    we get Nan for word that are not in some sentences .
    Then .T is used to Transpose the Df .
    """
    term_frequency = term_frequency.sort_index(axis=1)
    return term_frequency


# function to compute inverse sentence frequency
def compute_isf(no_of_sentences, preprocessed_sentences):
    sentence_dict = {}  # dictionary to store no of sentence that contains the words
    isf_dict = {}
    for i in range(no_of_sentences):
        words = set(
            word_split(preprocessed_sentences[i])
        )  # converting to set inorder to not have repeated words
        for word in words:
            if word in sentence_dict:
                sentence_dict[
                    word
                ] += 1  # if the word is already in the key of the dictionary it will increment its count
                # meaning the word as a index will have a value specifiying no of sentences containing the word
            else:
                sentence_dict[word] = 1  # else it is a new word
        for word, sentence_count in sentence_dict.items():
            isf_dict[word] = return_isf(no_of_sentences, sentence_count)
    # print(isf_dict)
    inverse_frequency = pd.DataFrame.from_dict(
        isf_dict, orient="index", columns=["ISF"]
    )  # creates a Df from the dictionary and columns with header ISF
    inverse_frequency = inverse_frequency.T.reset_index(drop=True)  # drops the header
    inverse_frequency = inverse_frequency.sort_index(
        axis=1
    )  # sorts the df on the basis of alphabetical order of the keys ie the words
    # print(inverse_frequency)
    return inverse_frequency


def return_isf(N, St):
    St = int(St)
    return math.log(N / (St))
