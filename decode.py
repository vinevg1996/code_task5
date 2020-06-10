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

class Decoder:

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
        self.create_finite_field()
        return

    def create_finite_field(self):
        self.coeff_table = list()
        self.dig_table = list()
        self.F = ffield.FField(self.m)
        one = 1
        self.dig_table.append(one)
        self.coeff_table.append(list(self.F.ShowCoefficients(one)))
        alpha = 2
        self.coeff_table.append(list(self.F.ShowCoefficients(alpha)))
        self.dig_table.append(alpha)
        beta = alpha
        for i in range(2, self.size + 1):
            beta = self.F.Multiply(alpha, beta)
            self.dig_table.append(beta)
            self.coeff_table.append(list(self.F.ShowCoefficients(beta)))
        return

    def print_finite_field(self):
        print("coeff_table:")
        for i in range(0, len(self.coeff_table)):
            print(i, " : ", self.coeff_table[i])
        print("dig_table:")
        for i in range(0, len(self.dig_table)):
            print(i, " : ", self.dig_table[i])
        return

    def convert_str_to_poly(self, coeff_str):
        coeff_list = list()
        last_one = 0
        for i in range(0, len(coeff_str)):
            coeff_list.append(int(coeff_str[i]))
            if (coeff_str[i] == '1'):
                last_one = i
        return Poly(self.size, last_one, coeff_list)

    def give_poly_value(self, poly, power):
        curr_sum = 0
        for j in range(0, len(poly.coeff_list)):
            if (poly.coeff_list[j] != 0):
                fin_power = (power * j) % self.size
                curr_sum = self.F.Add(curr_sum, self.dig_table[fin_power])
        return curr_sum

    def give_poly_value_for_power(self, poly, power):
        curr_sum = 0
        for j in range(0, len(poly.coeff_list)):
            fin_power = (power * j) % self.size
            curr_mult = self.F.Multiply(poly.coeff_list[j], self.dig_table[fin_power])
            curr_sum = self.F.Add(curr_sum, curr_mult)
        return curr_sum

    def create_syndrom_table(self, poly):
        syndrom_table = list()
        for j in range(1, self.d):
            value = self.give_poly_value(poly, j)
            #print("j = ", j, " : ", "value = ", value)
            syndrom_table.append(value)
            #break
        return syndrom_table

    def decode_poly(self, poly):
        syndrom_table = self.create_syndrom_table(poly)
        b = 0
        b_1 = 1
        sigma_coeff = [0 for i in range(0, self.t + 1)]
        sigma_coeff[0] = 1
        sigma = Poly(self.t + 1, 0, sigma_coeff)
        sigma_1_coeff = [0 for i in range(0, self.t + 1)]
        sigma_1_coeff[0] = 1
        sigma_1 = Poly(self.t + 1, 0, sigma_1_coeff)
        t = 0
        t_1 = -1
        tmp_coeff = [0 for i in range(0, self.d)]
        for j in range(0, self.d - 1):
            b = syndrom_table[j]
            for i in range(1, t + 1):
                x = self.F.Multiply(sigma.coeff_list[i], syndrom_table[j - i])
                b = self.F.Add(b, x)
            if (b != 0):
                tmp = Poly(sigma.size, sigma.deg, sigma.coeff_list)
                tmp2 = sigma_1.shift_right_poly(j - t_1)
                c = self.F.Multiply(b, self.F.Inverse(b_1))
                for k in range(0, len(tmp2.coeff_list)):
                    tmp2.coeff_list[k] = self.F.Multiply(tmp2.coeff_list[k], c)
                for k in range(0, len(sigma.coeff_list)):
                    sigma.coeff_list[k] = self.F.Add(sigma.coeff_list[k], tmp2.coeff_list[k])
                if (j <= 2 * t):
                    t = j + 1 - t
                    t_1 = j
                    b_1 = b
                    sigma_1 = Poly(tmp.size, tmp.deg, tmp.coeff_list)
        return sigma

    def decode_file(self, in_file, out_file):
        input_desc = open(in_file, "r")
        lines = input_desc.readlines()
        line = str(lines[0])
        correct_line = str()
        count = len(line) // self.size
        for i in range(0, count):
            curr_poly = self.convert_str_to_poly(line[i * self.size : (i + 1) * self.size])
            sigma = self.decode_poly(curr_poly)
            roots = self.solve_equation(sigma.coeff_list)
            for j in range(0, self.size):
                if (j in roots):
                    if (line[i * self.size + j] == '0'):
                        correct_line += '1'
                    else:
                        correct_line += '0'
                else:
                    correct_line += str(line[i * self.size + j])
        unicode_str = self.convert_to_unicode(correct_line)
        decode_str = str()
        count = len(unicode_str) // 8
        for i in range(0, count):
            curr_ord = 0
            for j in range(0, 8):
                if (unicode_str[i * 8 + j] == '1'):
                    curr_ord = 2 * curr_ord + 1
                else:
                    curr_ord = 2 * curr_ord
            sym = chr(curr_ord)
            decode_str += str(sym)
        out_desc = open(out_file, "w")
        out_desc.write(decode_str)
        return

    def convert_to_unicode(self, correct_line):
        unicode_str = str()
        count = len(correct_line) // self.size
        for i in range(0, count):
            last_one = 0
            coeff_list = list()
            for j in range(0, self.size):
                if (correct_line[i * self.size + j] == '1'):
                    coeff_list.append(1)
                    last_one = j
                else:
                    coeff_list.append(0)
            curr_poly = Poly(self.size, last_one, coeff_list)
            [divider_poly, rem_poly] = curr_poly.divide_polynomials(self.gen_poly)
            for r in range(0, self.k):
                unicode_str += str(divider_poly.coeff_list[r])
        return unicode_str

    def solve_equation(self, sigma_coeff):
        locator_poly_coeff = [0 for j in range(0, len(sigma_coeff))]
        for i in range(0, len(sigma_coeff)):
            locator_poly_coeff[len(sigma_coeff) - 1 - i] = int(sigma_coeff[i])
        locator_poly = Poly(self.t + 1, self.t, locator_poly_coeff)
        roots = list()
        for i in range(0, self.size):
            value = self.give_poly_value_for_power(locator_poly, i)
            if (value == 0):
                roots.append(i)
        return roots