import time
@micropython.asm_thumb
def asm_sleep_us(r0):

    sub(r0, 0)
    bne(sleep)
    b(END)

    cpsid('i')          # disable interrupts to go really fast

    label(sleep)
    mov(r7, 0x1)
    lsl(r7, r7, 6)
    add(r7, 0x0e)
    lsl(r7, r7, 8)
    add(r7, 0xf0)
    label(delay_loop)
    sub(r7, 1)
    bne(delay_loop)
    sub(r0, 1)
    bne(end_sleep)
    b(sleep)
    label(end_sleep)

    cpsie('i')          # enable interrupts to go really fast

    label(END)

begin=time.ticks_us()

asm_sleep_us(2000 * 16)
end=time.ticks_us()
print(time.ticks_diff(end,begin))
