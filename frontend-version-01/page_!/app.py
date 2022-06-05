import re
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
import pandas as pd
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import numpy as np

# import time
import time
import os

# selenium servies

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



import base64
import boto3
import os
from contextlib import closing

from flask import Flask
from flask import request
from flask import render_template



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
        

class TTS(TextPreProcessing ,linguistic):
    def __init__(self,text,NaiveBaseDF , voice_Select):
        TextPreProcessing.__init__(self,text)
        self.vowels = ['a','ɑ' ,'ā','ə','i','e','ai','əi']
        
        self.consonant = ['b','p' ,'t̪','ʈ','s','d͡ʒ','t͡ʃ','h', 
                          'd','x','t͡s','d͡z' ,'d̪' ,'ɖ','z','r',
                          'ɻ','z','d͡z','ʐ','s','ʃ','x','s','d̪' ,
                          't̪','z','ɣ','ɸ','q','k','ɡ','l','m','n',
                          'ɳ','w','h','t','ṱ','ʈ','θ','ʤ','ʧ',
                         'ħ','χ','ʦ','ʣ','ḓ','ɖ','ð','r','ɻ','ʒ',
                         'ɡʲ','s','ʃ','X','sˤ','dˤ','tˤ','zˤ','ʕ',
                         'ʁ','q','ɳ','ɦ','ʎ',]
        
        # Avaible syllble form that we can generate voice using this
        self.validated_Syllble = ['V','VC','VCC','CV','CVC','CVCC','CCV','CCVC','CCVCC','CCCV' , 'CCCVC' , 'CCCVCC']
        

        self.single_form = pd.read_csv(NaiveBaseDF).set_index('consonant')
        self.voice_Select = voice_Select
        
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

                # test : d̪

                if list_of_IPAs[outer_index][char_index] in self.consonant:
                    # print("yes its a consonent" , list_of_IPAs[outer_index][char_index])

                    # case 1.1 check the next char(Multiple syllables)
                    try :

                        if list_of_IPAs[outer_index][char_index+1] == '͡' or list_of_IPAs[outer_index][char_index+1] == '̪':
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
        Tokens_of_IPA = self.IPA(TokenizedText)
        
        syllbleForm ,list_of_IPA =  self.Make_Syllables(Tokens_of_IPA)
        
        self.turn_into_speech( syllbleForm ,list_of_IPA )
        
       
        # self.single_form.to_csv('NaiveBase_single_form.csv')
                
        
    def turn_into_speech(self,syllbleForm , list_of_IPA):
        print(" syllbleForm  :",syllbleForm)
        print("list_of_IPA : ",list_of_IPA)
        
        #check the list of syllables and list of IPA is equal
        final_ipa_list_to_Send_API = []
        if len(syllbleForm) == len(list_of_IPA):
            
            for index in range(0,len(syllbleForm)):
                
                # check given syllable is valid or not
                # if its not valid call the syllableModification fun to make it correct
                
                if syllbleForm[index] in self.validated_Syllble:
                    print("Valid syllable : ",syllbleForm[index] , list_of_IPA[index] )
                    alread_valid_syllable = list_of_IPA[index]
                    print('alread_valid_syllable : ',alread_valid_syllable)
                    final_ipa_list_to_Send_API.append(alread_valid_syllable)
                
                else:
                    
                    print('calling for modification : ',list_of_IPA[index])
                    modified_IPA = self.syllableModification(list_of_IPA[index])
                    print('modified_IPA :',modified_IPA)
                    final_ipa_list_to_Send_API.append(self.syllableModification(list_of_IPA[index]))
                    
                
        print('final_ipa_list_to_Send_API : ',final_ipa_list_to_Send_API)
        
        # calling AMazong API
        self.polly_handler(final_ipa_list_to_Send_API , self.voice_Select)
        
    def Turn_into_SyllbleForm(self,partial_ipa):
        
        syl_str = ''
        for index,value in enumerate(range(0,len(partial_ipa))):
            if partial_ipa[index] in self.vowels:
                syl_str += 'V'
            else:
                syl_str += 'C'
            
        return syl_str
            
        
    def max_Freq_vowels(self,consonant):
        df =  pd.read_csv('NaiveBase_single_form.csv').set_index('consonant')
        
        vowels_Dictionary = {
                0:'ɑ',
                1:'ā',
                2:'ə',
                3:'i',
                4:'e',
                5:'ai',
                6:'əi'
        }
        # print(df.loc[consonant])
        l1_ = df.loc[consonant]
        print(l1_)
        max_freq = np.argmax(l1_)
        
        print('Return max freq : ',consonant , vowels_Dictionary[max_freq] , max_freq)
        return vowels_Dictionary[max_freq]

            
            
            
            
    def syllableModification(self,WrongIPA):
        
        
        
        ret_modified_IPA_list = []
        
        
        # split the string into lenght of 2
        ipa_text = WrongIPA
        splitted_IPA = [ipa_text[i:i+2] for i in range(0, len(ipa_text), 2)]
        
        # checking 2 lenght of string is valid syllables
        for partial_ipa in splitted_IPA:
            
            partial_ipa_syllable_form = self.Turn_into_SyllbleForm(partial_ipa)
            # print('partial_ipa_syllable_form : ',partial_ipa_syllable_form , partial_ipa)
            
            if  partial_ipa_syllable_form in self.validated_Syllble:
                ret_modified_IPA_list.append(partial_ipa) 
            else:
                try: 
                    
                    print('before modification : ',partial_ipa)
                
                    partial_ipa += self.max_Freq_vowels(partial_ipa[-1])
                
                    print("After modification : ",partial_ipa)
                    ret_modified_IPA_list.append(partial_ipa)
                except:
                    ret_modified_IPA_list.append(partial_ipa)
        return ' '.join(ret_modified_IPA_list)
        
    
    
    def polly_handler(self,text,VoiceId='Salli'):
        aws_access_key_id = 'AKIATTX7A56JFU5UPRUR'
        aws_secret_access_key = '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'
        region_name='us-west-2'

        API_TEXT_String  = ''
        for text_value in text:
            print('text_value : ',text_value)
            API_TEXT_String += text_value + " "
        

        print('API_TEXT_String : ',API_TEXT_String)
        
        polly = boto3.client("polly",region_name=region_name, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

        text = API_TEXT_String
        # voice = event.get("voice", "Salli")

        # strip out slashes if submitted with text string
        if "/" in text:
            text = text.replace("/", "")

        # generate phoneme tag for polly to read
        phoneme = f"<phoneme alphabet='ipa' ph='{text}'></phoneme>"

#         send to polly, requesting mp3 back
#         The valid values for mp3 and ogg_vorbis are "8000", "16000", "22050", and "24000". 
#         The default value for standard voices is "22050". 
#         The default value for neural voices is "24000".
        print("------------------------------------------------------------------------------",VoiceId)
        response = polly.synthesize_speech(
            OutputFormat="mp3",
            TextType="ssml",
            Text=phoneme,
            VoiceId=VoiceId,
            SampleRate = '8000'
        )

        # encode polly's returned audio stream as base64 and return
        if "AudioStream" in response:
                with open('static/audio/play.mp3', 'wb') as f:
                    f.write(response['AudioStream'].read())

                        
    def Stats(self,IPA):
        # print('integrated IPA : ',IPA)
        #check the df
#         print(self.single_form.head(5))
        
        # print('Type(IPA) : {}\n IPA : {}'.format(type(IPA),IPA))
        
         # ['ɑ' ,'ā','ə','i','e','ai','əi']
        for count ,char_id in enumerate(range(0,len(IPA))):
            print('Count {} --> Char {} , IPA : {} , IPA[-1] : {}'.format(count,IPA[char_id],IPA,IPA[-1]))

            # check each if this then increament in df
            # print("--?" ,IPA[char_id: char_id+2])
            # print('i')
            # print('three charc consonant : ',IPA[char_id:char_id+3])

            for cons in self.consonant:
                
                # for single lenght
                if  IPA[char_id] != IPA[-1]:
                    
                    try :
                        if IPA[char_id +1] =='ā' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ā'] = self.single_form.loc[cons,'ā'] +1
                            
                        if IPA[char_id +1] =='ɑ' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ɑ'] = self.single_form.loc[cons,'ɑ'] +1
                            
                        if IPA[char_id +1] =='ə' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ə'] = self.single_form.loc[cons,'ə'] +1
                        
                        if IPA[char_id +1] =='i' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        if IPA[char_id +1] =='e' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        # print(IPA[char_id +1:char_id +3])
                        if IPA[char_id +1:char_id +3] =='əi' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'əi'] = self.single_form.loc[cons,'əi'] +1
                        
                        
                        if IPA[char_id +1,char_id +3] =='ai' and IPA[char_id] == cons:
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                    except:
                        continue
                    
                
                
                
                # for three character consonant base
                if (IPA[char_id:char_id+3] != IPA[-3:]):
                    # mean not last index
                    
                    try :
                        if IPA[char_id+4]=='ā' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ā'] = self.single_form.loc[cons,'ā'] +1
                            
                        if IPA[char_id+4]=='ɑ' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ɑ'] = self.single_form.loc[cons,'ɑ'] +1
                            
                            
                        if IPA[char_id+4]=='i' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        
                        if IPA[char_id+4]=='e' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        
                        
                        if IPA[char_id+4:char_id+7]=='ai' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                        if IPA[char_id+4:char_id+7]=='əi' and IPA[char_id:char_id+3] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+3] ,cons , IPA[char_id] != IPA[-3:] , IPA[char_id+4])
                            self.single_form.loc[cons,'əi'] = self.single_form.loc[cons,'əi'] +1
                        
                            
                            
                    except:
                            # print(IPA[char_id+5])
                            continue
                
                
                # for 2 lenght of cosonant character
                if (IPA[char_id:char_id+2] != IPA[-2:]):
                    # print(IPA[char_id:char_id+3] , IPA[-2:])

                    try :
                        if IPA[char_id+3]=='ā' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'ā'] = self.single_form.loc[cons,'ā'] +1
                            
                        if IPA[char_id+3]=='ɑ' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'ɑ'] = self.single_form.loc[cons,'ɑ'] +1
                            
                            
                        if IPA[char_id+3]=='i' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'i'] = self.single_form.loc[cons,'i'] +1
                        
                        
                        if IPA[char_id+3]=='e' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'e'] = self.single_form.loc[cons,'e'] +1
                        
                        
                        if IPA[char_id+3:char_id+5]=='ai' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons , IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+3])
                            self.single_form.loc[cons,'ai'] = self.single_form.loc[cons,'ai'] +1
                        
                        if IPA[char_id+3:char_id+5]=='əi' and IPA[char_id:char_id+2] == cons :
                            # print('break------------ : ',IPA[char_id:char_id+2] ,cons ,IPA[char_id:char_id+2] != IPA[-2:] , IPA[char_id+33])
                            self.single_form.loc[cons,'əi'] = self.single_form.loc[cons,'əi'] +1
                        
                            
                            
                    except:
                            # print(IPA[char_id+5])
                            continue
                
                 


app = Flask(__name__)


@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/Documentaion.html')
def Documentaion():
    return render_template('Documentaion.html')


@app.route("/",methods=['POST','GET'])
def index():

    if request.method =='POST':
        if request.form['rebot-Voice'] == 'Generate Audio':
            RawInput = request.form['user_content']
            
            # os.remove('static/audio/play.mp3')
            voice_select = request.form['voice-select']
            print('Voice Select Name : ',voice_select)
            
        Object =  TTS(RawInput , 'NaiveBase_single_form.csv' , str(voice_select))
        Object.Testing(RawInput)
        print('within object : ',Object.voice_Select)

        

        # time.sleep(3)
        path_ = 'static/audio/play.mp3'
        return  render_template('index.html' , path=path_)
    else:
        return render_template('index.html' , path= None)


if __name__ == "__main__":
    app.run(debug=True  )
