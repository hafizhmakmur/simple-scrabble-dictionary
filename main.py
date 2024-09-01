#!/usr/bin/python3

import os.path
import wget
from tqdm import tqdm

def generate_all():
    all_with_meaning_list = []

    if not os.path.isfile("all-with-meaning.txt"):
        if not os.path.isfile("count_1w.txt"):
            print("Downloading Peter Norvig's NGram count")
            wget.download("https://norvig.com/ngrams/count_1w.txt")

        if not os.path.isfile("/opt/NASPA Zyzzyva 3.4.1/data/words/North-American/NWL2023.txt"):
            print ("Please install Zyzzyva from http://www2.scrabbleplayers.org/w/NASPA_Zyzzyva_Download")
            print("Reading NGram File")

        ngram_words = []
        ngram_dict = {}
        duplicates = 0

        print("Reading count_1w.txt")
        with open("count_1w.txt", 'r') as ngram_file:
            for ngram_line in tqdm(ngram_file.readlines()):
                ngram_word = ngram_line.split("\t")[0].upper()
                ngram_words.append(ngram_word)
                if ngram_word not in ngram_dict:
                    ngram_dict[ngram_line.split("\t")[0]] = ""
                else:
                    duplicates += 1
                    print(ngram_word, "is read again")

            if duplicates > 0:
                print("There are", duplicates, "duplicates")
            print("Words read:", len(ngram_words))
            # print(ngram_words[0])
            # print(ngram_words[1])
        
        print("Reading NWL 2023 List")
        nwl_dict = {}

        with open("/opt/NASPA Zyzzyva 3.4.1/data/words/North-American/NWL2023.txt", 'r') as nwl_file:
            for nwl_line in tqdm(nwl_file.readlines()):
                nwl_word = nwl_line.split(" ")[0].upper()
                nwl_meaning = nwl_line.split(" ")[1:]
                nwl_dict[nwl_word] = nwl_meaning
            print("Words read:", len(nwl_dict))
            # print(list(nswl_dict.items())[0])
            # print(list(nswl_dict.items())[1])

        print("Reading Collins 2021 List")
        collins_dict = {}       
        
        with open("/opt/NASPA Zyzzyva 3.4.1/data/words/British/CSW21.txt", 'r') as collins_file:
            for collins_line in tqdm(collins_file.readlines()):
                collins_word = collins_line.split("\n")[0].upper()
                collins_dict[collins_word] = ""
            print("Words read:", len(collins_dict))
            # print(list(collins_dict.items())[0])
            # print(list(collins_dict.items())[1])
        
        print("Filtering words not in Collins Dictionary")
        compatible_words = []
        incompatible_words = 0
        length_counts = {}
        for ngram_word in tqdm(ngram_words):
            if ngram_word not in collins_dict:
                incompatible_words += 1
                # print(ngram_word)
            else:
                compatible_words.append(ngram_word)
                if len(ngram_word) not in length_counts:
                    length_counts[len(ngram_word)] = 1
                else:
                    length_counts[len(ngram_word)] += 1
                # print(ngram_word)

        print("Statistics :")
        print("Compatible NGram Word in Collins Dictionary =", \
            len(compatible_words), "/", len(ngram_words), "=", \
            "{:.2%}".format(len(compatible_words) / len(ngram_words)))
        
        for length, count in sorted(list(length_counts.items())):
            print(length, "Letters:", count, "words")
        
        print ("Generate all.txt")
        with open("all.txt", 'w') as all_file:
            for compatible_word in tqdm(compatible_words):
                all_file.write(compatible_word + "\n")
        
        print ("Generate all-with-meaning.txt")
        no_meaning = 0
        with open("all-with-meaning.txt", 'w') as all_with_meaning_file:
            for compatible_word in tqdm(compatible_words):
                if compatible_word in nwl_dict:
                    all_with_meaning_file.write(compatible_word + " " + \
                                                " ".join(nwl_dict[compatible_word]))
                    all_with_meaning_list.append((compatible_word, " ".join(nwl_dict[compatible_word])))
                else:
                    no_meaning += 1
                    all_with_meaning_file.write(compatible_word + "\n")
                    all_with_meaning_list.append((compatible_word, " "))
        print (no_meaning)
    else:
        print("Reading all-with-meaning.txt")
        with open("all-with-meaning.txt", 'r') as all_with_meaning_file:
            for all_with_meaning_line in tqdm(all_with_meaning_file.readlines()):
                all_with_meaning_word = all_with_meaning_line.split(" ")[0].upper().strip()
                all_with_meaning = all_with_meaning_line.split(" ")[1:]
                all_with_meaning_list.append((all_with_meaning_word, \
                                              " ".join(all_with_meaning).strip()))
                    
    return all_with_meaning_list

all_with_meaning_list = []

def generate_top_list(n):
    
    global all_with_meaning_list

    if not all_with_meaning_list:
        all_with_meaning_list = generate_all()
    
    print("Generating", str(n)+".txt")
    with open(str(n)+".txt", 'w') as top_file:
        for word, meaning in tqdm(sorted(all_with_meaning_list[:n])):
            top_file.write(word + "\n")
    
    print("Generating", str(n)+"-sort-by-length.txt")
    with open(str(n)+"-sort-by-length.txt", 'w') as top_file:
        for word, meaning in tqdm(sorted(all_with_meaning_list[:n], \
                                         key=lambda tuple: (len(tuple[0]), tuple[0]))):
            top_file.write(word + "\n")  
    
    print("Generating", str(n)+"-with-meaning.txt")
    with open(str(n)+"-with-meaning.txt", 'w') as top_file:
        for word, meaning in tqdm(sorted(all_with_meaning_list[:n])):
            top_file.write((word + " " + meaning).strip() + "\n")
  

if __name__ == "__main__":

    if not all_with_meaning_list:
        all_with_meaning_list = generate_all()
    
    generate_top_list(10000)
    generate_top_list(20000)
    generate_top_list(50000)