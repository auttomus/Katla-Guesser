with open('wordlist.txt', 'r') as file:
    words = file.read() 

char_list = 'abcdefghijklmnopqrstuvwxyz' 

for i in char_list:
    count = words.count(i)
    print(f'Jumlah huruf {i}: {count}')
