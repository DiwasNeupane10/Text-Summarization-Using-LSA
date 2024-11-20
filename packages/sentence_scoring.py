import numpy as np

def preprocessing_U_matrix(U):
    # org_U=U.copy()
    # print(org_U)
    # print("----")
    for i in range(U.shape[1]):          # Loop through each column index
        #for each concept represented by cols of U matrix 
        col_vector = np.absolute(U[:, i])              # Extract the current column
        avg_col_vector = np.mean(col_vector)  # Calculate the mean of this column
        col_vector = np.where(col_vector < avg_col_vector, 0, col_vector)  # Set elements < mean to 0
        U[:, i] = col_vector 
    # print(U)
    return U


def calc_sentence_length(preprocessed_U,tokenized_sentences):
   sentence_scores=[calc_l2_norm(preprocessed_U[i]) for i in range(preprocessed_U.shape[0])]#stores the l2 norm of sentences 
#    dict={}
#    for i,score in enumerate(sentence_scores):
#        dict[tokenized_sentences[i]]=float(score)
#    print(dict)    
   return sentence_scores

def calc_l2_norm(row_vector):
    return np.sqrt(np.sum(np.square(row_vector)))#calulates the l2 norm of each sentence

def calc_rank(sentence_scores,tokenized_sentences,index_map):
    idx=np.argsort(sentence_scores)[::-1]#stores the indices of how the sentence scores should be sorted in descending order
    ranked_original_indices=[index_map[i]for i in idx]#index map stores the indices of the preprocessed sentence 
    #get the indices of the sentence in the original sentences 
    # ranked_sentences=[tokenized_sentences[i] for i in idx]
    ranked_sentences=[tokenized_sentences[i]for i in ranked_original_indices]
    # print("-"*100)
    # for sent in ranked_sentences:
        # print("\n",sent)
    return ranked_sentences




def return_ordered(summary,tokenized_sentences):   
    dict={}
    for i,sentence in enumerate(summary):
        dict[sentence]=tokenized_sentences.index(sentence)#stores the indices of the summary so that the sentences that come first should also come first in the summary
    # print(dict)
    indices=sorted(list(dict.values()))#this sorts the indices 
    # print(indices)
    return [tokenized_sentences[i] for i in indices]

def cross(U,tokenized_sentences,summary_length,index_map):
    preprocessed_U=preprocessing_U_matrix(U)
    sentence_score=calc_sentence_length(preprocessed_U,tokenized_sentences)
    ranked_sentences=calc_rank(sentence_score,tokenized_sentences,index_map)
    summary=[ranked_sentences[i]for i in range(int(summary_length))]
    ordered_summary=return_ordered(summary,tokenized_sentences)
    # print(summary)
    # print("--"*80)
    # print(ordered_summary)
    # return summary
    return ordered_summary


    