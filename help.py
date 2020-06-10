#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from combinatorics import Combinatorics

class Help:

    def calculate_factorial(self, n):
        fact = 1
        for i in range(2, n + 1):
            fact = fact * i
        return fact

    def calculate_comb(self, n, k):
        comb = 1
        for i in range(n - k + 1, n + 1):
            comb = comb * i
        comb = comb // self.calculate_factorial(k)
        return comb

    def sum_of_vectors(self, matrix, combination):
        new_vector = list(matrix[combination[0]])
        for i in range(1, len(combination)):
            for j in range(0, len(new_vector)):
                new_vector[j] = (new_vector[j] + matrix[combination[i]][j]) % 2
        return new_vector

    def convert_decimal_to_binary(self, dec, base):
        string = "{0:{fill" + "}" + str(base) + "b}"
        res_str = string.format(dec, fill='0')
        res_dig = [int(sym) for sym in res_str]
        return res_dig

    def convert_binary_to_decimal(self, binary_list, base):
        dig = 0
        for i in range(0, base):
            dig = dig + binary_list[i] * (2 ** (base - i - 1))
        return dig

    def transpose_matrix(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        transpose_matrix = list()
        for j in range(0, m):
            curr_list = [ matrix[i][j] for i in range(0, n) ]
            transpose_matrix.append(curr_list)
        return transpose_matrix

    def change_rows_order(self, matrix):
        # m < n
        n = len(matrix)
        m = len(matrix[0])
        for i in range(0, m):
            temp = list(matrix[m - i - 1])
            matrix[m - i - 1] = list(matrix[n - i - 1])
            matrix[n - i - 1] = temp
        return

    def mult_vector_for_matrix(self, vec, matrix):
        res_vec = list()
        sum_ceil = 0
        for j in range(0, len(matrix[0])):
            for i in range(0, len(vec)):
                sum_ceil = (sum_ceil + vec[i] * matrix[i][j]) % 2
            res_vec.append(int(sum_ceil))
            sum_ceil = 0
        return res_vec

    def mult_matrix_for_vector(self, matrix, vec):
        res_vec = list()
        sum_ceil = 0
        for i in range(0, len(matrix)):
            for j in range(0, len(vec)):
                sum_ceil = (sum_ceil + matrix[i][j] * vec[j]) % 2
            res_vec.append(int(sum_ceil))
            sum_ceil = 0
        return res_vec

    def mult_matrix_for_matrix(self, matrix1, matrix2):
        matrix = list()
        n = len(matrix1)
        m = len(matrix1[0])
        k = len(matrix2[0])
        for vec in matrix1:
            res_vec = self.mult_vector_for_matrix(vec, matrix2)
            matrix.append(list(res_vec))
        return matrix

    def find_min_weight_in_depend_list(self, depend_list, size):
        Comb = Combinatorics()
        flag = True
        i = 1
        while (i < size) and (flag):
            allCombinations = []
            Comb.GenerationAllCombinations(allCombinations, size, i)
            #print("allCombinations: ", allCombinations)
            j = 0
            while (j < len(allCombinations)) and (flag):
                curr_list = [0 for x in range(0, size)]
                for index in allCombinations[j]:
                    curr_list[index] = 1
                dec = self.convert_binary_to_decimal(curr_list, size)
                if (depend_list[dec] == 0):
                    flag = False
                    depend_list[dec] = 1
                j = j + 1
            i = i + 1
        return curr_list

    def xor(self, vec1, vec2):
        vec = [(vec1[i] + vec2[i]) % 2 for i in range(0, len(vec1))]
        return vec

    def calculate_weight_for_vector(self, vector):
        weight = vector.count(1)
        return weight