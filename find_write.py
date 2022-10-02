from microbit import *
import machine

@micropython.asm_thumb
def asm_write_word(r0):

    mov(r1, 0x50)       # r1=0x50
    lsl(r1, r1, 16)     # r1=0x500000
    add(r1, 0x05)       # r1=0x500005
    lsl(r1, r1, 8)      
    add(r1, 0x10)        # r1=0x50000510 -- this points to GPIO read digita
    sub(r0, 0)
    bne(get_12)
    ldr(r0, [r1, 8] )    # move memory@r1 to r2
    b(end)
    label(get_12)
    ldr(r0, [r1, 12] )    # move memory@r1 to r2
    label(end)
    
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
        pin.write_digital(0)
    except:
        pass
    

for i in range(32):
    print((31-i)%10, end = "")
print("")

pin=pin0

pin.write_digital(1)
value=asm_write_word(1)
binary(value)
print(' \t',value)
pin.write_digital(0)
value=asm_write_word(0)
binary(value)
print(' \t',value)


