#!/usr/bin/env python

from gnuradio import gr, gr_unittest, blocks

from xor_frame_sync import xor_frame_sync
import numpy as np


class test_xor_frame_sync(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        """Test a byte aligned delay"""
        pattern = np.array([0xc0, 0xff, 0xee], dtype=np.uint8)
        testdata = np.packbits(np.concatenate([
            np.unpackbits(np.arange(0, 5, dtype=np.uint8)),
            # np.random.randint(0, 2, size = 8 * 5),
            np.unpackbits(pattern),
            np.random.randint(0, 2, size = 64)
        ]))

        src = blocks.vector_source_b(testdata)
        op = xor_frame_sync(pattern, 2048)
        dst = blocks.vector_sink_b()

        self.tb.connect(src, op, dst)
        self.tb.run()

        self.assertEqual(op.synchronized, True)

    # FIXME: implement feature
    # def test_002(self):
    #     """Test a byte unaligned delay"""
    #     pattern = np.array([0xbe, 0xef], dtype=np.uint8)
    #     testdata = np.packbits(np.concatenate([
    #         np.unpackbits(np.arange(0, 10, dtype=np.uint8)),
    #         np.random.randint(0, 2, size = (2 + 8 * 5)), np.unpackbits(pattern),
    #         np.random.randint(0, 2, size = 64)
    #     ]))

    #     src = blocks.vector_source_b(testdata)
    #     op = xor_frame_sync(pattern, 2048)
    #     dst = blocks.vector_sink_b()

    #     self.tb.connect(src, op, dst)
    #     self.tb.run()

    #     self.assertEqual(op.synchronized, True)


if __name__ == "__main__":
    gr_unittest.run(test_xor_frame_sync)
