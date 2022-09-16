import os
import csv

input_file="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\training_140_sentiment.csv"
output_file_label1="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\positive\\sentiment_positive1.txt"
output_file_label2="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\positive\\sentiment_positive2.txt"
output_file_label3="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\negetive\\sentiment_negetive1.txt"
output_file_label4="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\negetive\\sentiment_negetive2.txt"

def split_file_into_labels():
    count_neg=1
    count_pos=1
    with open(input_file,"r") as inpf,open(output_file_label1,"w") as outl1,open(output_file_label2,"w") as outl2,open(output_file_label3,"w") as outl3,open(output_file_label4,"w") as outl4:
        csv_reader=csv.reader(inpf,delimiter=',',quotechar='"')
        for line in csv_reader:
            if line[0]=='0':
                if count_neg<=400000:
                    outl3.write(line[5]+'\n')
                else:
                    outl4.write(line[5] + '\n')
                count_neg+=1
            else:
                if count_pos <= 400000:
                    outl1.write(line[5] + '\n')
                else:
                    outl2.write(line[5] + '\n')
                count_pos+=1


if __name__=="__main__":
    split_file_into_labels()
