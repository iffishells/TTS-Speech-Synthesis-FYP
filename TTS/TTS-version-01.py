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
           '1': "????",
             '2': "??????",
             '3':"??????",
             '4':"????????",
             '5':"????????",
             '6':"??????",
             '7':"????????",
             '8':"??????",
             '9':"??????",
             '0' : "??????"
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

        
        
class TTS(TextPreProcessing ,linguistic):
    def __init__(self,text,NaiveBaseDF):
        TextPreProcessing.__init__(self,text)
        self.vowels = ['??' ,'??','??','i','e','ai','??i']
        
        self.consonant = ['b','p' ,'t??','??','s','d????','t????','h', 
                          'd','x','t??s','d??z' ,'d??' ,'??','z','r',
                          '??','z','d??z','??','s','??','x','s','d??' ,
                          't??','z','??','??','q','k','??','l','m','n',
                          '??','w','h','t','???','??','??','??','??',
                         '??','??','??','??','???','??','??','r','??','??',
                         '????','s','??','X','s??','d??','t??','z??','??',
                         '??','q','??','??','??',]
        
        # Avaible syllble form that we can generate voice using this
        self.validated_Syllble = ['V','VC','VCC','CV','CVC','CVCC','CCV','CCVC','CCVCC','CCCV' , 'CCCVC' , 'CCCVCC']
        

        self.single_form = pd.read_csv(NaiveBaseDF).set_index('consonant')
        
    def Make_Syllables(self,list_of_IPAs):
        # print(list_of_IPAs)
        sylb_list = []

        for outer_counter , outer_index in enumerate(range(0,len(list_of_IPAs))):

            # pick the Single IPA

            sylb_form = ''
            for char_counter , char_index in enumerate(range(0,len(list_of_IPAs[outer_index]))):

                # now you have single char IPA
                # print('char Counter {} and char {}'.format(char_counter ,list_of_IPAs[outer_index][char_index]))

                # case 1 check the given char is consonent ?

                # test : d??

                if list_of_IPAs[outer_index][char_index] in self.consonant:
                    # print("yes its a consonent" , list_of_IPAs[outer_index][char_index])

                    # case 1.1 check the next char(Multiple syllables)
                    try :

                        if list_of_IPAs[outer_index][char_index+1] == '??' or list_of_IPAs[outer_index][char_index+1] == '??':
                            # print("meet 1 cond ", list_of_IPAs[outer_index][char_index+1])
                            sylb_form += "C"
                        else:
                            # print("meet 2 cond")
                            sylb_form += "C"
                    except:
                        if list_of_IPAs[outer_index][char_index] in self.consonant:
                            # print("meet 3 cond")
                            sylb_form += "C"
                        elif list_of_IPAs[outer_index][char_index] in self.vowels:
                            # print("meet 4 cond") 
                            sylb_form += "V"


                elif list_of_IPAs[outer_index][char_index] in self.vowels:
                    # print("yes its a vowels")
                    sylb_form += "V"
                else:
                    # for space
                    if list_of_IPAs[outer_index][char_index] == ' ':
                        sylb_form += " "
                    continue
            sylb_list.append(sylb_form)
            # print('sylb_form : ',sylb_form)
        # print(sylb_list)            
        # print(list_of_IPAs)
        
        return sylb_list ,list_of_IPAs  
    
            
    def Testing(self,Text):
        
        # case 1 clean it 
        CleanedText = self.Cleaning(Text)
        
        # case 2 : Normalization
        NormalaizedText = self.Normalization(CleanedText)
        
        # case 3 Tokenization
        
        TokenizedText = self.Tokenization(NormalaizedText)
        
        # print("Final Text : ",TokenizedText)
        
        # print(self.IPA(TokenizedText))
        
        syllbleForm ,list_of_IPA =  self.Make_Syllables(self.IPA(TokenizedText))
        
        self.turn_into_speech( syllbleForm ,list_of_IPA )
        
        # self.single_form.to_csv('NaiveBase_single_form.csv')
                
        
    def turn_into_speech(self,syllbleForm , list_of_IPA):
        print(" syllbleForm  :",syllbleForm)
        print("list_of_IPA : ",list_of_IPA)
        
        #check the list of syllables and list of IPA is equal
        if len(syllbleForm) == len(list_of_IPA):
            
            for index in range(0,len(syllbleForm)):
                
                self.polly_handler(list_of_IPA[index])

                # if given syllable form in validated syllables mean its correct syllables ,it can speack
                # if syllbleForm[index] in self.validated_Syllble:
                #     # print("validated syllables : ",list_of_IPA[index])
                #     # print()
                #     polly_handler(list_of_IPA[index])
                # else:
                #     print("Not validated syllables : ",list_of_IPA[index])
                    
                    
                    
    def syllableModification(self,WrongIPA):
        pass
    
    
    def polly_handler(self,text,VoiceId='Salli'):
        aws_access_key_id = 'AKIATTX7A56JM4EMUCVY' 
        aws_secret_access_key = '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' 
        region_name='us-west-2'

        polly = boto3.client("polly",region_name=region_name, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)


        # voice = event.get("voice", "Salli")

        # strip out slashes if submitted with text string
        if "/" in text:
            text = text.replace("/", "")

        # generate phoneme tag for polly to read
        phoneme = f"<phoneme alphabet='ipa' ph='{text}'></phoneme>"

        # send to polly, requesting mp3 back
        #The valid values for mp3 and ogg_vorbis are "8000", "16000", "22050", and "24000". 
        #The default value for standard voices is "22050". 
        #The default value for neural voices is "24000".
        response = polly.synthesize_speech(
            OutputFormat="mp3",
            TextType="ssml",
            Text=phoneme,
            VoiceId='Salli',
            SampleRate = '16000'
        )

        # encode polly's returned audio stream as base64 and return
        if "AudioStream" in response:
    #         with closing(response["AudioStream"]) as stream:
    #             audio = base64.encodebytes(stream.read())

    #         return audio.decode("ascii")
            with open('audio/play.mp3', 'wb') as f:
                f.write(response['AudioStream'].read())


            # Use the pygame module from within Linux or Raspberry Pi. Not MP3 support for MP3 on Windows
        # !pip install pygame
        from pygame import mixer # Load the required library
        mixer.init()
        mixer.music.load('audio/play.mp3')
        mixer.music.play()

        

                    
                
                        
    def Stats(self,IPA):
        # print('integrated IPA : ',IPA)
        #check the df
#         print(self.single_form.head(5))
        
        # print('Type(IPA) : {}\n IPA : {}'.format(type(IPA),IPA))
        
         # ['??' ,'??','??','i','e','ai','??i']
        for count ,char_id in enumerate(range(0,len(IPA))):
            # print('Count {} --> Char {} , IPA : {} IPA[-1] : {}'.format(count,IPA[char_id],IPA,IPA[-1]))

            # check each if this then increament in df
            # print("--?" ,IPA[char_id: char_id+2])
            # print('i')
            # print('three charc consonant : ',IPA[char_id:char_id+3])

            for cons in self.consonant:
                
                # for single lenght
                if  IPA[char_id] != IPA[-1]:
                    
                    try :
                        if IPA[char_id +1] =='??' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                        if IPA[char_id +1] =='??' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                        if IPA[char_id +1] =='??' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                        
                        if IPA[char_id +1] =='i' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        if IPA[char_id +1] =='e' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        # print(IPA[char_id +1:char_id +3])
                        if IPA[char_id +1:char_id +3] =='??i' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??i'] = self.single_form.loc[cons,'??i'] +1
                        
                        
                        if IPA[char_id +1,char_id +3] =='ai' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                    except:
                        continue
                    
                
                
                
                # for three character consonant base
                if (IPA[char_id:char_id+3] != IPA[-3:]):
                    # mean not last index
                    
                    try :
                        if IPA[char_id+4]=='??' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                        if IPA[char_id+4]=='??' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                            
                        if IPA[char_id+4]=='i' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        
                        if IPA[char_id+4]=='e' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        
                        
                        if IPA[char_id+4:char_id+7]=='ai' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                        if IPA[char_id+4:char_id+7]=='??i' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'??i'] = self.single_form.loc[cons,'??i'] +1
                        
                            
                            
                    except:
                            # print(IPA[char_id+5])
                            continue
                
                
                # for 2 lenght of cosonant character
                if (IPA[char_id:char_id+2] != IPA[-2:]):
                    # print(IPA[char_id:char_id+3] , IPA[-2:])

                    try :
                        if IPA[char_id+3]=='??' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                        if IPA[char_id+3]=='??' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'??'] = self.single_form.loc[cons,'??'] +1
                            
                            
                        if IPA[char_id+3]=='i' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        
                        if IPA[char_id+3]=='e' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        
                        
                        if IPA[char_id+3:char_id+5]=='ai' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                        if IPA[char_id+3:char_id+5]=='??i' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons ,IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+33])
                            self.single_form.loc[cons,'??i'] = self.single_form.loc[cons,'??i'] +1
                        
                            
                            
                    except:
                            # print(IPA[char_id+5])
                            continue
                
                 


            # print(self.single_form)

    
    def request_to_read_IPA(self,ipa):


        #  getting input tags
        input_ipa = driver.find_element('id','ipa-text')
        
        input_ipa.clear()
        # sennding IPA
        input_ipa.send_keys(ipa)

        # getting read button
        read_button = driver.find_element('id','submit')
        
        read_button.click()
        
     
        