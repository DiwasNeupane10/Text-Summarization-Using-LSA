import numpy as np

def calc_sentence_score(preprocessed_U,tokenized_sentences):
   sentence_scores=[calc_l2_norm(preprocessed_U[i]) for i in range(preprocessed_U.shape[0])]
#    dict={}
#    for i,score in enumerate(sentence_scores):
#        dict[tokenized_sentences[i]]=float(score)
#    print(dict)    
   return sentence_scores

def calc_rank(sentence_scores,tokenized_sentences,index_map):
    idx=np.argsort(sentence_scores)[::-1]
    ranked_original_indices=[index_map[i]for i in idx]
    # ranked_sentences=[tokenized_sentences[i] for i in idx]
    ranked_sentences=[tokenized_sentences[i]for i in ranked_original_indices]
    # print("-"*100)
    # for sent in ranked_sentences:
        # print("\n",sent)
    return ranked_sentences


def preprocessing_U_matrix(U):
    for i,row_vector in enumerate(U):
        avg_row_vector=np.mean(row_vector)
        # print(avg_row_vector)
        for j in range(U.shape[1]):
            if row_vector[j]<avg_row_vector:
                row_vector[j]=0
        # print(row_vector)
    # print("----")
    # print(U)
    return U
#

def calc_l2_norm(row_vector):
    return np.sqrt(np.sum(np.square(row_vector)))


def cross(U,tokenized_sentences,summary_length,index_map):
    preprocessed_U=preprocessing_U_matrix(U)
    sentence_score=calc_sentence_score(preprocessed_U,tokenized_sentences)
    ranked_sentences=calc_rank(sentence_score,tokenized_sentences,index_map)
    summary=[ranked_sentences[i]for i in range(int(summary_length))]
    ordered_summary=return_ordered(summary,tokenized_sentences)
    # print(summary)
    # print("--"*80)
    # print(ordered_summary)
    # return summary
    return ordered_summary

def return_ordered(summary,tokenized_sentences):   
    dict={}
    for i,sentence in enumerate(summary):
        dict[sentence]=tokenized_sentences.index(sentence)
    # print(dict)
    indices=sorted(list(dict.values()))
    # print(indices)
    return [tokenized_sentences[i] for i in indices]
    