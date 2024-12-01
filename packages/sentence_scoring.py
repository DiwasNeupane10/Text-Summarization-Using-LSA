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
    # print(U.shape[0])
    return U


def calc_sentence_length(preprocessed_U,preprocessed_sentences):
    sentence_scores=[calc_l2_norm(preprocessed_U[i]) for i in range(preprocessed_U.shape[0])]#stores the l2 norm of sentences 
    # listt=[]
    # for i,ps in enumerate(preprocessed_sentences):
    #     listt.append([ps,sentence_scores[i]])
    return [[ps,sentence_score]for ps,sentence_score in zip(preprocessed_sentences,sentence_scores)]

def calc_l2_norm(row_vector):
    return np.sqrt(np.sum(np.square(row_vector)))#calulates the l2 norm of each sentence

def calc_rank(tokenized_sentences,index_map,listt):
    for li,index in zip(listt,index_map):
        li[0]=tokenized_sentences[index]
    scores=[li[1] for li in listt]
    sentences=[li[0]for li in listt]
    idxx=np.argsort(scores)[::-1]
    ranked_sent=[sentences[i] for i in idxx]
    # print(ranked_sent)
    
    ranked_scores=sorted(scores,reverse=True)
    # summary_data=[(sent,score)for sent,score in zip(ranked_sent,score) ]

    return ranked_sent,ranked_scores





def return_ordered(summary_data,tokenized_sentences):   
    ordered_summary=sorted(summary_data,key=lambda x:tokenized_sentences.index(x[0]))
    return ordered_summary

def cross(U,tokenized_sentences,summary_length,index_map,preprocessed_sentences):
    preprocessed_U=preprocessing_U_matrix(U)
    listt=calc_sentence_length(preprocessed_U,preprocessed_sentences)
    ranked_sentences,ranked_scores=calc_rank(tokenized_sentences,index_map,listt)
    summary=[ranked_sentences[i]for i in range(int(summary_length))]
    summary_score=[ranked_scores[i]for i in range(int(summary_length))]
    # print("----"*50)
    # print(f'{len(summary_score)}{summary_score}')
    summary_data=[(sentence,score)for sentence,score in zip(summary,summary_score)]
    ordered_summary=return_ordered(summary_data,tokenized_sentences)
    # print("----"*50)
    # print(ordered_summary)
    return ordered_summary


    