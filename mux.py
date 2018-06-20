from myhdl import *


def generate_mux_signals(BIT_WIDTH = 16, DEPTH = 4):
    ret = {}

    ret['d'] = Signal(intbv(0)[BIT_WIDTH*DEPTH:])
    ret['sel'] = Signal(intbv(0)[int.bit_length(DEPTH-1):])
    ret['q'] = Signal(intbv(0)[BIT_WIDTH:])

    return ret

@block
def mux(d, sel, q):

    @always_comb
    def logic():
        q.next = d[(sel+1)*len(q):sel*len(q)]

    return logic

@block
def test_mux(BIT_WIDTH = 8, DEPTH = 4):
    sigs = generate_mux_signals(BIT_WIDTH, DEPTH)

    input = [Signal(intbv(0)[BIT_WIDTH:]) for _ in range(DEPTH)]

    # for idx, tmp in enumerate(input):
    #     sigs['d'][(idx+1)*BIT_WIDTH:idx*BIT_WIDTH] = tmp

    sigs['d'] = ConcatSignal(*input)

    inst = mux(**sigs)

    input.reverse()

    @instance
    def stimulus():
        for i in range(DEPTH):
            for ii in range(2**BIT_WIDTH):
                input[i].next = ii
                sigs['sel'].next = i
                yield delay(1)
                if sigs['q'] != ii:
                    print('''error:\n\tSelected: {}\n\tInput: {}\n\tOutput: {}'''
                        .format(i, ii, sigs['q']))

    return inst, stimulus



if __name__ == '__main__':
    # sigs = generate_mux_signals()
    # tmp = mux(**sigs)
    # tmp.convert()

    tmp = test_mux()
    tmp.config_sim(trace=True)
    tmp.run_sim(1500)
