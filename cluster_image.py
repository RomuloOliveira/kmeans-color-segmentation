#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import random
import math
import os

from os import path

DEBUG = False

# Euclidian distance of two points. Call it hypotenuse if you want
def distance(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b

    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def read_input():
    import png

    # Next lines contains a pair of values
    #data = []
    #for line in sys.stdin:
    #    line = re.sub('[\n\r]*', '', line)
    #    x, y = [float(n) for n in re.sub('\s+', ' ', line).split(' ')]
    #    data.append((x, y))

    #data = [(x, y) for x,y in [[float(n) for n in re.sub('\s+', ' ', re.sub('[\n\r]*', '', line)).split(' ')] for line in sys.stdin]]
    #data = [(random.random() * 10, random.random() * 10, random.random() * 10) for x in range(10) for y in range(10) for z in range(10)]

    # Flexible path
    filename = path.normpath(path.expandvars(path.expanduser(sys.argv[1])))

    w, h, pixels, meta = png.Reader(filename = filename).asRGB()

    print w, h

    data = []

    for p in pixels:
        r = range(0, len(p), 3)
        for i in r:
            px = (p[i], p[i+1], p[i+2])
            data.append(px)

    return data, w, h

def select_first_candidates(data, k):
    p = set()

    while len(p) != k:
        p.add(random.choice(data))

    return p


def select_prototypes(data, groups):
    l = []
    for g in groups:

        sum_x = 0
        sum_y = 0
        sum_z = 0
        for x, y, z in g:
            sum_x = sum_x + x
            sum_y = sum_y + y
            sum_z = sum_z + z


        l.append((sum_x/len(g), sum_y/len(g), sum_z/len(g)))

    return l

def rearrage_groups(data, prototypes):

    groups = [[] for _ in range(len(prototypes))]
    indexes = []

    for d in data:

        minimum = sys.maxint
        i = 0
        group_number = 0

        for p in prototypes:
            dis = distance(d, p)

            if (dis < minimum):
                group_number = i
                minimum = dis

            i = i + 1

        indexes.append(group_number)
        groups[group_number].append(d)

    return groups, indexes

def sum_squares(prototypes, groups):

    i = 0
    ssum = 0

    for group in groups:

        for point in group:
            ssum = ssum + distance(point, prototypes[i])**2

        i = i + 1

    return ssum

def write_image(run, k, width, height, indexes, prototypes):
    import png

    # Vamos usar os próprios protótipos como cores. Com cores aleatórios fica muito feio e
    # dessa forma dá pra perceber melhor
    colors = prototypes

    data = []

    for idx in indexes:
        r, g, b = colors[idx]

        data.append(r)
        data.append(g)
        data.append(b)

    im = png.Writer(width, height)

    try:
        os.mkdir('./out')
    except:
        pass

    f = open('./out/out_{}_{}.png'.format(k, run), 'w')

    im.write_array(f, data)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: python {} [image_file]'.format(sys.argv[0])
        exit()

    k_runnings = [4, 8, 16]
    runnings = 3

    input_data, w, h = read_input()

    for k in k_runnings:

        for run in range(runnings):

            print '====== RUNNING {} FOR {} CLUSTERS ==== '.format(run, k)

            groups = None
            prototypes = select_first_candidates(input_data, k)

            print 'Centroides iniciais:', prototypes

            iterations = 0
            while True:
                iterations = iterations + 1

                last_prototypes = prototypes

                last_groups = groups

                groups, indexes = rearrage_groups(input_data, prototypes)
                prototypes = select_prototypes(input_data, groups)

                print '==== ITERACAO {} ===='.format(iterations)

                if last_groups == groups:
                    break

            print 'Total de iteracoes:', iterations

            print 'Soma dos erros quadráticos:', sum_squares(prototypes, groups)

            write_image(run, k, w, h, indexes, prototypes)
