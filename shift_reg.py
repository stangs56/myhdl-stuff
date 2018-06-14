from myhdl import *
from random import randrange
from sys import argv

def generate_shift_reg_signals():
    ret = {}

    for i in ['ser_in', 'ser_out', 'output_latch', 'clk', 'clk_en']:
        ret[i] = Signal(bool(0))

    ret['data_out'] = Signal(intbv(0)[8:])

    return ret

@block
def shift_reg(ser_in, data_out, ser_out, output_latch, clk, clk_en):

    tmp = Signal(intbv(0)[8:])

    @always(clk.posedge)
    def logic():
        if clk_en:
            tmp.next[len(tmp)-1] = ser_in
            ser_out.next = tmp[0]

            for i in range(len(tmp)-1):
                tmp.next[i] = tmp[i+1]

        if output_latch:
            data_out.next = tmp

    return logic

@block
def test_shift_reg():
    sigs = generate_shift_reg_signals()
    inst = shift_reg(**sigs)

    @always(delay(10))
    def clkgen():
        sigs['clk'].next = not sigs['clk']

    @always(sigs['clk'].negedge)
    def stimulus():
        sigs['clk_en'].next = True
        sigs['output_latch'].next = True
        sigs['ser_in'].next = randrange(2)

    return inst, clkgen, stimulus

if __name__ == "__main__":
    if argv[1] == 'convert':
        sigs = generate_shift_reg_signals()
        inst = shift_reg(**sigs)
        inst.convert(hdl='Verilog')

    if argv[1] == 'sim':
        tmp = test_shift_reg()
        tmp.config_sim(trace=True)
        tmp.run_sim(3000)
