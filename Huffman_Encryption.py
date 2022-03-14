'''
Huffman Encryption and Decryption
'''

'''
import packages
'''
from pandas import read_csv
from numpy.random import randint

'''
Class Huff contains methods to encrypt and decrypt strings using a huffman encryption method
'''
class Huff:
    '''
    the encrypt method uses randomization to convert a string to a binary
        form using the Huffman method
    @param string:str. This input is any string using valid keys from the
        keyboard
    @return str. The output is the encrypted version of the string input
        with the randomized index
    '''
    def encrypt(string:str):
        index = randint(0,999)
        string = list(string)
        idx = read_csv(f'/Users/Zach/Huffman Encryption/Index/{index}.csv')
        left = idx['left'].tolist()
        right = idx['right'].tolist()
        encryptedString = ""
        for position in string:
            for row in range(len(left)):
                if position in left[row]:
                    encryptedString = encryptedString + '0'
                elif position in right[row]:
                    encryptedString = encryptedString + '1'
        encryptedString = encryptedString + f':#{index}'
        return encryptedString
    '''
    the encryptFI method uses a set index to convert a string to a binary
        form using the Huffman method
    @param string:str. This input is any string using valid keys from the
        keyboard
    @param index:int. This input is an integer associated with a preset
        index
    @return str. The output is the encrypted version of the string input
        with the randomized index
    '''
    def encryptFI(string:str,index:int):
        string = list(string)
        idx = read_csv(f'/Users/Zach/Huffman Encryption/Index/{index}.csv')
        left = idx['left'].tolist()
        right = idx['right'].tolist()
        encryptedString = ""
        for position in string:
            for row in range(len(left)):
                if position in left[row]:
                    encryptedString = encryptedString + '0'
                elif position in right[row]:
                    encryptedString = encryptedString + '1'
        encryptedString = encryptedString + f':#{index}'
        return encryptedString

    '''
    the encryptList method accesses the encrypt method and applies it to
        each string in the given list
    @param list_name: list. This input is any size list made up of strings
    @return list. The output is a list of encrypted strings with their
        randomized indexes in the same order inputted in the initial list
    '''
    def encryptList(list_name:list):
        return [Huff.encrypt(str(i)) for i in list_name]

    '''
    the decrypt method uses the Huffman method to convert a string in
        Huffman binary form into a string
    @param string:str. This input is a pre-encrypted string in the string
        format that includes its designated index in the correct form
    @return str. The output is the decrypted version of the string input
        as per the specified index. if the format is incorrect, a decryption
        error will be returned
    '''
    def decrypt(string:str):
        if not(':' in string):
            return "Decryption Error: Incorrect Format"
        index,string = string[string.index(':')+2:], string[:string.index(':')]
        df = read_csv(f'/Users/Zach/Huffman Encryption/Index/{index}.csv')
        left, right, combine = df['left'].tolist(),df['right'].tolist(),df['combine'].tolist()
        decryptedString = ""
        current = combine[0]
        for value in list(string):
            if value == '0':
                if len(current) == 1:
                    decryptedString = decryptedString + current
                    current = combine[0]
                else:
                    current = left[combine.index(current)]
                if len(current) == 1:
                    decryptedString = decryptedString + current
                    current = combine[0]
            elif value == "1":
                if len(current) == 1:
                    decryptedString = decryptedString + current
                    current = combine[0]
                else:
                    current = right[combine.index(current)]
                if len(current) == 1:
                    decryptedString = decryptedString + current
                    current = combine[0]
        if current != combine[0]:
            decryptedString = decryptedString + current
        return decryptedString

    '''
    the decryptList method accesses the decrypt method and applies it to
        each string in the given list
    @param list_name: list. This input is any size list made up of strings
        in the required Huffman encryption format
    @return list. The output is a list of decrypted strings as per their
        specified indexes in the same order inputted in the initial list
    '''
    def decryptList(list_name:list):
        return [Huff.decrypt(i) for i in list_name]


'''
If this file is downloaded to device, call:

    from Huffman_Encryption import *
    
to access the defined Huff class.
'''
