from microbit import *

@micropython.asm_thumb
# pin-bit, value to write 0/1
def asm_write(r0, r1):
    cpsid('i')      # disable interrupts

    mov(r2, 0x50)       # r1=0x50
    lsl(r2, r2, 16)     # r1=0x500000
    add(r2, 0x05)       # r1=0x500005
    lsl(r2, r2, 8)      # r1=0x50000500 -- this points to GPIO write digita

    mov(r5, 0x1)
    sub(r0, 0)
    bne(loop)
    b(cont)
    label(loop)
    lsl(r5, r5, 1)
    sub(r0, 1)
    bne(loop)
    label(cont)

    sub(r1, 0)
    bne(high)
    str(r5, [r2, 12] )    #lo
    b(end)

    label(high)
    str(r5, [r2, 8] )    #hi

    label(end)
    cpsie('i')      # enable interrupts
    mov(r0, r5)

def pin2bit(pin):
    # this is a dictionary, microbit.pinX can't be a __hash__
    if pin == pin0:
        bit_id = 2
    elif pin == pin1:
        bit_id = 3
    elif pin == pin2:
        bit_id = 4
    elif pin == pin3:
        bit_id = 31
    elif pin == pin4:
        bit_id = 28
    elif pin == pin7:
        bit_id = 11
    elif pin == pin8:
        bit_id = 10
    elif pin == pin9:
        bit_id = 9
    elif pin == pin10:
        bit_id = 30 
    elif pin == pin12:
        bit_id = 12
    elif pin == pin13:
        bit_id = 17
    elif pin == pin14:
        bit_id = 1
    elif pin == pin15:
        bit_id = 13
        # con't find pin16
    else:
        raise ValueError('function not suitable for this pin')

    return bit_id

def binary(value):

    if value<0:
        print(1,end="")
        value=value+(1<<31)
    else:
        print(0,end="")

    check=1<<30        
    while check>0:
        if value>=check:
            print(1, end="")
            value=value-check
        else:
            print(0, end="")
            
        check = check // 2

 
display.off()
for p in range(17):
    pin = eval('pin{}'.format(p))
    try:
        pin.write_digital(1)
    except:
        pass

for i in range(32):
    print(i, end = " ")
    asm_write(i,0)
    sleep(500)
    asm_write(i,1)
    print('*')
