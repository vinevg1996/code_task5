#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from pyfinite import ffield
from poly import Poly
from help import Help
import time
import math
###########################


class CodeCreator:
    
    def __init__(self, n, p):
        self.coeff_table = list()
        self.dig_table = list()
        self.cyclomatic_classes = list()
        self.m = int(math.log(n, 2)) + 1
        self.size = 2 ** self.m - 1
        self.p = p
        #self.entropy = (-1) * p * math.log2(p) + (-1) * (1 - p) * math.log2(1 - p)
        self.entropy = (-1) * p * math.log(p, 2) + (-1) * (1.0 - p) * math.log(1.0 - p, 2)
        self.r = int(self.size * self.entropy) + 1
        self.k = self.size - self.r
        self.d = self.calculate_dist()
        self.t = (self.d - 1) // 2
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
        self.create_cyclomatic_classes()
        self.gen_poly = self.create_generate_poly(self.t)
        self.verify_poly = self.create_verify_poly()
        return

    def write_code_to_file(self, out_file):
        out_file_desc = open(out_file, 'w')
        out_str = "size = " + str(self.size) + "\n"
        out_file_desc.write(out_str)
        out_str = "m = " + str(self.m) + "\n"
        out_file_desc.write(out_str)
        out_str = "k = " + str(self.k) + "\n"
        out_file_desc.write(out_str)
        out_str = "r = " + str(self.r) + "\n"
        out_file_desc.write(out_str)
        out_str = "d = " + str(self.d) + "\n"
        out_file_desc.write(out_str)
        out_str = "t = " + str(self.t) + "\n"
        out_file_desc.write(out_str)
        out_str = "p = " + str(self.p) + "\n"
        out_file_desc.write(out_str)
        out_str = "deg = " + str(self.gen_poly.deg) + "\n"
        out_file_desc.write(out_str)
        gen_poly = list(self.gen_poly.coeff_list[:len(self.gen_poly.coeff_list) - 1])
        gen_poly_str = str()
        for i in range(0, len(gen_poly)):
            gen_poly_str += str(gen_poly[i])
            if (i != len(gen_poly) - 1):
                gen_poly_str += ' '
        out_file_desc.write(gen_poly_str)
        out_file_desc.write("\n")
        return

    def calculate_dist(self):
        helper = Help()
        sum_combs = 1
        i = 1
        flag = True
        while flag:
            sum_combs = sum_combs + helper.calculate_comb(self.size - 1, i)
            if (sum_combs >= 2 ** self.r):
                flag = False
            else:
                i = i + 1
        dist = i + 1
        if (dist <= self.r - 1):
            return dist
        else:
            return self.r - 1

    def old_init(self, size, m):
        self.coeff_table = list()
        self.dig_table = list()
        self.cyclomatic_classes = list()
        self.size = size
        self.m = m
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
        self.create_cyclomatic_classes()
        return

    def create_cyclomatic_classes(self):
        bool_flag = [0 for i in range(0, self.size)]
        bool_flag[0] = 1
        curr_class = [0]
        self.cyclomatic_classes.append(curr_class)
        while (bool_flag.count(0) > 0):
            curr_class = list()
            leader_class = bool_flag.index(0)
            curr_class.append(leader_class)
            bool_flag[leader_class] = 1
            flag = True
            prev_elem = leader_class
            while flag:
                curr_elem = (prev_elem * 2) % (self.size)
                if (curr_elem == leader_class):
                    self.cyclomatic_classes.append(list(curr_class))
                    flag = False
                else:
                    bool_flag[curr_elem] = 1
                    curr_class.append(curr_elem)
                    prev_elem = curr_elem
        return

    def mult_poly(self, poly1, poly2):
        deg = poly1.deg + poly2.deg
        poly_coeff = [0 for i in range(0, self.size)]
        for i in range(0, deg + 1):
            curr_sum = 0
            for j in range(0, i + 1):
                curr_elem = self.F.Multiply(poly1.coeff_list[j], poly2.coeff_list[i - j])
                curr_sum = self.F.Add(curr_sum, curr_elem)
            poly_coeff[i] = curr_sum
        return Poly(self.size, deg, poly_coeff)

    def create_generate_poly(self, number_min_func):
        gen_poly = self.create_minimum_function(1)
        for i in range(2, number_min_func + 1):
            min_poly = self.create_minimum_function(i)
            gen_poly = self.mult_poly(gen_poly, min_poly)
        return gen_poly

    def create_verify_poly(self):
        ext_gen_poly = Poly(self.gen_poly.size + 1, self.gen_poly.deg, self.gen_poly.coeff_list)
        gen_field_coef = [0 for i in range(0, self.size + 1)]
        gen_field_coef[0] = 1
        gen_field_coef[self.size] = 1
        gen_field_poly = Poly(self.size + 1, self.size, gen_field_coef)
        [divider_poly, new_poly] = gen_field_poly.divide_polynomials(ext_gen_poly)
        return divider_poly

    def create_minimum_function(self, class_id):
        polynomials = list()
        for power in self.cyclomatic_classes[class_id]:
            curr_poly_coeff = [self.dig_table[power], 1]
            #print("curr_poly_coeff = ", curr_poly_coeff)
            curr_poly = Poly(self.size, 1, curr_poly_coeff)
            polynomials.append(curr_poly)
        poly = polynomials[0]
        for i in range(1, len(polynomials)):
            poly = self.mult_poly(poly, polynomials[i])
        return poly
