from microbit import *
import machine
# r0 - the number of bits to shift for given pin
@micropython.asm_thumb
def asm_read_digital():

    mov(r1, 0x50)       # r1=0x50
    lsl(r1, r1, 16)     # r1=0x500000
    add(r1, 0x05)       # r1=0x500005
    lsl(r1, r1, 8)      
    add(r1, 0x10)       # r1=0x50000510 -- this points to GPIO read digita
    ldr(r0, [r1,0] )    # move memory@r1 to r2

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
    pin.read_digital()
    pin.set_pull(pin.PULL_DOWN)

for i in range(32):
    print((31-i)%10, end = "")
print("")

value=asm_read_digital()
binary(value)
print(' \t',value)
sleep(5000)
value=asm_read_digital()
binary(value)
print(' \t',value)


