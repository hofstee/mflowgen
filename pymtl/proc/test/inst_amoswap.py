#=========================================================================
# amoswap
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0xdeadbeef
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    amoswap x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw x4, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0xcafebabe
    csrw proc2mngr, x4 > 0xdeadbeef

    .data
    .word 0xcafebabe
  """
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    # Test swap ping-pong

    gen_amo_value_test( "amoswap", 0x00002000, 0xffffffff, 0xcafebabe, 0xffffffff ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xcafebabe, 0xffffffff, 0xcafebabe ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xffffffff, 0xcafebabe, 0xffffffff ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xcafebabe, 0xffffffff, 0xcafebabe ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xffffffff, 0xcafebabe, 0xffffffff ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xcafebabe, 0xffffffff, 0xcafebabe ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xffffffff, 0xcafebabe, 0xffffffff ),
    gen_amo_value_test( "amoswap", 0x00002000, 0xcafebabe, 0xffffffff, 0xcafebabe ),

    gen_amo_value_test( "amoswap", 0x00002004, 0x88888888, 0x99999999, 0x88888888 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x77777777, 0x88888888, 0x77777777 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x66666666, 0x77777777, 0x66666666 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x55555555, 0x66666666, 0x55555555 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x44444444, 0x55555555, 0x44444444 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x33333333, 0x44444444, 0x33333333 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x22222222, 0x33333333, 0x22222222 ),
    gen_amo_value_test( "amoswap", 0x00002004, 0x11111111, 0x22222222, 0x11111111 ),

    # Test misc

    gen_amo_value_test( "amoswap", 0x00002008, 0x1111, 0xdeadbeef, 0x1111 ),
    gen_amo_value_test( "amoswap", 0x0000200c, 0x2222, 0xdeadbeef, 0x2222 ),
    gen_amo_value_test( "amoswap", 0x00002010, 0x3333, 0xdeadbeef, 0x3333 ),
    gen_amo_value_test( "amoswap", 0x00002014, 0x4444, 0xdeadbeef, 0x4444 ),
    gen_amo_value_test( "amoswap", 0x00002018, 0x5555, 0xdeadbeef, 0x5555 ),
    gen_amo_value_test( "amoswap", 0x0000201c, 0x6666, 0xdeadbeef, 0x6666 ),

    gen_amo_value_test( "amoswap", 0x00002020, 0xdeadbeef, 0xcafebabe, 0xdeadbeef ),
    gen_amo_value_test( "amoswap", 0x00002024, 0xffffffff, 0xcafebabe, 0xffffffff ),
    gen_amo_value_test( "amoswap", 0x00002028, 0xf0f0f0f0, 0xcafebabe, 0xf0f0f0f0 ),
    gen_amo_value_test( "amoswap", 0x0000202c, 0x00000000, 0xcafebabe, 0x00000000 ),

    gen_word_data([
      0xcafebabe,
      0x99999999,

      0xdeadbeef,
      0xdeadbeef,
      0xdeadbeef,
      0xdeadbeef,
      0xdeadbeef,
      0xdeadbeef,

      0xcafebabe,
      0xcafebabe,
      0xcafebabe,
      0xcafebabe,
    ])

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():

  # Generate some random data

  data = []
  for i in xrange(128):
    data.append( random.randint(0,0xffffffff) )

  # AMOs modify the data, so keep a copy of the original data to dump later

  original_data = list(data)

  # Generate random accesses to this data

  asm_code = []
  for i in xrange(50):

    a = random.randint(0,127)
    b = random.randint(0,127)

    addr        = 0x2000 + (4*a)
    result_pre  = data[a]
    result_post = b # swap
    data[a]     = result_post

    asm_code.append( \
        gen_amo_value_test( "amoswap", addr, b, result_pre, result_post ) )

  # Add the data to the end of the assembly code

  asm_code.append( gen_word_data( original_data ) )
  return asm_code
