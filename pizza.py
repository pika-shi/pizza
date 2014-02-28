#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse, math, os, sys, re
from collections import defaultdict
from twilio_call import TwilioCall

def main():
    pizza_dict = get_pizza_dict()
    description = '*****Pizza*****\n'
    for k, v in pizza_dict.items():
        description += str(k) + ': ' + v['name'] + ' ￥' + str(v['price']) + '\n'

    args = parse(description)

    if args.interactive == True:
        flag = True

        while flag:
            print 'input pizza number(1-26)'
            args.kind.append(raw_input())
            print 'input size of pizza (35 or 45)'
            args.size.append(raw_input())
            print 'input number of pizza(1-)'
            args.num.append(raw_input())
            print 'Do you order another pizza?(y/n)'
            if raw_input() != 'y':
                flag = False

        print args.kind[0]
        print args.size
        for i in range(len(args.kind)):
            print 'Order' + str(i+1) + ':PizzaNumber ' + str(args.kind[i]) + ' SizeOfPizza '+ str(args.size[i]) + ' NumberOfPizza ' + str(args.num[i])

        print 'Are you sure this order?(y/n)'
        if raw_input() != 'y':
            sys.exit()

    if not (len(args.kind) == len(args.size) == len(args.num) != 0):
        print 'Error: You have to equalize num of arguments(k, s, and n).'
        sys.exit()

    contact_dict = get_contact_dict()

    validate_contact(contact_dict)
    """
    kind_list = [pizza_dict[kind]['name'] for kind in args.kind]
    TwilioCall().order_pizza({'name':contact_dict[0]['name'], 'tel':contact_dict[0]['tel'],
                              'dlt':contact_dict[0]['delivery_limit_time'],
                              'kind_list':kind_list, 'size_list':args.size, 'num_list':args.num})
    """

def get_pizza_dict():
    pizza_dict = {}
    with open("pizza_list.txt","r") as f:
        for l in f:
            pinfo = l.strip().split(',')
            pizza_dict[int(pinfo[0])] = {'name':pinfo[1], 'name_for_twillio':pinfo[2],
                                         'price':int(pinfo[3])}
    return pizza_dict

def parse(description):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description)

    parser.add_argument('-k', '--kind', type=int, choices=xrange(1,27),
                        dest='kind', default=[], nargs='+', help='kind of pizza')
    parser.add_argument('-s', '--size', type=int, choices=[35, 45], dest='size',
                        default=[], nargs='+', help='size of pizza')
    parser.add_argument('-n', '--num', type=int, dest='num', default=[],
                        nargs='+', help='number of pizza')
    parser.add_argument('-i','--interactive',dest='interactive',action='store_true', help='interactive order mode')

    return parser.parse_args()

def get_contact_dict():
    if not os.path.exists('./.pizza.conf'):
        with open('.pizza.conf', 'w') as f:
            f.write('contact:\n')
            print 'Input your phone number.'
            f.write('    tel: {0}\n'.format(raw_input()))
            print 'Input your name.'
            f.write('    name: {0}\n'.format(raw_input()))
            print 'Input delivery limit time.'
            f.write('    delivery_limit_time: {0}\n'.format(raw_input()))
    contact_dict, contact_num = defaultdict(dict), 0
    with open('.pizza.conf','r') as f:
        for l in f:
            if not l.strip(): contact_num += 1
            if l.strip() == 'contact:': continue
            else: contact_dict[contact_num][l.split(':')[0].strip()] = l.split(':')[1].strip()
    return contact_dict

def validate_contact(contact_dict):
    for v in contact_dict.itervalues():
        phone_pattern = re.compile(r'^(\d{3})(\d{3,4})(\d{4})$')
        if not(phone_pattern.match(v['tel'])):
            print 'Error: Invalid Phone Number.'
            sys.exit()

        if not ( 30 <= int(v['delivery_limit_time']) <= 60 ):
            print "Error: delivery_limit_time must be between 30 and 60"
            sys.exit()

        regexp = re.compile(r'^(?:\xE3\x81[\x81-\xBF]|\xE3\x82[\x80-\x93])+$')
        result = regexp.search(v['name'])
        if result == None:
            print 'Error: name must be full-width hiragana'
            sys.exit()

def calc_charge(pizza_dict, kinds, nums):
    charge = 0
    for i, kind in enumerate(kinds):
        charge += pizza_dict[kind]['price'] * nums[i]
    return math.ceil((charge + 500) * 1.05)

if __name__ == '__main__':
    main()
