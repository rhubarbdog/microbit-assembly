from microbit import *

@micropython.asm_thumb
def asm_write(r0):
    # pin-bit value to write 0/1
    cpsid('i')      # disable interrupts

    mov(r2, 0x50)       # r1=0x50
    lsl(r2, r2, 16)     # r1=0x500000
    add(r2, 0x05)       # r1=0x500005
    lsl(r2, r2, 8)      
    #add(r2, 0x10)        # r1=0x50000510 -- this points to GPIO read digita

    add(r2, r2, r0)

    mov(r5, 0xff)
    lsl(r5, r5, 8)
    add(r5,  0xff)
    lsl(r5, r5, 8)
    add(r5,  0xff)
    lsl(r5, r5, 8)
    add(r5,  0xff)
    mov(r4, 0x1)
    lsl(r4, r4, 19)
    eor(r5, r4)
    str(r5, [r2, 0] )    #lo


    mov(r7, 1<<7)
    lsl(r7, r7, 15)

    label(delay)
    sub(r7, 1)
    bne(delay)

    cpsie('i')      # enable interrupts
    mov(r0, r5)

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
    

pin=pin0
#pin.write_digital(1)
#sleep(1000)
#pin.write_digital(0)

for i in range(0,128,4):
    print(i, end = " ")
    asm_write(i)
    print('*')
