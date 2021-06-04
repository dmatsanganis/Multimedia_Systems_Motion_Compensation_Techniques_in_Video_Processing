import numpy as np
from cv2 import cv2 
import random   
import huffman
import collections

def zigzag(input):
    horizontal = 0
    vertical = 0
    vertical_max = input.shape[0] 
    horizontal_max = input.shape[1]
    i = 0
    output = np.zeros((vertical_max * horizontal_max)) 

    while ((vertical < vertical_max) and (horizontal < horizontal_max)): 
        if ((horizontal + vertical) % 2) == 0: 
            if (vertical == 0): 
                output[i] = input[vertical, horizontal]       
                if (horizontal == horizontal_max): 
                    vertical = vertical + 1 
                else:
                    horizontal = horizontal + 1                       
                i = i + 1 

            elif ((horizontal == horizontal_max - 1) and (vertical < vertical_max)):   
            	output[i] = input[vertical, horizontal] 
            	vertical = vertical + 1 
            	i = i + 1

            elif ((vertical > 0) and (horizontal < horizontal_max - 1)):    
            	output[i] = input[vertical, horizontal] 
            	vertical = vertical - 1 
            	horizontal = horizontal + 1
            	i = i + 1

        else:                                    
        	if ((vertical == vertical_max - 1) and (horizontal <= horizontal_max - 1)): 
        		output[i] = input[vertical, horizontal] 
        		horizontal = horizontal + 1 
        		i = i + 1 
        
        	elif (horizontal == 0):                 
        		output[i] = input[vertical, horizontal] 
        		if (vertical == vertical_max - 1):  
        			horizontal = horizontal + 1 
        		else:
        			vertical = vertical + 1 
        		i = i + 1

        	elif ((vertical < vertical_max - 1) and (horizontal > 0)):
        		output[i] = input[vertical, horizontal] 
        		vertical = vertical + 1 
        		horizontal = horizontal - 1
        		i = i + 1

        if ((vertical == vertical_max - 1) and (horizontal == horizontal_max - 1)): 
        	output[i] = input[vertical, horizontal] 
        	break
    return output

def huffman_encoding(macroblock,output): 
    zigzaged = zigzag(macroblock) 
    codes = huffman.codebook(collections.Counter(zigzaged).items()) 
    for i in zigzaged:
        output.append(codes.get(i)) 

A = []
count = 0
while count <= 3:
    if count == 0:
        print("\nGive ID of students in a team (min:1 and max:3 students per team)")
        count += 1
    if count == 1:
        student1 = input("\nID of first student: ")
        if len(student1) != 5 and not student1.isnumeric():
            print("ID must contain 5 digits")
            continue
        else:
            selection = input("\nDo you want to stop? (y/n): ").lower()
            if selection in ["y", "n"]:
                A.append(student1) 
                if(selection == 'y'):
                    break
            else:
                print("\nInvalid input.")
                continue
            count += 1
    if count == 2:
        student2 = input("\nID of second student: ")
        if len(student2) != 5 and not student2.isnumeric():
            print("ID must contain 5 digits")
            continue
        else:
            selection = input("\nDo you want to stop? (y/n): ").lower()
            if selection in ["y", "n"]:
                A.append(student2) 
                if(selection == 'y'):
                    break
            else:
                print("\nInvalid input.")
                continue
            count += 1
    if count == 3:
        student3 = input("\nID of third student: ")   
        if len(student3) != 5 and not student2.isnumeric():
            print("ID must contain 5 digits")
            continue
        else:
            A.append(student3) 
            count += 1           
print("\nStudents' ID for this group: " + str(A))

for i in range(len(A)):
    change_index = random.randint(0,4) 
    A[i] = A[i][:change_index] + "5" + A[i][change_index+1:] 
print("\nStudents' ID for this group after the change of one digit with the number 5: " + str(A))

logos_simpiesis = [] 
for f in range(100):
    imageA = np.zeros([104, 200]) 
    for i in range(104): 
        for j in range(40): 
            rnd = random.randint(0,len(A)-1) 
            for a in range(5):
                imageA[i, j*5 + a] = A[rnd][a] 

    imageB = np.zeros([104, 200], dtype=np.float32) 
    
    quantization_table = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]]) 

    imageA_after_huffman = [] 
    for i in range(0,104,8): 
        for j in range(0,200,8): 
            huffman_encoding(imageA[i:(i+8),j:(j+8)],imageA_after_huffman) 

    imageB_after_huffman = [] 
    for i in range(0,104,8): 
        for j in range(0,200,8): 
            imageB[i:(i+8),j:(j+8)] = cv2.dct(imageA[i:(i+8),j:(j+8)]) 
            imageB[i:(i+8),j:(j+8)] = np.ceil(np.divide(imageB[i:(i+8),j:(j+8)], quantization_table)) 
            #imageC[i:(i+8),j:(j+8)] = np.multiply(quantization_table, imageB[i:(i+8),j:(j+8)]) 
            #imageC[i:(i+8),j:(j+8)] = np.round(cv2.idct(imageC[i:(i+8),j:(j+8)])) 
            huffman_encoding(imageB[i:(i+8),j:(j+8)],imageB_after_huffman)

    imageA_bits = len(''.join(imageA_after_huffman)) 
    imageB_bits = len(''.join(imageB_after_huffman)) 
    logos_simpiesis.append(imageA_bits/imageB_bits) 

print("\nAverage compression ratio: " + str(sum(logos_simpiesis)/len(logos_simpiesis)))
input("\nPress any button to exit the program...")