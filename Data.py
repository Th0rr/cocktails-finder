import configparser as cp
import itertools


def calc_cocktail_price(name,ingredients,dict_ingredients):
	price_sum = 0
	for ingredient,price in dict_ingredients.items():
		if ingredient in ingredients:
			price_sum+=int(price)
	return {name:price_sum}

def load_cocktails_prices(cocktails,dict_ingredients):
	prices = {}
	add = 0
	for name,cocktail_ingredients in cocktails.items():
		prices.update(calc_cocktail_price(name,cocktail_ingredients,dict_ingredients))
	return prices

