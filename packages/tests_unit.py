from packages.preprocessing_text import TextPreProcessor
from packages.LSA import LSA
from packages.sentence_scoring import SentenceSelection
import unittest
from nltk.tokenize import sent_tokenize

class Testcases(unittest.TestCase):
    def test_preprocessing(self):
        #tc_003
        text = ["123456","!@##%^&&*","उक्त छानबिन समितिको प्रतिवेदनपछि यातायात व्यवस्था विभागका अधिकारीहरूले १,०२,००० वटा शङ्कास्पद लाइसन्समध्ये ७२,००० को तथ्याङ्कलाई पुनर्प्रमाणीकरण गर्न भौतिक पूर्वाधार तथा यातायात मन्त्रालयमार्फत् प्रदेश सरकारलाई अनुरोध गरिएको बीबीसीलाई बताएका थिए।"]
        preprocessor_object=TextPreProcessor()
        for txt in text:
            preprocessed_sentences,_,_,_,_,= preprocessor_object.preprocessor(txt)
            messsage="failed"
            self.assertEqual(len(preprocessed_sentences),0,messsage) 


    def test_summarylength(self):
        #tc_004
        summary_length=5
        preprocessor_object=TextPreProcessor()
        text="Apples fall to the ground. We live in a world in which objects behave the same given the same circumstances. We can imagine living in a different world: a world that constantly changes, a world in which the Sun does not rise every day, a world in which water one day boils at 50°C, and at 120°C another day, a world in which apples sometimes fall from trees and sometimes rise into the sky. Only because we live in a world that displays stable regularities are we able to reliably shape our environment and plan our lives. We have an intuition that these regularities are due to laws of nature, but we normally do not interrogate what these laws are and how they work in any basic metaphysical sense. Instead, we assume that science not only provides these laws but also elucidates their structure and metaphysical status, even when the answers seem partial at best. In short, we assume that, thanks to science, there is a recipe of sorts for how the laws of nature work. You take the state of the Universe at a given moment – every single fact about every single aspect of it – and combine it with the laws of nature, then assume that these will reveal, or at least determine, the state of the Universe in the moment that comes next. I refer to this as the layer-cake model of the Universe, which dates back to the 17th-century philosopher René Descartes. Not long after Descartes embraced the idea of a deterministic universe, Isaac Newton presented a mathematical law for gravitation, which gave the concept a powerful quantitative update. The gravitational force on one body at one time is determined by the location of all the bodies in the Universe at that time; the state of the Universe plus the law of gravitation tells you how all bodies will move: a layer-cake model, indeed. The influence of Descartes and Newton on how we think about laws of nature is immense – and not without justification. It has helped to unify whole fields of physics, including mechanics, gravitation and electromagnetism. It is still so widespread in the scientific community, and it has such a distinguished pedigree, that scientists may not even realise that they subscribe to the layer-cake model at all. But the uncomfortable truth is that there are many aspects of modern physics that seem to provide counterexamples to the layer-cake model. To date, some of these alternatives have occupied only a rogue niche in physics. But they should be studied more deeply and understood more widely because they pose major challenges to our fundamental understanding of the Universe – how it began, where it is going, and what kind of entity, if any, is driving it."
        preprocessed_sentences,_,_= preprocessor_object.preprocessor(text)
        length=len(preprocessed_sentences)
        test=  True if summary_length <= length else False
        self.assertEqual(test,True,"failed")
        
    def test_summarylengthaccuracy(self):
        #tc_005
        summary_length=5
        preprocessor_object=TextPreProcessor()
        text="Apples fall to the ground. We live in a world in which objects behave the same given the same circumstances. We can imagine living in a different world: a world that constantly changes, a world in which the Sun does not rise every day, a world in which water one day boils at 50°C, and at 120°C another day, a world in which apples sometimes fall from trees and sometimes rise into the sky. Only because we live in a world that displays stable regularities are we able to reliably shape our environment and plan our lives. We have an intuition that these regularities are due to laws of nature, but we normally do not interrogate what these laws are and how they work in any basic metaphysical sense. Instead, we assume that science not only provides these laws but also elucidates their structure and metaphysical status, even when the answers seem partial at best. In short, we assume that, thanks to science, there is a recipe of sorts for how the laws of nature work. You take the state of the Universe at a given moment – every single fact about every single aspect of it – and combine it with the laws of nature, then assume that these will reveal, or at least determine, the state of the Universe in the moment that comes next. I refer to this as the layer-cake model of the Universe, which dates back to the 17th-century philosopher René Descartes. Not long after Descartes embraced the idea of a deterministic universe, Isaac Newton presented a mathematical law for gravitation, which gave the concept a powerful quantitative update. The gravitational force on one body at one time is determined by the location of all the bodies in the Universe at that time; the state of the Universe plus the law of gravitation tells you how all bodies will move: a layer-cake model, indeed. The influence of Descartes and Newton on how we think about laws of nature is immense – and not without justification. It has helped to unify whole fields of physics, including mechanics, gravitation and electromagnetism. It is still so widespread in the scientific community, and it has such a distinguished pedigree, that scientists may not even realise that they subscribe to the layer-cake model at all. But the uncomfortable truth is that there are many aspects of modern physics that seem to provide counterexamples to the layer-cake model. To date, some of these alternatives have occupied only a rogue niche in physics. But they should be studied more deeply and understood more widely because they pose major challenges to our fundamental understanding of the Universe – how it began, where it is going, and what kind of entity, if any, is driving it."
        preprocessed_sentences,tokenized_sentences,index_map= preprocessor_object.preprocessor(text)
        lsa=LSA(preprocessed_sentences)
        U,_,_=lsa.process()
        sentselect=SentenceSelection(U,preprocessed_sentences,tokenized_sentences,summary_length, index_map)
        summary=sentselect.cross()
        test_length=0
        for sent in summary:
            test_length+=1

        self.assertEqual(test_length,summary_length,"failed")

    
    

    

if __name__=="__main__":
    unittest.main()

