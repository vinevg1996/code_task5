#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from pyfinite import ffield
from poly import Poly
from code import CodeCreator
from encode import Encoder
from decode import Decoder
import time
import sys
###########################

if (sys.argv[1] == "mode=1"):
    n = int(sys.argv[2])
    p = float(sys.argv[3])
    Code = CodeCreator(n, p)
    Code.write_code_to_file(sys.argv[4])
elif (sys.argv[1] == "mode=2"):
    enc = Encoder(sys.argv[2])
    encode_str = enc.encode_file(sys.argv[3])
    enc.write_to_file_with_noise(encode_str, sys.argv[4])
    enc.write_to_file(encode_str, sys.argv[5])
elif (sys.argv[1] == "mode=3"):
    dec = Decoder(sys.argv[2])
    decode_str = dec.decode_file(sys.argv[3], sys.argv[4])
