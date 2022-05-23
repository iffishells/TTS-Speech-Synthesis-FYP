import re
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
import pandas as pd
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import numpy as np

# import time
import time


# selenium servies

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



import base64
import boto3
import os
from contextlib import closing


class linguistic:
    def __init__(self,filePath):
        self.filePath = filePath
    
    def IPA(self,token_list):
        filledIPA = []
        for token in token_list:
            IPAString = ""
            for char in token:
                # print("Char : ",char)
                # print("type : ",type(char))
                ret = self.df_ipa(char)
                # print(ret)
                
                print("Token : {} ,char : {} , IPA : {} ".format(token,char,ret))
                IPAString = IPAString+str(ret)
            filledIPA.append(IPAString)
            
        # print('filledIPA : ',filledIPA)
        return filledIPA
            
        
    def df_ipa(self,TokenChar):
        '''
            There are three type dictonary Final, medial and initial and 
        '''
        df = pd.read_csv("Datasets/IPA_pashto.csv",encoding="utf-8")
        
        array_isolated = np.array(df['Isolated'])
        array_Final = np.array(df['Final'])
        array_Medial = np.array(df['Medial'])
        array_Initial = np.array(df['Initial'])
        
        # general array combined with everyone
        IPA = np.array(df['IPA'])
        
        
        # dict1 for isolated
        Isolated_dict = {}
        Final_dict = {}
        Medial_dict = {}
        Initial_dict = {}
        try :
            
            if len(array_isolated) == len(IPA) and  len(array_Final) == len(IPA) and len(array_Medial) == len(IPA) and len(array_Initial) == len(IPA):

                for index in range(0,len(IPA)):
                    # for isolated dictionary
                    Isolated_dict[ array_isolated[index].strip(' ')   ] = IPA[index].strip('')

                    # for Final dictionary 
                    Final_dict[array_Final[index].strip(' ')] = IPA[index].strip(' ')

                    # for middle dictionary 
                    Medial_dict[array_Medial[index].strip(' ')] = IPA[index].strip(' ')

                    # for initial dictionary
                    Initial_dict[array_Initial[index].strip(' ')] = IPA[index].strip(' ')

                    # for


                # print("Isolated Dict : ",Isolated_dict)
                # print("Final Dict : ",Final_dict)
                # print("Medial Dict : ",Medial_dict)
                # print("Initial Dict : ",Initial_dict)
        except:
            print("Key value must be equal in df_ipa function ")
        # print("Given char ",TokenChar)
        # print("return char : ",Initial_dict[TokenChar])
        # print("key ",Isolated_dict.keys())
        # print("value",Isolated_dict.values())
        
        
        if TokenChar in Initial_dict:
            if Initial_dict[TokenChar] != None:
                # print("init cond")
                return Initial_dict[TokenChar]
            
        elif TokenChar in Final_dict:
            if Final_dict[TokenChar] != None:
                # print("Final cond")
                return Final_dict[TokenChar]
        elif TokenChar in Medial_dict:
            if Medial_dict[TokenChar] != None:
                # print("Medial cond")
                return Medial_dict[TokenChar]
                
        elif TokenChar in Isolated_dict:
            if Isolated_dict[TokenChar]!= None:
                # print("Isoalted cond")
                return Isolated_dict[TokenChar]
        else:
            with open('NotavailableIPA.txt' , 'w') as file:
                # print('wrote in file')
                file.write(TokenChar)
                Isolated_dict[TokenChar] = 'r'
            return Isolated_dict[TokenChar]


class TextPreProcessing:
    
    def __init__(self,OrginalText):
        self.OrginalText = OrginalText
        # print("Orginal Text :{} ".format(self.OrginalText))
        
        
    def Cleaning(self,Sentance):
        
        # case 0 : remove extra space if exist 
        # RES = Removed Extra spaceed
        RES = Sentance.strip()
        
        
        # case 2 : remove English character if exist :
        # REC  = Removed English Character
        REC = re.sub('[a-zA-Z]' ,"",RES)
        
        # case 3 :  Remove special character:
        # RSC = Removed Special characters
        RSC = re.sub( '[~!@#$%^&*()-_+]' , "",REC )
        
        # console print 
        # print("Cleaned Text : {} ".format(RSC))
        
        return RSC
        
        
        
    
    def Tokenization(self,Sentance):
        # case 1 [Tokenization] from Python lib's
        
        
        TokenizedText = word_tokenize(Sentance)
        
        # print("Tokenized Text : {}".format(TokenizedText))
        
        return TokenizedText
    
    
    def Normalization(sefl,sentance):
        
        # case 3 [Replace Counting digit to Pashto couting words]
        
        MathDigit = ['1','2','3','4','5','6','7','8','9','0']
        
        # iterate over all Math digit and replace with it
        pasto_counting_dict = {
           '1': "يو",
             '2': "دؤه",
             '3':"درے",
             '4':"څلور",
             '5':"پنځه",
             '6':"شپږ",
             '7':"أوؤه",
             '8':"أته",
             '9':"نهه",
             '0' : "صفر"
        }
        
        
        for digit in MathDigit:
            sentance = sentance.replace(digit ,pasto_counting_dict[digit] )
        # print("Normalized Text : {}".format(sentance))
        
        return sentance
    def Testing(self,Text):
        
        # case 1 clean it 
        CleanedText = self.Cleaning(Text)
        
        # case 2 : Normalization
        NormalaizedText = self.Normalization(CleanedText)
        
        # case 3 Tokenization
        
        TokenizedText = self.Tokenization(NormalaizedText)
        
        # print("Final Text : ",TokenizedText)
        
        self.IPA(TokenizedText)
