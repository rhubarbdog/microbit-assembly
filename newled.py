from microbit import *
"""
This script uses the inline assembler to make the LEDs light up
in a pattern based on how they are multiplexed in rows/cols.
"""

# row pins: 13, 14, 15
# col pins: 4..12 inclusive
# GPIO words starting at 0x50000500:
#   RESERVED, OUT, OUTSET, OUTCLR, IN, DIR, DIRSET, DIRCLR

@micropython.asm_thumb
def led_cycle(r0, r1):
    b(START)

    # DELAY routine
    label(DELAY)
    mov(r7, 0xa0)
    lsl(r7, r7, 15)
    label(delay_loop)
    sub(r7, 1)
    bne(delay_loop)
    bx(lr)

    label(START)

    cpsid('i')          # disable interrupts so we control the display

    mov(r2, 0x50)       # r0=0x50
    lsl(r2, r2, 16)     # r0=0x500000
    add(r2, 0x05)       # r0=0x500005
    lsl(r2, r2, 8)      # r0=0x50000500 -- this points to GPIO registers
    mov(r3, 0b11111)
    sub(r0, 0)
    bne(left_row)
    b(cont_row)
    label(left_row)
    lsl(r3, r3, 1)
    sub(r0, 1)
    bne(left_row)
    label(cont_row)    
    str(r3, [r2, 8])    # pull all rows high
    mov(r0, r3)

    mov(r3, 0b11111)     # r1 holds current col bit
    mov(r5,r1)
    sub(r5, 0)
    bne(left_col)
    b(cont_col)
    label(left_col)
    lsl(r3, r3, 1)
    sub(r5, 1)
    bne(left_col)
    label(cont_col)
    
    str(r3, [r2, 12])   # pull col low to turn LEDs on
    bl(DELAY)           # wait
    str(r3, [r2, 8])   # pull col hi to turn LEDs off
    mov(r0, r3)

    cpsie('i')      # enable interrupts

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


for r in range(28):
    for c in range(28):
        print(r,"%2d" % c, end = ' ')
        binary(led_cycle(r,c))
        print("", end = '\r')

    print("")
