import huffman
import random
import collections
import numpy
from cv2 import cv2   


quant_array = numpy.array([[16, 11, 10, 16, 24, 40, 51, 61],
                            [12, 12, 14, 19, 26, 58, 60, 55],
                            [14, 13, 16, 24, 40, 57, 69, 56],
                            [14, 17, 22, 29, 51, 87, 80, 62],
                            [18, 22, 37, 56, 68, 109, 103, 77],
                            [24, 35, 55, 64, 81, 104, 113, 92],
                            [49, 64, 78, 87, 103, 121, 120, 101],
                            [72, 92, 95, 98, 112, 100, 103, 99]])






def zigzag(block):
    i = 0
    j = 0
    k = 0
    out = numpy.zeros(64)

    while ((i < 8) and (j < 8)): 
        if ((i + j) % 2) == 0: 
            if (i == 0): 
                out[k] = block[i, j]       
                if (j == 8): 
                    i += 1
                else:
                    j += 1                       
                k += 1

            elif ((j == 7) and (i < 8)):   
            	out[k] = block[i, j] 
            	i += 1
            	k += 1

            elif ((i > 0) and (j < 7)):    
            	out[k] = block[i, j] 
            	i -= 1 
            	j += 1
            	k += 1

        else:                                    
        	if ((i == 7) and (j <= 7)): 
        		out[k] = block[i, j] 
        		j += 1 
        		k += 1
        
        	elif (j == 0):                 
        		out[k] = block[i, j] 
        		if (i == 7):  
        			j += 1 
        		else:
        			i += 1 
        		k += 1

        	elif ((i < 7) and (j > 0)):
        		out[k] = block[i, j] 
        		i += 1 
        		j -= 1
        		k += 1

        if ((i == 7) and (j == 7)): 
        	out[k] = block[i, j] 
        	break
    return out

def huffman_encoding(macroblock,out): 
    zigzaged = zigzag(macroblock) 
    codes = huffman.codebook(collections.Counter(zigzaged).items()) 
    for i in zigzaged:
        out.append(codes.get(i)) 

print("Please input the team number IDs in the format id_1 id_2 id_3.\n")

idz = input()
id_list = []
while(True):
    id_list = idz.split()
    if(len(id_list)> 3 or len(id_list)==0 ):
        print("Please input correct IDs sequence\n")
        idz = input()
        continue
    for i in range(len(id_list)):
        if(not id_list[i].isdigit() or not (len(id_list[i]))):
            print("Please input correct IDs sequence\n")
            idz = input()
            continue
    break

print("Number IDs are: " + str(id_list))


#randomly change a digit of each ID with 5
for i in range(len(id_list)):
    j = random.randint(0,4)
    id_list[i] = id_list[i][:j] + "5" + id_list[i][j+1:]
print(id_list)

comp_ratios = [] 
for iteration in range(100): #main loop
    imgA = numpy.zeros([104, 200]) 
    for i in range(104): 
        for j in range(40): 
            idd = random.randint(0,len(id_list)-1) 
            for d in range(5):
                imgA[i, j*5 + d] = id_list[idd][d] 

    imgB = numpy.zeros([104, 200], dtype=numpy.float32) 
    


    huffA = [] 
    for i in range(0,104,8): 
        for j in range(0,200,8): 
            huffman_encoding(imgA[i:(i+8),j:(j+8)],huffA) 

    huffB = [] 
    for i in range(0,104,8): 
        for j in range(0,200,8): 
            imgB[i:(i+8),j:(j+8)] = cv2.dct(imgA[i:(i+8),j:(j+8)]) 
            imgB[i:(i+8),j:(j+8)] = numpy.ceil(numpy.divide(imgB[i:(i+8),j:(j+8)], quant_array))
            huffman_encoding(imgB[i:(i+8),j:(j+8)],huffB)

    imgA_size = len(''.join(huffA))
    imgB_size = len(''.join(huffB))
    comp_ratios.append(imgA_size/imgB_size) 

final_ratio = sum(comp_ratios)/len(comp_ratios)
print("Avg compression ratio: " + str(final_ratio))