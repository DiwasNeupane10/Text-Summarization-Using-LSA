import numpy as np

class SentenceSelection:
    def __init__(self,U,preprocessed_sentences,tokenized_sentences,summary_length, index_map):
        self.__preprocessed_sentences=preprocessed_sentences
        self.__U=U
        self.__tokenized_sentences=tokenized_sentences
        self.__summary_length=summary_length 
        self.__index_map=index_map
        self.__used_indices={}
        


    def preprocessing_U_matrix(self):
        # org_U=U.copy()
        U=self.__U.copy()
      
        
        # print(org_U)
        # print("----")
        for i in range(U.shape[1]):  # Loop through each column index
            # for each concept represented by cols of U matrix
            col_vector = np.absolute(U[:, i])  # Extract the current column
            avg_col_vector = np.mean(col_vector)  # Calculate the mean of this column
            col_vector = np.where(
                col_vector < avg_col_vector, 0, col_vector
            )  # Set elements < mean to 0
            U[:, i] = col_vector
        # print(U.shape[0])
        return U


    def calc_sentence_length(self,preprocessed_U):
        sentence_scores = [self.calc_l2_norm(preprocessed_U[i]) for i in range(preprocessed_U.shape[0])]  # stores the l2 norm of sentences

        return [[ps, sentence_score] for ps, sentence_score in zip(self.__preprocessed_sentences, sentence_scores)]


    def calc_l2_norm(self,row_vector):
        return np.sqrt( np.sum(np.square(row_vector)))  # calulates the l2 norm of each sentence


    def calc_rank(self,sentence_length_list):
        # convert the preprocessed sentence to the original sentences using the sentence index map
        for li, index in zip(sentence_length_list, self.__index_map):
            li[0] = self.__tokenized_sentences[index]
        # extract the scores
        scores = [li[1] for li in sentence_length_list]
        # extract the sentences
        sentences = [li[0] for li in sentence_length_list]
        # get the indices that sort the scores in descending order
        idxx = np.argsort(scores)[::-1]
        # sort the sentences on the indices obtained above as the scores correspond to the each sentence
        ranked_sent = [sentences[i] for i in idxx]
        # sort the scores in descending order
        ranked_scores = sorted(scores, reverse=True)
        return ranked_sent, ranked_scores


    def return_ordered(self,summary_data,sentence_to_indices):
        """key is the sorting criteria
        for the tuples in summary data extract index and sorts accordingly.Meaning the sentences that come first in the
        original sentence will be first
        """
    
        ordered_summary = sorted(summary_data, key=lambda x: self.get_original_index(x[0],sentence_to_indices))
    
        return ordered_summary
    


    def cross(self,sentence_to_indices):
        preprocessed_U = self.preprocessing_U_matrix()
        sentence_length_list =self.calc_sentence_length(preprocessed_U)
        ranked_sentences, ranked_scores = self.calc_rank(sentence_length_list)
        summary = [ranked_sentences[i] for i in range(int(self.__summary_length))]
        summary_score = [ranked_scores[i] for i in range(int(self.__summary_length))]
        summary_data = [(sentence, score) for sentence, score in zip(summary, summary_score)]
     

        ordered_summary = self.return_ordered(summary_data,sentence_to_indices)
      
      
        return ordered_summary


    

    def get_original_index(self,sentence,sentence_to_indices):
        """Retrieve the correct index for duplicate sentences."""
       
        if sentence not in self.__used_indices:
            self.__used_indices[sentence] = 0
        index = sentence_to_indices[sentence][self.__used_indices[sentence]]
        self.__used_indices[sentence] += 1  # Move to the next occurrence
        return index

   