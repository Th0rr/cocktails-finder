import configparser as cp
import itertools


def remove_double(lst):
	aa = []
	for s in lst:
		for i in lst:
			if i not in aa:
				aa.append(i)
	return aa


def get_key(val,dic): 
	for key, value in dic.items(): 
		 if set(val) == set(value): 
			 return key 
	return "cocktail doesn't exist"


#take tuple and find name
def find_cocktail_name(val):
	for key, value in cocktails_list_dic.items(): 
		if set(val) == set(value): 
			return key 







