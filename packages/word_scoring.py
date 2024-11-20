import numpy as np

def preprocessing_V_matrix(Vt):
    # V=Vt.T
    # for row_vector in (V):
    #     avg_row_vector=np.mean(row_vector)
    #     for j in range(V.shape[1]):
    #         if row_vector[j]<avg_row_vector:
    #             row_vector[j]=0
    # return V
    V=Vt.T
    for i in range(V.shape[1]):          # Loop through each column index
        col_vector = np.absolute(V[:, i])              # Extract the current column
        avg_col_vector = np.mean(col_vector)  # Calculate the mean of this column
        col_vector = np.where(col_vector < avg_col_vector, 0, col_vector)  # Set elements < mean to 0
        V[:, i] = col_vector 
    # print(U)
    return V
#


def calc_word_length(preprocessed_V):
   word_scores=[calc_l2_norm(preprocessed_V[i]) for i in range(preprocessed_V.shape[0])]   
   return word_scores


def calc_l2_norm(row_vector):
    return np.sqrt(np.sum(np.square(row_vector)))



def calc_rank(word_score,tokenized_words,word_index_map):
    idx=np.argsort(word_score)[::-1]
    original_indices=[word_index_map[i] for i in idx]
    ranked_words=[tokenized_words[i] for i in original_indices]
    # print(ranked_words)
    # print("--"*50)
    # print(tokenized_words)
    top_five_words=[ranked_words[i] for i in range(5)]
    return top_five_words


def cross_words(Vt,tokenized_words,word_index_map):
    preprocessed_V=preprocessing_V_matrix(Vt)
    word_score=calc_word_length(preprocessed_V)
    ranked_words=calc_rank(word_score,tokenized_words,word_index_map)
    # print(ranked_words)
    # top_words(V,tokenized_words)
    # topic_det(Vt,tokenized_words)
    return ranked_words





# def top_words(Vt,tokenized_words):
#     V=Vt.T
#     idx=[]
#     for i in range(3):
#         col_vector=np.abs(V[:,i])
#         idx.append(np.argmax(col_vector))
#     indices=list(set(idx)) 
#     words=[tokenized_words[i] for i in indices]
#     print(words)

# def topic_det(Vt,tokenized_words):
#     # V=Vt.T
#     # indices=[]
#     # col_vector=np.array(np.abs(V[:,0]))
#     # temp=col_vector.copy()
#     # i=0
#     # while i !=3:
#     #     max=temp.argmax()
#     #     indices.append(max)
#     #     temp=np.delete(temp,max)
#     #     i+=1
#     # topic=[tokenized_words[i] for i in indices]
#     # print(topic)
#     V=Vt.T
#     col_vector = np.abs(V[:, 0])
    
#     # Find indices of top n values
#     indices = np.argsort(-col_vector)[:3]  # negative for descending order
    
#     # Extract corresponding words
#     topics = [tokenized_words[i] for i in indices]

    



