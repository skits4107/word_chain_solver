import json
from collections import defaultdict, deque
import os
import sys
from colorama import Fore

def build_word_ladder_neighbors(words):
    word_neighbors = defaultdict(list)
    alphabet = set('abcdefghijklmnopqrstuvwxyz')

    for word in words:
         # loop through each character in the word and change one letter 
         # going through all possible mutations and only add mutations that are words
         # all mutations are inherently valid neighbors
         for i in range(len(word)):
            for char in alphabet:
                new_word = word[:i] + char + word[i+1:] # mutate the word
                if new_word in words and new_word != word:
                    word_neighbors[word].append(new_word)

    return word_neighbors

def get_ladder(predecessors, word):
    # builds path backwords by adding the predeccesar of each word until there isnt any
    path = [word]
    while predecessors[word] != None:
        word = predecessors[word]
        path.append(word)
    path.reverse()
    return path

def bfs_word_ladder_sovler(word_neighbors, starting_word, final_word):

    # used to sotre next words to check
    queue = deque([starting_word]) 

    #will be used to generate the path or chain of words by keeping track of what words came before each other
    predecessors = { starting_word: None }

    #while there are still words to visit
    while queue:

        #get the word to visit from queue and check if it is the final word
        current_word = queue.popleft()
        if current_word == final_word:
            path = get_ladder(predecessors, current_word)
            return path
        
        #get the neighbors or words that are valid chains of the current word
        neighbors = word_neighbors[current_word]

        for neighbor in neighbors:
            if neighbor not in predecessors:
                #if we havent checked this word add it to queue to be checked and set its predeccessor
                predecessors[neighbor] = current_word
                queue.append(neighbor)

    #if no path or chain is found
    return None

def get_word(words, prompt):
    #keeps asking for a word until word is a valid word
    while True:
        word = input(prompt)
        if word not in words:
            print("invalid word")
            continue
        return word
    
def get_user_words(words):
    #keeps asking for set of words unitl the words are valid
    while True:
        starting_word = get_word(words, f"{Fore.WHITE}enter {Fore.GREEN}starting {Fore.WHITE}word: ")
        ending_word = get_word(words, f"{Fore.WHITE}enter {Fore.RED}final {Fore.WHITE}word: ")

        if starting_word == ending_word:
            print(f"{Fore.RED}words cant be the same{Fore.WHITE}")
            continue
        if len(starting_word) != len(ending_word):
            print(f"{Fore.RED}words have to be same length{Fore.WHITE}")
            continue
        return starting_word, ending_word

def display_max_connected_word(word_neighbors):
    most_connections_word = ""
    most_connections_count = 0
    for word in word_neighbors.keys():
        length = len(word_neighbors[word])
        if length > most_connections_count:
            most_connections_count = length
            most_connections_word = word
    print(f"the word with the most connections is '{most_connections_word}' with {most_connections_count} connections")
    print(f"connections: {word_neighbors[most_connections_word]}")

def main():

    with open("words.txt", "r") as file:
        file_content = file.read()

    words = set(file_content.strip().split("\n"))

    # used for storing what words are valid neighbors in the chain
    word_neighbors = {}

    regen_cache = False
    if len(sys.argv) == 2 and sys.argv[1] == "-r":
        regen_cache = True

    #check for cache
    if os.path.exists("word_neighbors_cache.json") and not regen_cache:
        with open("word_neighbors_cache.json", "r") as file:
            word_neighbors = json.load(file)
    else:
        word_neighbors = build_word_ladder_neighbors(words)

        #cache generated adjacency list
        with open("word_neighbors_cache.json", "w") as file:
            json.dump(word_neighbors, file)


    print('\n')# add white space
    start_word, end_word = get_user_words(words)

    # try get and print path
    path = bfs_word_ladder_sovler(word_neighbors, start_word, end_word)

    if path:
        #color the first and last word
        path[0] = Fore.GREEN + path[0] + Fore.WHITE
        path[-1] = Fore.RED + path[-1] + Fore.WHITE

        print(f"{Fore.WHITE}the shortest word chain is: " + " -> ".join(path))
    else:
        print(f"{Fore.RED}no path found{Fore.WHITE}")

    should_display_stats = input("do you want to see stats: ")
    if should_display_stats == 'y' or should_display_stats == "yes":
        print("\n", end="")
        display_max_connected_word(word_neighbors)


    print('\n') # add white space

if __name__ == "__main__":
    main()

