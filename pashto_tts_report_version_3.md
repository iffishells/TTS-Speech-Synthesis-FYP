

Pashto Text To Speech System

Project Team

Aimen Wadood

P18-0002

P18-0054

Muhammad Iftikhar

Muhammad Hamza Majeed P18-0128

Session 2021-2022

Supervised by

Dr. Muhammad Taimoor Khan

Department of Computer Science

National University of Computer and Emerging Sciences

Peshawar, Pakistan

July, 2022





Student’s Declaration

We declare that this project titled “Pashto Text To Speech System”, submitted as require-

ment for the award of degree of Bachelors in Computer Science, does not contain any

material previously submitted for a degree in any university; and that to the best of our

knowledge, it does not contain any materials previously published or written by another

person except where due reference is made in the text.

We understand that the management of Department of Computer Science, National Uni-

versity of Computer and Emerging Sciences, has a zero tolerance policy towards plagia-

rism. Therefore, We, as authors of the above-mentioned thesis, solemnly declare that no

portion of our thesis has been plagiarized and any material used in the thesis from other

sources is properly referenced.

We further understand that if we are found guilty of any form of plagiarism in the thesis

work even after graduation, the University reserves the right to revoke our BS degree.

Aimen Wadood

Signature:

Signature:

Signature:

Muhammad Iftikhar

Muhammad Hamza Majeed

Veriﬁed by Plagiarism Cell Ofﬁcer

Dated:





Certiﬁcate of Approval

The Department of Computer Science, National University of Computer and Emerging

Sciences, accepts this thesis titled Pashto Text To Speech System, submitted by Aimen

Wadood (P18-0002), Muhammad Iftikhar (P18-0054), and Muhammad Hamza Majeed

(P18-0128), in its current form, and it is satisfying the dissertation requirements for the

award of Bachelors Degree in Computer Science.

Supervisor

Dr. Muhammad Taimoor Khan

Signature:

Mashal Khan

FYP Coordinator

National University of Computer and Emerging Sciences, Peshawar

Dr. Hafeez Ur Rehman

HoD of Department of Computer Science

National University of Computer and Emerging Sciences





Acknowledgements

First and foremost, all praises and thanks to ALLAH ALMIGHTY that he gave us the

power and knowledge to complete such an immense project. We would also like to extend

our deepest gratitude to Dr. Muhamamd Taimoor Khan who supported and guided us

throughout this project. Without him, it would have been impossible for us to carry out

this project. Despite his busy schedule, he would always ﬁnd time whenever we have to

meet him. We would also like to thank all the teachers who were always ready to solve

our queries whenever we needed them. Last but not least we would like to thank all our

friends who gave useful suggestions regarding our project.

Aimen Wadood

Muhammad Iftikhar

Muhammad Hamza Majeed





Abstract

Text to Speech Systems (TTS) has received immense interest from professionals over the

years. Different TTS have been developed in a variety of languages however there is

not much developed in the Pashto language. Pashto is a vast language having 19 di-

alects. It is the native language of around 15.4 million, mainly across Afghanistan and

Pakistan.Previously Pashto TTS were developed on RNN with bi-directional LSTM and

concatenative synthesis. The accuracy of RNN was 74 percent but it requires a huge

amount of data. The accuracy of concatenative synthesis was 80 percent but it is com-

plex. In this report the we developed TTS that is based on sequential model HMM. It

consists of two parts; text pre-processing and an HMM-based speech synthesizer. The

main challenges included the language dependant components such as tokenization, parts

of speech tagging, phrase breakers, phonetic dictionaries, and letter to sound mapping.

However, better performance can be achieved with more data and with other dialects con-

sidered. The accuracy of the system is evaluated by two methods subjective and objective.

The accuracy of HMM outstands all the previous models.





Contents

1 Preliminaries and Introduction

[1](#br10)

[1](#br10)

[2](#br11)

[2](#br11)

[3](#br11)

[3](#br12)

1.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1.2 Problem Statement . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1.3 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1.4 Objectives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1.5 Scope . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2 Review of Literature

[5](#br14)

[5](#br14)

[5](#br14)

[6](#br15)

[6](#br15)

[8](#br16)

[8](#br17)

[9](#br18)

[9](#br18)

2.1 Articulatory Synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2 Formant Synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.3 Concatenative Synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.3.1 Diphone Concatenation Synthesis . . . . . . . . . . . . . . . . .

2.3.2 Unit Selection Concatenative Synthesis . . . . . . . . . . . . . .

2.4 Deep Neural Network Synthesis . . . . . . . . . . . . . . . . . . . . . .

2.5 End to End Deep Learning Synthesis . . . . . . . . . . . . . . . . . . . .

2.5.1 Tacotron . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.5.2 FastSpeech . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [10](#br19)

2.5.3 WaveNet . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [11](#br20)

2.5.4 Glow TTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [12](#br21)

2.6 Comparison Of Different Techniques . . . . . . . . . . . . . . . . . . . . [13](#br22)

3 System Design and Analysis

[15](#br24)

3.1 Usecase Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [15](#br24)

3.2 Activity Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [16](#br25)

3.3 Class Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [17](#br26)

ii





3.4 Sequence Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [18](#br27)

4 Methodology [19](#br28)

4.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [19](#br28)

4.2 Corpus . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [20](#br28)

4.3 Text Preprocessing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [20](#br29)

4.3.1 Normalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . [20](#br29)

4.3.2 Tokenization . . . . . . . . . . . . . . . . . . . . . . . . . . . . [20](#br29)

4.3.3 Removal of Stop Words . . . . . . . . . . . . . . . . . . . . . . . [21](#br30)

4.4 Parts Of Speech Tagging . . . . . . . . . . . . . . . . . . . . . . . . . . [21](#br30)

4.5 Phonetic Lexicon Lookup . . . . . . . . . . . . . . . . . . . . . . . . . . [22](#br31)

4.6 Letter to Sound Mapping . . . . . . . . . . . . . . . . . . . . . . . . . . [23](#br32)

4.7 IPA Transcription . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [23](#br32)

4.8 HMM Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [23](#br32)

4.8.1 HMM Training Part . . . . . . . . . . . . . . . . . . . . . . . . . [24](#br33)

4.8.2 HMM Synthesis Part . . . . . . . . . . . . . . . . . . . . . . . . [25](#br34)

References

[29](#br36)





List of Figures

2.1 Architecture of Diphone Concatenation Synthesis . . . . . . . . . . . . .

2.2 Architecture of RNN . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[7](#br16)

[9](#br18)

2.3 Architecture of Tacotron [[18](#br38)] . . . . . . . . . . . . . . . . . . . . . . . . [10](#br19)

2.4 Architecture of Fast Speech [[13](#br37)] . . . . . . . . . . . . . . . . . . . . . . [11](#br20)

2.5 Architecture of WaveNet [[10](#br37)] . . . . . . . . . . . . . . . . . . . . . . . . [12](#br21)

2.6 Architecture of Glow TTS . . . . . . . . . . . . . . . . . . . . . . . . . [13](#br22)

3.1 Usecase Diagram of Pashto Text to Speech System . . . . . . . . . . . . [16](#br25)

3.2 Activity Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [17](#br26)

3.3 Class Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [18](#br27)

3.4 Sequence Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [18](#br27)

4.1 Architecture Of Methodology . . . . . . . . . . . . . . . . . . . . . . . . [19](#br28)

4.2 Tokenization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [21](#br30)

4.3 Stemming in Pashto . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [21](#br30)

4.4 Parts Of Speech Tagging Architecture . . . . . . . . . . . . . . . . . . . [22](#br31)

4.5 Training and Synthesis Parts Of HMM . . . . . . . . . . . . . . . . . . . [24](#br33)

iv





List of Tables

2.1 Comparison of different techniques . . . . . . . . . . . . . . . . . . . . . [14](#br23)

4.1 Base Rules Of POS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . [23](#br32)

0





Chapter 1

Preliminaries and Introduction

Text to Speech System (TTS) is the artiﬁcial production of human speech. It takes raw

data as input and then after applying pre-processing converts it into digital signals which

then forges natural-sounding speech. The chapter introduces the following sections: an

overview of the text to speech, problem statement, motivations, limitations, and scope.

1.1 Overview

Nowadays communications play a vital role to connect the world. It is nearly impossible

to live without communication. One of the forms of communication exchange is through

text to speech. It beneﬁts people in different forms. Numerous TTS has been developed

for the English language but very few are built for other languages, Pashto is one of them.

The main challenge in developing Pashto TTS is that it consists of 45 alphabets so its

phonetics transcription is difﬁcult as compared to other languages. The sentence structure

of Pashto language is subject-object-verb which is same as that of Urdu. In this project,

we have developed Pashto TTS using Hidden Markov Model (HMM). It is a statistical

model in which the system being modeled is assumed to be a Markov process. Our sys-

tem has two major components, preprocessing, and an HMM-based speech synthesizer.

In the preprocesisng part, the input text is processed and converted into words by apply-

ing normalization, tokenization, chunking, stemming, POS (Parts Of Speech) tagger, and

1





\1. Preliminaries and Introduction

parsing. Every individual word is then given a sound by IPA transcription. In the HMM-

based speech synthesizer, each signal is then passed through a parameter generator and

the synthesized speech is produced.The accuracy is measured by objective and subjec-

tive evaluation. In the subjective method of evaluating, the MOS score is measured by a

group of language experts. The objective method is an extrinsic evaluation which is done

by different evaluating matrices.

1.2 Problem Statement

There is a very limited text-to-speech system developed for Pashto. They were developed

on RNN with bi-directional LSTM and concatenative synthesis. The accuracy of RNN

was 74 percent but it requires a huge amount of data. The accuracy of concatenative

synthesis was 80 percent but it is complex.

1.3 Motivation

• Text To Speech System is useful for learning a new language. While learning new

language people face difﬁculties in pronunciations. They need TTS systems to

ﬂuently speak new languages.

• People with learning disabilities have a problem in reading large text due to dyslexia

beneﬁts from TTS systems.

• People who read online and do not have access to laptops read on small screens of

their mobile phones which makes it difﬁcult for them to read the text.

• TTS system is beneﬁcial for people who are visually impaired. By this feature, a

lot of online content is accessible to them.

• Apps like Google Translate are useful for cross-culture communication and it is

also based on the TTS system.

2





1.4 Objectives

1.4 Objectives

The main objective of this project is to develop a TTS for the Pashto language and to

generate sound that is close to humans. And to improve accuracy of the previous work.

1.5 Scope

Initially, we will train our model on the standard dialect of Pashto, then will move to one

more dialect. Our focus will be on using a sequential model. We will not consider all

dialects of Pashto.

3









Chapter 2

Review of Literature

This chapter provides a comprehensive literature review on Text to Speech Systems. Sev-

eral methods have been proposed in the literature. Each of these methods has its pros and

cons.

2.1 Articulatory Synthesis

Articulatory Synthesis has been built on the human speech production system. It recon-

stitutes vocal track shape. To generate a human-like speech, the human vocal tract is

modeled combining electrical, mechanical, and electronic components. To generate the

signal, a simulation of air is passed through the vocal tract [[11](#br37)]. The parameters of the

synthesizer are the vocal cord tension and respective position of articulatory organs. The

advantage of articulatory synthesis is that it needs no speech database. Its limitations are

that it is difﬁcult to debug, human vocal tract precision is hard, and it produces robotic

sound.

2.2 Formant Synthesis

Formant Synthesis utilizes a rule-based approach.Unlike Articulatory Synthesis it is based

on the resonant frequencies of the vocal tract.These frequencies and noise levels vary from

5





\2. Review of Literature

time to time to generate speech waveforms. To generate intelligible and natural-sounding

speech, at least three formant synthesizers are required [[9](#br37)]. However, up to ﬁve Formant

Synthesizers are built for higher-quality speech. A pole resonator is required to man-

age formant frequencies and their bandwidth. Like Articulatory Synthesis, it requires no

speech database.Its limitations are that estimation of the vocal tract is hard, and updating

and modiﬁcation of frequency at each phoneme is difﬁcult.

2.3 Concatenative Synthesis

In the ﬁrst step whole sentences are recorded as syllables by voice actors which are then

labeled and stored in a database as phones, diphones, and triphones. During speech syn-

thesis, it searches the whole database for matching speech units as that of input and then

concatenates them and produces audio. It is divided into the following subcategories;

2.3.1 Diphone Concatenation Synthesis

It is based on the same principles as that of concatenative synthesis. The only difference

is that instead of phones, diphones are used as concatenative units [[6](#br36)]. The advantage of

diphone concatenative synthesis is that it produces highly natural speech. Its limitation is

its dependency on the database.

6





2.3 Concatenative Synthesis

Figure 2.1: Architecture of Diphone Concatenation Synthesis

7





\2. Review of Literature

2.3.2 Unit Selection Concatenative Synthesis

In unit selection, there are two methods.The ﬁrst technique is based on target cost. It uses

a database to match the input units and then concatenate them together to produce the

audio.Target cost and concatenation cost are two major roles in this technique.Target cost

indicates how accurately the input unit matches the candidate unit from the database. A

heuristic function is deﬁned to measure target cost [[1](#br36)]. The model tries to minimize the

overall cost. Its limitation is that it is dependant on the database. The second technique is

based on clustering. To avoid the heuristic function clustering is used which allows pre-

calculated target cost and then the same clusters are mapped on the decision tree.Then it

is searched for the available features. Its limitation is the same as the ﬁrst technique.

2.4 Deep Neural Network Synthesis

The use of deep learning is currently the state of the art in the text to speech synthesis. It

is based on statistical models. In Deep Neural Networks(DNN) sentences are converted

into characters embeddings. Character embeddings are a numeric representation of words

[[1](#br36)]. These can be used to create numeric representations of paragraphs, documents, etc.

Character embeddings are then fed to Recurrent sequence to sequence feature prediction

which predicts the sequence of spectrograms. It consists of an encoder, an attention net-

work, and a decoder network. The encoder encodes character embeddings into the hidden

features.The output of encoding is the input of the attention network which produces a

ﬁxed-length vector in each step. The decoder is the regressive neural network (RNN) [[3](#br36)]

which takes the output of the attention network as input and predicts the sequence of the

spectrogram from the hidden feature representation. The output of DNN is not readable

by humans but it is readable for computers. The limitation of deep learning models is that

it requires a large amount of data.

8





2.5 End to End Deep Learning Synthesis

Figure 2.2: Architecture of RNN

2.5 End to End Deep Learning Synthesis

Deep Neural Networks requires multiple-stage but it has some limitations. Its limitations

are that building a new system is complex, every component is trained individually, every

component requires immense expertise which is difﬁcult. On the other hand, end-to-end

text-to-speech synthesis requires minimal human annotation and can be trained on pairs

which eliminate the engineering efforts [\[](#br36)[4](#br36)]. It is ﬂexible in adapting new data. It allows us

to train noisy data. Following are the types of end-to-end text-to-speech synthesis models.

2.5.1 Tacotron

Tacotron is a generative model. It takes text audio pair as input and outputs its spectro-

gram [\[](#br38)[19](#br38)]. It is based on sequence learning with an attention model. The advantage of

Tacotron is that it produces high-quality speech. Its shortcoming is that it is computation-

ally expensive to train the model.

9





\2. Review of Literature

Figure 2.3: Architecture of Tacotron [[18](#br38)]

Figure [2.3](#br19)[ ](#br19)the model takes characters as input and generates spectrogram as output which

is then converted to synthesized speech after passing through linear scaling algorithm

“Grifﬁn-Lim”. CBHG module is the 1-D convolutional layer + network + bi-directional

GRU. It uses RNN as an encoder and decoder. Pre-net is the processed network. The

attention mechanism is applied in the decoder part.

2.5.2 FastSpeech

FastSpeech generates Mel-spectrogram in parallel. The major component of the feed-

forward transformer is the feed-forward transformer block(FFT block). It consists of a

convoultional layer and attention model. It converts phoneme to Mel spectrogram se-

quence [[13](#br37)]. There is a length regulator which acts as a bridge of length mismatch of

phoneme and Mel spectrogram sequences. The number of Mel spectrogram that aligns

with phoneme is called phoneme duration. The length regulator expands the sequence of

10





2.5 End to End Deep Learning Synthesis

phonemes to match the length of the Mel spectrogram. The limitation of FastSpeech is

that it can not be trained without external aligners.

Figure 2.4: Architecture of Fast Speech [[13](#br37)]

In Figure [2.4](#br20), feedforward module takes phoneme as input and by stacking FFT block

it passes the spectrogram to the length regulator. The length regular matches the length

of phoneme and spectrogram. Duration Predictor predicts how much time is consumed

during matching and generating spectrogram. It is a 2-D convolutional layer. FFT block

is a 1-D convolutional layer.

2.5.3 WaveNet

WaveNet was the ﬁrst model that works on raw audio waveform directly. It is an auto-

regressive model where each unit depends on the previous one. It is built on a full con-

volutional neural network (CNN). As shown in the ﬁgure, each convolutional layer has a

dilation factor [[14](#br37)]. Real waveforms recorded by humans were used during training. The

ﬁnal waveform is provided by the network. First, a sample value is found by the distri-

bution. Then this value is fed back to the input and then it generates a new prediction.

The process is continued until the entire speech waveform is generated. The limitation

11





\2. Review of Literature

of WaveNet is that the sample value is fed again and again to the input at every step so

this makes it computationally expensive. And errors will propagate and will affect the

synthesized speech.

Figure 2.5: Architecture of WaveNet [[10](#br37)]

In Figure [2.5](#br21), each convolutional layer has some dilation factor. The input nodes are the

leaves while the output nodes are the root. Green nodes show the intermediate computa-

tion. As it forms a binary tree therefore its computational cost for a single output is O(2L)

where L is the layers in the network.

2.5.4 Glow TTS

Glow TTS is a ﬂow-based generative model. It does not require external aligners. It

is designed in such a way that it does not skip any alignments between text and speech

representations. It consists of two major components; a decoder and encoder duration

12





2.6 Comparison Of Different Techniques

predictor. The decoder contains one convolutional layer, normalization layer, and afﬁne

layer. The encoder has a relative positioning module in the attention model [[8](#br37)]. The du-

ration predictor consists of two convolutional layers. A major shortcoming of Glow TTS

is that it sometimes produces slurry speech.

Figure 2.6: Architecture of Glow TTS

2.6 Comparison Of Different Techniques

Table [2.1](#br23)[ ](#br23)shows comparison between different techniques of text to speech system [\[](#br37)[16](#br37)].

13





\2. Review of Literature

Table 2.1: Comparison of different techniques

Technique

Articulatory

Formant

Corpus size

Naturalness Intelligibility Complexity

Corpus Independant Low

Corpus Independant Low

High

High

High

High

Very high

High

Concatenative Large

HMM Large

High

High

Low

Low

14





Chapter 3

System Design and Analysis

This chapter provides an analysis of the project. In system analysis, use case, activity,

class, and sequence diagrams are given so that a proper workﬂow is followed in project

completion.

3.1 Usecase Diagram

UseCase diagram visualizes how different actors interact with the system. User inputs

text. The text is then processed and then assigned tags. These tags are then given sound

through IPA. Not all the words are tagged. Some of them are tagged manually which

is then given an IPA transcription. These spectrograms move to the parameter generator

where the waveform of the input text is generated. The output is then shown to the user.

There is no use-case descriptions because our project is not for every user.

15





\3. System Design and Analysis

«Pashto Text to Speech System»

Input Text

≪include≫

Text Pre-processing

user

IPA

≪include≫

POS Tagging

≪include≫

Phonetics Lookup

≪include≫

Generate Speech

Letter to Sound Mapping

≪include≫

Parameter Generation

≪include≫

≪

include≫

Excitation

Speech Synthesis

Figure 3.1: Usecase Diagram of Pashto Text to Speech System

3.2 Activity Diagram

The activity diagram helps to understand the project in terms of constraints and conditions

that cause the events. A user inputs the text and then chooses dialect. If the desired

dialect is found then the text is processed and the waveform is generated which is then

synthesized. If the desired dialect is not selected then the user will quit the system.

16





3.3 Class Diagram

Figure 3.2: Activity Diagram

3.3 Class Diagram

The class diagram shows how different classes interact with each other. Use class will

give the raw text to the Text processing class. Text processing class has a child class

“processing class”. This class will perform functions like normalization, tokenization,

stop words removal. The output of the processing class will be the input of the POS

tagging class. In this class, all the words will be assigned tags. In the letter to sound class,

the tags are given sound which uses IPA class. Then DSP class performs functions like

excitation, parameter generation to produce speech waveform.

17





\3. System Design and Analysis

Figure 3.3: Class Diagram

3.4 Sequence Diagram

Sequence diagram tells the sequence in which the system ﬂows.

Figure 3.4: Sequence Diagram

18





Chapter 4

Methodology

4.1 Overview

As discussed earlier, we have used Hidden Markov Model (HMM) [\[](#br38)[17](#br38)]. The basic archi-

tecture of our system is shown in the Figure [4.1](#br28).

Figure 4.1: Architecture Of Methodology

Major components of our system are;

\1. Text preprocessing.

\2. POS Tagging.

\3. Phonetic Lexicon Lookup.

\4. Letter to sound mapping.

\5. I PA Transcription.

\6. HMM, Model.

19





\4. Methodology

4.2 Corpus

We have dataset for parts-of-speech tag and for speech we will scrap it.

4.3 Text Preprocessing

In the ﬁrst step, the textual corpus is processed. Pre-processing is an important step be-

cause it gets rid of the data that is not helpful while training our model. It takes raw input

and converts it into normalized text. Following are the steps involved in pre-processing.

4.3.1 Normalization

A token is made up of two things; a morpheme and preﬁx or sufﬁx. Morpheme in Natural

Language Processing is the base word. In normalization, A token is converted into its

base word [[2](#br36)]. In Pashto language normalization is usually done on cardinal and ordinal

digits or dates. Cardinal number is “how many” for example one, two, etc. The ordinal

number is the “position” for example 1st, 2nd, etc.

4.3.2 Tokenization

Tokenization means splitting sentences into tokens. Tokens can be words, characters,

symbols. This is done by splitting the sentence from the white spaces. Tokenization can

be performed on sentence-level or at word level or even at the character level. Figure [4.2](#br30)

shows how tokenization is done in the Pashto language.

20





4.4 Parts Of Speech Tagging

Figure 4.2: Tokenization

4.3.3 Removal of Stop Words

Symbols that make no sense in sentences are removed in this step. Figure [4.3](#br30)[ ](#br30)shows

removal of stop words in Pashto.

Figure 4.3: Stemming in Pashto

4.4 Parts Of Speech Tagging

It takes normalized text as input and assigns tags to it as shown in Figure [4.4](#br31).

These tags are given to the words by trigram language model and POS lexicon [[7](#br36)]. Every

word is given a probability and based on that probably it is decided that what tag should

be assigned to it. Those words whose tag is not decided are marked outside the Parts Of

Speech (POS) lexicon. We have applied POS tags based on some rules [[12](#br37)]. The base

rules are shown is [4.1](#br32).

21





\4. Methodology

Figure 4.4: Parts Of Speech Tagging Architecture

4.5 Phonetic Lexicon Lookup

It contains words and their respective parts of speech tag. Initially, tags are assigned man-

ually. These include tags such as prepositions, conjunctions, interjunctions, and pronouns.

Lexicon lookup will grow when real input is given.

22





4.6 Letter to Sound Mapping

Table 4.1: Base Rules Of POS

4.6 Letter to Sound Mapping

Those words whose lexicon pronunciation is not found are then passed to the letter to

sound module. These words are given the rule-based letter to sound conversion is imple-

mented [[15](#br37)]. Then these words are given to CISAMPA module to assign its compatible

symbols to these words. Generated transcription of input text is then moved to speech

synthesis engine.

4.7 IPA Transcription

Those words whose tags are assigned are then given transcriptions based on IPA symbols

[[20](#br38)]. I PA transcription is converted to CISAMPA. The lexicon is passed to the CISAMP

to verify that it is in a compatible format. Then these are passed to the synthesis engine.

4.8 HMM Model

Hidden Markov Model (HMM) is the statistical parametric model [[5](#br36)]. It has two parts

training part and the synthesis part as shown in Figure [4.5](#br33)

23





\4. Methodology

Figure 4.5: Training and Synthesis Parts Of HMM

4.8.1 HMM Training Part

In the training part, maximum likelihood is estimated by [4.1](#br33)

o = argmaxo[p(o|w,λ)]

(4.1)

24





4.8 HMM Model

where λ is the set of model parameters, O is the set of training information, and W is the

set of words for O.

The training part is performed as; 1. Excitation and spectral parameters are extracted as

speech databases and are modeled as a multi-stream. Spectral parameters include Mel

cepstral coefﬁcients and their dynamic features. Excitation parameters include logF0 and

its linguistic features. F0 sequences have voiced region and unvoiced region. The voiced

region has continuous values while the unvoiced region has discrete values. Both of these

distributions are stored in a variable.

\2. Standard HMM has a transition model that decreases exponentially as time increases

while HMM-based speech synthesis utilizes Hidden Semi Markov Model(HSMM) which

uses gaussian distribution.

4.8.2 HMM Synthesis Part

Synthesis is done by [4.2](#br34)

λ = argmaxλ [p(O|W,λ)]

(4.2)

where W is a set of word sequences, λ is the maximize output probability, o speech

waveform.

First, a series of words are converted to context dependant sequences. Based on the labels,

an utterance is constructed by combining context dependant HMMs. Secondly, excitation

and spectral parameters are generated for these utterances. Finally, a speech synthesis

ﬁlter is applied to synthesis speech waves.

25









Bibliography

[1] Farah Adeeba, Tania Habib, Sarmad Hussain, Kh Shahzada Shahid, et al. Compari-

son of urdu text to speech synthesis using unit selection and hmm based techniques.

In 2016 Conference of The Oriental Chapter of International Committee for Co-

ordination and Standardization of Speech Databases and Assessment Techniques

(O-COCOSDA), pages 79–83. IEEE, 2016.

[2] Abbas Raza Ali and Maliha Ijaz. Urdu text classiﬁcation. In Proceedings of the 7th

international conference on frontiers of information technology, pages 1–7, 2009.

[3] Sin-Horng Chen, Shaw-Hwa Hwang, and Yih-Ru Wang. An rnn-based prosodic

information synthesizer for mandarin text-to-speech. IEEE transactions on speech

and audio processing, 6(3):226–239, 1998.

[4] Jeff Donahue, Sander Dieleman, Mikołaj Bin´kowski, Erich Elsen, and Karen Si-

monyan. End-to-end adversarial text-to-speech. arXiv preprint arXiv:2006.03575,

\2020.

[5] A Femina Jalin and J Jayakumari. Text to speech synthesis system for tamil using

hmm. In 2017 IEEE International Conference on Circuits and Systems (ICCS),

pages 447–451. IEEE, 2017.

[6] Pijus Kasparaitis. Diphone databases for lithuanian text-to-speech synthesis. Infor-

matica, 16(2):193–202, 2005.

[7] Haris Ali Khan, Muhammad Junaid Ali, and Umm E Hanni. Poster: A novel ap-

proach for pos tagging of pashto language. In 2020 First International Conference of

27





BIBLIOGRAPHY

Smart Systems and Emerging Technologies (SMARTTECH), pages 259–260. IEEE,

\2020.

[8] Jaehyeon Kim, Sungwon Kim, Jungil Kong, and Sungroh Yoon. Glow-tts: A gen-

erative ﬂow for text-to-speech via monotonic alignment search. arXiv preprint

arXiv:2005.11129, 2020.

[9] Sneha Lukose and Savitha S Upadhya. Text to speech synthesizer-formant synthesis.

In 2017 International Conference on Nascent Technologies in Engineering (ICNTE),

pages 1–4. IEEE, 2017.

[10] Tom Le Paine, Pooya Khorrami, Shiyu Chang, Yang Zhang, Prajit Ramachandran,

Mark A Hasegawa-Johnson, and Thomas S Huang. Fast wavenet generation algo-

rithm. arXiv preprint arXiv:1611.09482, 2016.

[11] S Parthasarathy and Cecil H Coker. On automatic estimation of articulatory param-

eters in a text-to-speech system. Computer Speech & Language, 6(1):37–75, 1992.

[12] Ihsan Rabbi, Mohammad Abid Khan, and Rahman Ali. Rule-based part of speech

tagging for pashto language. In Conference on Language and Technology, Lahore,

Pakistan, 2009.

[13] Yi Ren, Yangjun Ruan, Xu Tan, Tao Qin, Sheng Zhao, Zhou Zhao, and Tie-Yan

Liu. Fastspeech: Fast, robust and controllable text to speech. arXiv preprint

arXiv:1905.09263, 2019.

[14] Abdul Rahman Saﬁ. Wolwala: Deep pashto text-to-speech. 2019.

[15] H Sarmad. Letter-to-sound conversion for urdu text-to-speech system. In Workshop

on Computational Approaches to Arabic Script, pages 74–79, 2004.

[16] Youcef Tabet and Mohamed Boughazi. Speech synthesis techniques. a survey.

In International Workshop on Systems, Signal Processing and their Applications,

WOSSPA, pages 67–70. IEEE, 2011.

28





BIBLIOGRAPHY

[17] Keiichi Tokuda, Heiga Zen, and Alan W Black. An hmm-based speech synthesis

system applied to english. In IEEE speech synthesis workshop, pages 227–230.

IEEE, 2002.

[18] Yuxuan Wang, RJ Skerry-Ryan, Daisy Stanton, Yonghui Wu, Ron J Weiss, Navdeep

Jaitly, Zongheng Yang, Ying Xiao, Zhifeng Chen, Samy Bengio, et al. Tacotron:

Towards end-to-end speech synthesis. arXiv preprint arXiv:1703.10135, 2017.

[19] Yuxuan Wang, RJ Skerry-Ryan, Daisy Stanton, Yonghui Wu, Ron J Weiss, Navdeep

Jaitly, Zongheng Yang, Ying Xiao, Zhifeng Chen, Samy Bengio, et al. Tacotron:

Towards end-to-end speech synthesis. arXiv preprint arXiv:1703.10135, 2017.

[20] Haitong Zhang, Haoyue Zhan, Yang Zhang, Xinyuan Yu, and Yue Lin. Revisiting

ipa-based cross-lingual text-to-speech. arXiv preprint arXiv:2110.07187, 2021.

29

