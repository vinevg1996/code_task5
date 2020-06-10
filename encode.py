#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from pyfinite import ffield
from poly import Poly
from code import CodeCreator
import time
import random
import sys

###########################

#size = 15
#m = 4
#k = 5
#r = 10
#d = 5
#t = 2

class Encoder:

    def __init__(self, code_file):
        self.code_info_desc = open(code_file, "r")
        lines = self.code_info_desc.readlines()
        self.size = int(lines[0].split('=')[1])
        self.m = int(lines[1].split('=')[1])
        self.k = int(lines[2].split('=')[1])
        self.r = int(lines[3].split('=')[1])
        self.d = int(lines[4].split('=')[1])
        self.t = int(lines[5].split('=')[1])
        self.p = float(lines[6].split('=')[1])
        deg = int(lines[7].split('=')[1])
        coeff_list_lines = lines[8].split(' ')
        coeff_list = [int(elem) for elem in coeff_list_lines ]
        self.gen_poly = Poly(self.size, deg, coeff_list)
        return

    def write_to_file(self, encode_str, out_file):
        output_desc = open(out_file, "w")
        output_desc.write(encode_str)
        return

    def write_to_file_with_noise(self, encode_str, out_file):
        random.seed()
        output_desc = open(out_file, "w")
        noise_encode_str = str()
        for sym in encode_str:
            prob = random.random()
            if (prob < self.p):
                if (sym == '0'):
                    noise_encode_str += '1'
                else:
                    noise_encode_str += '0'
            else:
                noise_encode_str += str(sym)
        output_desc.write(noise_encode_str)
        return

    def encode_file(self, in_file):
        input_desc = open(in_file, "r")
        binary_str = str()
        for line in input_desc:
            for sym in line:
                sym_str = "{0:{fill}8b}".format(ord(sym), fill='0')
                binary_str += sym_str
        #print("binary_str = ", binary_str)
        count = len(binary_str) // self.k
        encode_str = str()
        for i in range(0, count):
            last_one = 0
            coeff_list = list()
            for j in range(0, self.k):
                if (binary_str[i * self.k + j] == '1'):
                    coeff_list.append(1)
                    last_one = j
                else:
                    coeff_list.append(0)
            curr_poly = Poly(self.size, last_one, coeff_list)
            encode_poly = self.gen_poly.mult_poly(curr_poly)
            #encode_poly.print_poly()
            encode_poly_str = encode_poly.convert_poly_to_str()
            encode_str += encode_poly_str
        coeff_list = [0 for i in range(0, self.k)]
        last_one = 0
        for j in range(0, len(binary_str) - count * self.k):
            if (binary_str[count * self.k + j] == '1'):
                coeff_list[j] = 1
                last_one = j
        curr_poly = Poly(self.size, last_one, coeff_list)
        encode_poly = self.gen_poly.mult_poly(curr_poly)
        #encode_poly.print_poly()
        encode_poly_str = encode_poly.convert_poly_to_str()
        encode_str += encode_poly_str
        return encode_str