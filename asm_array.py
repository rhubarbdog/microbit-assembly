from microbit import *
# r0 byte array
# r1 index
# r2 value
@micropython.asm_thumb
def asm_set(r0, r1, r2):
    mov(r3, 0x03)      # set r3 to bit mask for r4 = r1 % 4
    mov(r4, r1)
    and_(r4, r3)       # r4 is the byte number in the word
    lsl(r4, r4, 3)     # r4 *= 8 ,r4 is now a number of bits
    lsr(r1, r1, 2)     # r1 = r1 // 4
    lsl(r1, r1, 2)     # r1 *= 4
    add(r0, r0, r1)    # r0 now points to the word in memory in bytearray

    ldr(r1, [r0, 0])   # get the word store it in r1
    mov(r3, 0xff)      # create a bit mask of 1 byte in r3
    lsl(r3, r4)        # move it to correct byte (r4 bits left)
    bic(r1, r3)        # clear bits in r1 specified by r3
    mov(r5, 0xff)      # r5 is a value mask
    and_(r2, r5)       # limit the value at r2 to 1 byte
    lsl(r2, r4)        # move the value to the correct byte
    orr(r1, r2)        # put r2 into r1
    str(r1, [r0, 0])   # store r1 back in the bytearray

    mov(r0, r2)
    
# r0 byte array
# r1 index
@micropython.asm_thumb
def asm_get(r0, r1):
    mov(r3, 0x03)      # set r3 to bit mask for r4 = r1 % 4
    mov(r4, r1)
    and_(r4, r3)       # r4 is the byte number in the word
    lsl(r4, r4, 3)     # r4 *= 8 ,r4 is now a number of bits
    lsr(r1, r1, 2)     # r1 = r1 // 4
    lsl(r1, r1, 2)     # r1 *= 4
    add(r0, r0, r1)    # r0 now points to the word in memory in bytearray

    ldr(r1, [r0, 0])   # get the word store it in r1
    mov(r3, 0xff)      # create a 1 byte bit mask
    lsl(r3, r4)        # move r4 bits left to correct byte
    and_(r1, r3)       # r1 is now just the byte required but in situ
    lsr(r1, r4)        # move r1 right r4 bits

    mov(r0, r1)        # return the value
    
def print_array(array):
    for elem in array:
        print(elem, end = " ")
    print("")

data = bytearray(10)
for i in range(len(data)):
    data[i] = i + 1

print_array(data)

# data[4] = 15
asm_set(data, 4, 15)

print_array(data)

# v = data[9]
v = asm_get(data, 9)
print('data[9]',v)
