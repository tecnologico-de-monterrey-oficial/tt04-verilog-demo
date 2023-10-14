import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


segments = [ 63, 6, 91, 79, 102, 109, 124, 7, 127, 103 ]

async def check_display(dut, compare):
    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    # set the compare value
    dut.ui_in.value = compare
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # the compare value is shifted 10 bits inside the design to allow slower counting
    max_count = compare << 10
    dut._log.info(f"check all segments with compare set to {compare} [{max_count} cycles]")
    # check all segments and roll over
    for i in range(15):
        dut._log.info(f"check segment {i%10}")
        await ClockCycles(dut.clk, max_count)
        assert int(dut.segments.value) == segments[i % 10]

        # all bidirectionals are set to output
        assert dut.uio_oe == 0xFF

@cocotb.test()
async def test_7seg(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    await check_display(dut, 1)
    await check_display(dut, 5)
    await check_display(dut, 10)

