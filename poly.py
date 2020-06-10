#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

class Poly:
    def __init__(self, size, deg, coeff_list):
        self.size = int(size)
        self.coeff_list = list(coeff_list)
        self.deg = int(deg)
        #for i in range(len(coeff_list), size + 1):
        for i in range(len(coeff_list), size):
            self.coeff_list.append(0)
        return

    def shift_right_poly(self, n):
        new_coeff_list = self.coeff_list[-n:] + self.coeff_list[:-n]
        return Poly(self.size, self.deg + n, new_coeff_list)

    def print_poly(self):
        #print("deg_poly = ", self.deg)
        #print("poly = ", self.coeff_list)
        for i in range(0, len(self.coeff_list)):
            if (self.coeff_list[i] == 1):
                print('x^', end='')
                print(i, end='')
                print('+', end='')
        print()
        return

    def sum_polynomials(self, poly2):
        new_coeff_list = [0 for i in range(0, self.size)]
        last_one = 0
        for i in range(0, len(new_coeff_list)):
            new_coeff_list[i] = (self.coeff_list[i] + poly2.coeff_list[i]) % 2
            if (new_coeff_list[i] == 1):
                last_one = i
        return Poly(self.size, last_one, new_coeff_list)

    def divide_polynomials(self, poly2):
        #print("source_poly")
        #self.print_poly()
        diff_degs = self.deg - poly2.deg
        new_poly = Poly(self.size, self.deg, self.coeff_list)
        divider_coeff = [0 for i in range(0, self.size)]
        divider_power = diff_degs
        while (diff_degs >= 0):
            divider_coeff[diff_degs] = 1
            divider = poly2.shift_right_poly(diff_degs)
            #print("divider")
            #divider.print_poly()
            new_poly = new_poly.sum_polynomials(divider)
            #print("new_poly")
            #new_poly.print_poly()
            diff_degs = new_poly.deg - poly2.deg
            #time.sleep(0.5)
            #break
        divider_poly = Poly(self.size, divider_power, divider_coeff)
        return [divider_poly, new_poly]

    def mult_poly(self, poly2):
        #new_poly = Poly(self.size, self.deg, self.coeff_list)
        new_coeff_list = [0 for i in range(0, self.size)]
        new_deg = 0
        new_poly = Poly(self.size, new_deg, new_coeff_list)
        for j in range(0, poly2.deg + 1):
            if (poly2.coeff_list[j] == 1):
                shift_poly = self.shift_right_poly(j)
                new_poly = new_poly.sum_polynomials(shift_poly)
        return new_poly

    def convert_poly_to_str(self):
        out_str = str()
        for elem in self.coeff_list:
            out_str += str(elem)
        return out_str
