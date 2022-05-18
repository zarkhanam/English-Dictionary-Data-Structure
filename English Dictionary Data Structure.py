import tkinter as tk
from tkinter import ttk


class Node:
    def __init__(self, data=None):
        self.data = data
        self.children = [None] * 26  # Every node has list of 26 children
        self.is_eow = False  # eow = end of word


class Dictionary:
    _alphabets = [chr(num) for num in range(97, 123)]

    def __init__(self):
        self.root = Node()
        self._word = ''

    @staticmethod
    def get_index(alphabet):
        """This method takes an alphabet and returns its index
        :param alphabet
        :return int
        """
        return Dictionary._alphabets.index(alphabet)

    def store_alphabet(self, char, parent, mark=False):
        """ This method stores an alphabet and marks it as end of word if it is end
        :param char:
        :param parent:
        :param mark:
        :return: newly created node or previously stored node
        """
        char = char.lower()
        index = self.get_index(char)
        if node := parent.children[index]:
            # Check if the character already exits
            if mark:
                node.is_eow = mark
            return node
        else:
            new_node = Node(char)
            new_node.is_eow = mark
            parent.children[index] = new_node
            return new_node

    def store_word(self, word: str, parent):
        """ This recursive method stores a word, alphabet by alphabet
        :param word: string of alphabets
        :param parent: Node
        :return: None
        """
        if word.isalpha() and len(word) != 0:
            if len(word) == 1:
                parent = self.store_alphabet(word[0], parent, True)
            else:
                parent = self.store_alphabet(word[0], parent)
            word = word[1:]
            self.store_word(word, parent)

    def search(self, word: str):
        """ This method linearly searches a word from the dictionary
        :param word:
        :return: if found the word) returns existing Node of last alphabet of the word otherwise returns False
        """
        if word:
            parent = self.root
            for alphabet in word:
                index = self.get_index(alphabet)
                if not (new_parent := parent.children[index]):  # If the sequence of alphabets gets disturbed
                    return False
                parent = new_parent
            return parent
        return False

    def give_suggestions(self, last_node, suggestion='', suggestions=list()):
        """
        This recursive method takes last alphabet of the input word and checks for all the possible words next to that
         alphabet
        :param last_node: Node of last alphabet of input
        :param suggestion: string of one complete sequence of alphabets
        :param suggestions: list of all the suggested words
        :return: suggestions
        """
        if last_node:
            for node in last_node.children:
                if node:
                    suggestion += node.data
                    if node.is_eow:
                        suggestions.append(suggestion)
                    self.give_suggestions(node, suggestion, suggestions)
                    suggestion = suggestion[:-1]
            return suggestions

    def suggest(self, word: str) -> list:
        """ This method modifies the list of suggested possible sequence of alphabets by combining it to given word
        :param word: sequence of alphabets
        :return: modified list of suggested words
        """
        if word.isalpha():
            word = word.lower()
            if last_node := self.search(word):
                suggestions = self.give_suggestions(last_node)
                suggestions.sort(key=len)
                return [word + suggestion for suggestion in suggestions]

    def handle_word(self, key):
        if len(key) == 1 and key.isalpha():
            self._word += key
        elif key == 'BackSpace':
            self._word = self._word[:-1]
        print(self._word)
        return self._word

    def get_word(self):
        return self._word


my_dict = Dictionary()
my_dict.store_word('abc', my_dict.root)
my_dict.store_word('the', my_dict.root)
my_dict.store_word('thIS', my_dict.root)
my_dict.store_word('then', my_dict.root)
my_dict.store_word('that', my_dict.root)
my_dict.store_word('there', my_dict.root)
my_dict.store_word('than', my_dict.root)
my_dict.store_word('thief', my_dict.root)
my_dict.store_word('their', my_dict.root)
typed = 'tha'
print('Typed: ', typed, '\nSuggestions: ', my_dict.suggest(typed))


# --------------------- GUI ------------------------
def key_handler(event=None):
    if event:
        my_dict.handle_word(event.keysym)


def change_month():
    comboExample["values"] = []
    comboExample["values"] = my_dict.suggest(my_dict.get_word())


r = tk.Tk()
r.title('Dictionary')
t = tk.Entry(r)
r.geometry('400x300')
label_one = tk.Label(r, text="Enter Word")
label_two = tk.Label(r, text="Predictions")

comboExample = ttk.Combobox(r,
                            values=[
                                "January",
                                "February",
                                "March",
                                "April"],
                            postcommand=change_month)

label_one.grid(row=0, column=0)
t.grid(row=0, column=1)
comboExample.grid(row=1, column=1)
label_two.grid(row=1, column=0)

r.bind('<Key>', key_handler)

r.mainloop()
