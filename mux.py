from myhdl import *
from math import log2


def generate_mux_signals(BIT_WIDTH = 16, DEPTH = 4):
    ret = {}

    ret['d'] = Signal(intbv(0)[BIT_WIDTH*DEPTH:])
    ret['sel'] = Signal(intbv(0)[int.bit_length(DEPTH):])
    ret['q'] = Signal(intbv(0)[BIT_WIDTH:])

    return ret

@block
def mux(d, sel, q):

    @always_comb
    def logic():
        q.next = d[sel*len(q):(sel+1)*len(q)-1]

    return logic


if __name__ == '__main__':
    sigs = generate_mux_signals()
    tmp = mux(**sigs)
    tmp.convert()
