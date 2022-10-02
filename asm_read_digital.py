from microbit import *
# r0 - the number of bits to shift for given pin
@micropython.asm_thumb
def asm_read_digital(r0):

    mov(r1, 0x50)       # r1=0x50
    lsl(r1, r1, 16)     # r1=0x500000
    add(r1, 0x05)       # r1=0x500005
    lsl(r1, r1, 8)      
    add(r1, 0x10)       # r1=0x50000510 -- this points to GPIO read digital
                        # registers 
    ldr(r2, [r1, 0])    # move memory@r1 to r2
    
    mov(r3, 0x01)       # make a bit mask in r3
    lsl(r3, r0)         # shift mask  left r0 bits
    and_(r2, r3)        # this value will be someting like 0x0400 or 0x00
    lsr(r2, r0)         # shift result right r0 bits
    mov(r0, r2)         # and return it 
 
    
def read_digital(pin):
    # this is a dictionary, microbit.pinX can't be a __hash__
    if pin == pin0:
        bit_shift = 3
    elif pin == pin1:
        bit_shift = 2
    elif pin == pin2:
        bit_shift = 1
    elif pin == pin3:
        bit_shift = 4
    elif pin == pin4:
        bit_shift = 5
    elif pin == pin5:
        bit_shift = 17
    elif pin == pin6:
        bit_shift = 12
    elif pin == pin7:
        bit_shift = 11
    elif pin == pin8:
        bit_shift = 18
    elif pin == pin9:
        bit_shift = 10
    elif pin == pin10:
        bit_shift = 6
    elif pin == pin11:
        bit_shift = 26
    elif pin == pin12:
        bit_shift = 20
    elif pin == pin13:
        bit_shift = 23
    elif pin == pin14:
        bit_shift = 22
    elif pin == pin15:
        bit_shift = 21
    elif pin == pin16:
        bit_shift = 16
    else:
        raise Exception('function not suitable for this pin')

    return asm_read_digital(bit_shift)





display.off()
print("")
for p in range(17):
    if not p in (5, 11):
        pin = eval('pin{}'.format(p))
        # a dummy read_digital / this set_pull configures the pin as
        # read digital
        pin.set_pull(pin.PULL_DOWN)
        #print('pin{}\t'.format(p),end = ' ')
        #print(read_digital(pin))

for p in (5, 11):
    pin = eval('pin{}'.format(p))
    # a dummy read_digital / this set_pull configures the pin as
    # read digital
    pin.set_pull(pin.PULL_UP)
    #print('pin{}\t'.format(p),end = ' ')
    #print(read_digital(pin))
