import os
import csv

input_file="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\training_140_sentiment.csv"
pos_file_path="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\pos"
neg_file_path="E:\\python_projects\\Springboard\\datasets\\twitter_sentiment140\\neg"

def split_line_file():
        neg_counter=0
        pos_counter = 0
        with open(input_file,"r") as inpf:
            csv_reader=csv.reader(inpf,delimiter=',',quotechar='"')

            for line in csv_reader:
                    if line[0]=='0' and neg_counter<100000:
                        neg_file=os.path.join(neg_file_path,'neg_text_'+str(neg_counter)+'.txt')
                        with open(neg_file,'w') as negf:
                            negf.write(line[5] + '\n')
                        neg_counter+=1
                    elif line[0]!='0' and pos_counter<100000:
                        pos_file = os.path.join(pos_file_path, 'pos_text_' + str(pos_counter) + '.txt')
                        print(pos_file)
                        with open(pos_file,'w') as posf:
                            posf.write(line[5] + '\n')
                        pos_counter+=1

if __name__=="__main__":
    split_line_file()