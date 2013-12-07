# -*- coding:utf-8 -*-

import argparse, math, sys

def main():
    parser = argparse.ArgumentParser(description='Let\'s order pizza!')

    parser.add_argument('-k', '--kind', type=int, choices=xrange(1,27),
                        dest='kind', default=3, nargs='+', help='kind of pizza')
    parser.add_argument('-s', '--size', type=int, choices=[35, 45], dest='size',
                        default=45, nargs='+', help='size of pizza')
    parser.add_argument('-n', '--num', type=int, dest='num', default='1',
                        nargs='+', help='number of pizza')

    args = parser.parse_args()

    if not (len(args.kind) == len(args.size) == len(args.num)):
        print 'Error: You have to equalize num of arguments(k, s, and n).'
        sys.exit()

    pizza_dict = {}
    for line in open("pizza_list.txt","r"):
        pizza_info = line.strip().split(',')
        pizza_dict[int(pizza_info[0])] = {'name':pizza_info[1], 'price':int(pizza_info[2])}

    # 電話する
    kind_list = [pizza_dict[kind]['name'] for kind in args.kind]
    #call(name=name, tel=tel, dlt=dlt, kind_list=kind_list, size_list=args.size,
    #     num_list=args.num)

    charge = 0
    for i, kind in enumerate(args.kind):
        charge += pizza_dict[kind]['price'] * args.num[i]
    print math.ceil((charge + 500) * 1.05)

if __name__ == '__main__':
    main()
