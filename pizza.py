# -*- coding:utf-8 -*-

import argparse, math, sys,re

def main():
    parser = argparse.ArgumentParser(description='Let\'s order pizza!')

    parser.add_argument('-k', '--kind', type=int, choices=xrange(1,27),
                        dest='kind', default=3, nargs='+', help='kind of pizza')
    parser.add_argument('-s', '--size', type=int, choices=[35, 45], dest='size',
                        default=45, nargs='+', help='size of pizza')
    parser.add_argument('-n', '--num', type=int, dest='num', default='1',
                        nargs='+', help='number of pizza')

    args = parser.parse_args()
    """
    if not (len(args.kind) == len(args.size) == len(args.num)):
        print 'Error: You have to equalize num of arguments(k, s, and n).'
        sys.exit()
    """ 
    contact_dict = {}
    contact_number = -1
    for line in open('.pizza.conf','r'):
        if not line.rstrip().strip():
            continue
        
        if line.rstrip() == 'contact:':
            contact_number += 1
            contact_dict[contact_number] = {}
     
        contact_dict[contact_number][line.rstrip().split(':')[0].strip()] =  line.rstrip().split(':')[1].strip()
    
    #validate contact
    for i in range (contact_number + 1):
        phone_pattern = re.compile(r'^(\d{3})(-)?(\d{3,4})(-)?(\d{4})$')
        if not(phone_pattern.match(contact_dict[i]['tel'])):
            print 'Error: Invalid Phone Number '
            sys.exit()


        if not ( 30 <= int(contact_dict[i]['delivery_limit_time']) <= 60 ):
            print "Error: delibery_limit_time must be between 30 and 60"
            sys.exit()

        regexp = re.compile(r'^(?:\xE3\x81[\x81-\xBF]|\xE3\x82[\x80-\x93])+$')
        result = regexp.search(contact_dict[i]['name'])
        if result == None :
            print 'Error: name must be full-width hiragana' 
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
