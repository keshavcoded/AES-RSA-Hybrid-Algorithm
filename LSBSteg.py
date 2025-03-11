import cv2
import numpy as np

def data2binary(data):
    if type(data) == str:
        return ''.join([format(ord(i),"08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i,"08b") for i in data]


def hideData(image,secret_data1,secret_data2,secret_data3):
    secret_data1 += "#####"
    secret_data2 += "#####"
    secret_data3 += "#####"     

    data_index = 0
    binary_data1 = data2binary(secret_data1)
    binary_data2 = data2binary(secret_data2)
    binary_data3 = data2binary(secret_data3)
    data_length1 = len(binary_data1)
    data_length2 = len(binary_data2)
    data_length3 = len(binary_data3)
    
    for values in image:
        for pixel in values:
            
            r,g,b = data2binary(pixel)

            if data_index < data_length1:
                pixel[0] = int(r[:-1] + binary_data1[data_index])
                data_index += 1
            if data_index < data_length1:
                pixel[1] = int(g[:-1] + binary_data1[data_index])
                data_index += 1
            if data_index < data_length1:
                pixel[2] = int(b[:-1] + binary_data1[data_index])
                data_index += 1
            if data_index < data_length2:
                pixel[0] = int(r[:-2] + binary_data2[data_index])
                data_index += 1
            if data_index < data_length2:
                pixel[1] = int(g[:-2] + binary_data2[data_index])
                data_index += 1
            if data_index < data_length2:
                pixel[2] = int(b[:-2] + binary_data2[data_index])
                data_index += 1
            if data_index < data_length3:
                pixel[0] = int(r[:-3] + binary_data3[data_index])
                data_index += 1
            if data_index < data_length3:
                pixel[1] = int(g[:-3] + binary_data3[data_index])
                data_index += 1
            if data_index < data_length3:
                pixel[2] = int(b[:-3] + binary_data3[data_index])
                data_index += 1
            if data_index >= (data_length1+data_length2+data_length3):
                break

    return image
            
    
def encode_text():
    image_name = input("Enter Cover Image Name : ")
    image = cv2.imread(image_name)

    data1 = input("Enter The Text1 : ")
    data2 = input("Enter The Text2 : ")
    data3 = input("Enter The Text3 :")
    if data1 == 0:
        raise ValueError("Data is Empty ... ")
    elif data2 == 0:
        raise ValueError("Data is Empty ... ")
    elif data3 == 0:
        raise ValueError("Data is Empty ... ")


    file_name = input("Enter The Encoded Image Name : ")

    encoded_data = hideData(image,data1,data2,data3)
    cv2.imwrite(file_name,encoded_data)
    print(" ")
    print("Successfully Encoded into image:",file_name)
    print(" ")

def show_data(image):
    binary_data1 = ""
    binary_data2 = ""
    binary_data3 = ""
    for values in image:
        for pixel in values:
            r,g,b = data2binary(pixel)
            
            binary_data1 += r[-1]
            binary_data1 += g[-1]
            binary_data1 += b[-1]
            binary_data2 += r[-2]
            binary_data2 += g[-2]
            binary_data2 += b[-2]
            binary_data3 += r[-3]
            binary_data3 += g[-3]
            binary_data3 += b[-3]


    all_bytes1 = [binary_data1[i: i+8] for i in range (0,len(binary_data1),8)]
    all_bytes2 = [binary_data2[i: i+8] for i in range (0,len(binary_data2),8)]
    all_bytes3 = [binary_data3[i: i+8] for i in range (0,len(binary_data3),8)]

    decoded_data1 = ""
    decoded_data2 = ""
    decoded_data3 = ""
    for byte in all_bytes1:
        decoded_data1 += chr(int(byte,2))
        if decoded_data1[-5:] == "#####":
            break
    for byte in all_bytes2:
        decoded_data2 += chr(int(byte,2))
        if decoded_data2[-5:] == "#####":
            break
    for byte in all_bytes3:
        decoded_data3 += chr(int(byte,2))
        if decoded_data3[-5:] == "#####":
            break

    return (decoded_data1[:-5],decoded_data2[:-5],decoded_data3[:-5])



def decode_text():
    image_name = input("Enter Image You Want To Extract : ")
    image = cv2.imread(image_name)

    text1,text2,text3=show_data(image)   
    return (text1,text2,text3)



def stegnography():
    print(" ")
    print("!STEGNOGRAPHY LSB SYSTEM!")
    userinput = int(input("\n 1. Encode data into image \n 2. Decode data from a image \n\n Enter your choice : "))
    if userinput == 1:
        encode_text()
    else:
        final_data1,final_data2,final_data3=decode_text()
        print("\nDecoded Data : ",final_data1,final_data2,final_data3)

#stegnography()







if __name__ == "__main__":
    main()



