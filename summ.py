import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


def summarize(result):
#Getting data
    extra_words=list(STOP_WORDS)+list(punctuation)+['\n']
    nlp=spacy.load('en_core_web_sm')

    # doc = "As the market for personal computers expanded and evolved through the 1990s, Apple lost market share to the lower-priced duopoly of Microsoft Windows on Intel PC clones. The board recruited CEO Gil Amelio to what would be a 500-day charge for him to rehabilitate the financially troubled company—reshaping it with layoffs, executive restructuring, and product focus. In 1997, he led Apple to buy NeXT, solving the desperately failed operating system strategy and bringing Jobs back. Jobs regained leadership status, becoming CEO in 2000. Apple swiftly returned to profitability under the revitalizing Think different campaign, as he rebuilt Apple's status by launching the iMac in 1998, opening the retail chain of Apple Stores in 2001, and acquiring numerous companies to broaden the software portfolio. In January 2007, Jobs renamed the company Apple Inc., reflecting its shifted focus toward consumer electronics, and launched the iPhone to great critical acclaim and financial success. In August 2011, Jobs resigned as CEO due to health complications, and Tim Cook became the new CEO. Two months later, Jobs died, marking the end of an era for the company. In June 2019, Jony Ive, Apple's CDO, left the company to start his own firm, but stated he would work with Apple as its primary client."
    doc = result
    docx = nlp(doc)

    #All the extra words are removed and the count of each other word is entered into the dictionary.
    all_words=[word.text for word in docx]
    Freq_word={}
    for w in all_words:
        w1=w.lower()
        if w1 not in extra_words and w1.isalpha():
            if w1 in Freq_word.keys():
                Freq_word[w1]+=1
            else:
                Freq_word[w1]=1

    #titles of the content  generation
    val=sorted(Freq_word.values())
    max_freq=val[-3:]
    # # print("Topic of document given :-")
    # for word,freq in Freq_word.items():
    #     if freq in max_freq:
    #          # print(word ,end=" ")
    #     else:
    #         continue

    #TF-IDF It is used to represent how important a given word is to a document on a complete collection relatively
    for word in Freq_word.keys():
           Freq_word[word] = (Freq_word[word]/max_freq[-1])

    #The sentence with the most important words will have much more importance
    sent_strength={}
    for sent in docx.sents:
          for word in sent :
                if word.text.lower() in Freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent]+=Freq_word[word.text.lower()]
                    else:
                        sent_strength[sent]=Freq_word[word.text.lower()]
                else:
                    continue

    #Getting Important Sentences
    top_sentences=(sorted(sent_strength.values())[::-1])
    top30percent_sentence=int(0.3*len(top_sentences))
    top_sent=top_sentences[:top30percent_sentence]


    #Getting the final summary
    summary=[]
    for sent,strength in sent_strength.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue


    summ = ''
    for i in summary:
        summ = summ + ' ' + str(i)
    return summ

# doc = "As the market for personal computers expanded and evolved through the 1990s, Apple lost market share to the lower-priced duopoly of Microsoft Windows on Intel PC clones. The board recruited CEO Gil Amelio to what would be a 500-day charge for him to rehabilitate the financially troubled company—reshaping it with layoffs, executive restructuring, and product focus. In 1997, he led Apple to buy NeXT, solving the desperately failed operating system strategy and bringing Jobs back. Jobs regained leadership status, becoming CEO in 2000. Apple swiftly returned to profitability under the revitalizing Think different campaign, as he rebuilt Apple's status by launching the iMac in 1998, opening the retail chain of Apple Stores in 2001, and acquiring numerous companies to broaden the software portfolio. In January 2007, Jobs renamed the company Apple Inc., reflecting its shifted focus toward consumer electronics, and launched the iPhone to great critical acclaim and financial success. In August 2011, Jobs resigned as CEO due to health complications, and Tim Cook became the new CEO. Two months later, Jobs died, marking the end of an era for the company. In June 2019, Jony Ive, Apple's CDO, left the company to start his own firm, but stated he would work with Apple as its primary client."
# outt=summarize(doc)
# print(outt)