from packages.calc_TF_IDF import CustomTFIDF
from packages.svd import CustomSVD




class LSA:
    def __init__(self,preprocessed_sentences):
        self.__TFIDF_object=None
        self.__SVD_object=None
        self.__preprocessed_sentences=preprocessed_sentences
    
    def process(self):
        self.__TFIDF_object=CustomTFIDF(self.__preprocessed_sentences)
        A=self.__TFIDF_object.compute_tf_idf()
        self.__SVD_object=CustomSVD(A)
        U,Sigma,Vt=self.__SVD_object.calc_svd()
        return U,Sigma,Vt
        