import configparser as cp
import itertools
import webbrowser
import fileinput
import sys
import argparse
from drinks import *
from Data import *

# ----------------- COMBINATION ------------------------
def find_combination(cocktail_list,combination):
	cocktails = []
	for name,ingredients in cocktail_list.items():
		if set(tuple([ingredients])).issubset(combination):
			cocktails.append(name)

	cocktails = remove_double(cocktails)
	cocktails.append(combination)
	cocktails.append(len(cocktails)-1)
	return cocktails


def find_best_combinations(combinations):
	m = 0
	save = []
	for c in combinations:
		if c[-1] > m:
			m = c[-1]
			save.clear()
			save.append(c[-1]) # max number of comb reached
			save.append(c[-2]) # actual combination
		elif c[-1] == m:
			save.append(c[-2])
	return save


def get_combination_infos(single_combination):
	ingredients = {}
	cocktails = {}
	infos = []

	for ingredient,price in dict_ingredients.items():
		if ingredient in single_combination:
			ingredients.update({ingredient:price})
	infos.append(ingredients)


	for name,ingredients in cocktails_list_dic.items():
		if ingredients in single_combination:
			cocktails.update({name:ingredients})
	infos.append(cocktails)

	return infos



# ------------------------- DISPLAY -----------------------
def print_infos(best_combinations):
	cocktail_number = best_combinations[0]
	del best_combinations[0]

	best_combinations= sort_by_price(best_combinations)
	
	print("------------- "+str(len(best_combinations))+" COMBINATIONS FOUND-----------")
	print("--- FOLLOWING COMBINATIONS ALLOWS FOR",cocktail_number,"COCKTAILS---")
	for b in best_combinations:
		print_element(get_combination_infos(b))


# add total cost at the end of tuple then sort the list of tuple
def sort_by_price(best_combinations):
	sort = []
	tuplex = ()
	for e in best_combinations:
		dic = get_combination_infos(e)
		price = (' '.join(['{1}'.format(k, v) for k,v in dic[0].items()])).split(" ") # extract price of ingredients
		price = (str(sum([int(i) for i in price if type(i) == type("a")])) ) #sum them to get total price of combination
		tuplex = e+(price,)
		sort.append(tuplex)
	sort = sorted(sort, key=lambda x: x[-1],reverse=False)
	return sort



def print_element(e):
	product_infos = ' '.join(['{0} {1}€'.format(k, v) for k,v in e[0].items()])
	price = (' '.join(['{1}'.format(k, v) for k,v in e[0].items()])).split(" ") # extract price of ingredients
	price = str(sum([int(i) for i in price if type(i) == type("a")])) #sum them to get total price of combination

	print("\n----------- COMBINATION FOUND ! ",price,"€ -----------\n",product_infos )
	print("\n----------- LIST OF COCKTAILS AVAILABLE---------")
	for c,k in e[1].items():
		print(c)
		print("Key ingredients: ",k,"\n")


def create_html(best_combinations,filename):

	f = open(filename,'w')
	cocktail_number = best_combinations[0]
	del best_combinations[0]
	best_combinations= sort_by_price(best_combinations)
	f.write("<html>")
	f.write("""<link rel="stylesheet" type="text/css" href="style.css">""")
	f.write("<h2 class ='title'>------------- {0} COMBINATIONS FOUND-----------</h2>\n".format(str(len(best_combinations) )))
	f.write("<h3 class = 'title'>--- FOLLOWING COMBINATIONS ALLOWS FOR {0} COCKTAILS---</h3><br><br>\n\n".format(cocktail_number))
	f.write("<h4 class = 'title'>BUDGET {0} €</h4><br><br>\n\n".format(budget))
	count = 0
	f.write("<body>")
	for b in best_combinations:
		if int(get_combination_price(get_combination_infos(b))) <= budget:
			write_element(get_combination_infos(b),f,"green")
		else:
			count+=1
			write_element(get_combination_infos(b),f,"red")

	f.write("</body>")
	f.write("</html>")
	f.close()
	if count == len(best_combinations):
		return False
	else : 
		return True

def write_element(e,f,color):

		product_infos = ' '.join(['{0} {1}€'.format(k, v) for k,v in e[0].items()])
		price = (' '.join(['{1}'.format(k, v) for k,v in e[0].items()])).split(" ") # extract price of ingredients
		price = sum([int(i) for i in price if type(i) == type("a")]) #sum them to get total price of combination

		f.write("<p class = 'title' style='color:{0}'><br>\n----------- COMBINATION FOUND ! {1} € -----------</p><br>\n".format(color,price))
		f.write("{0}<br>\n".format(product_infos))
		f.write("<p class = 'title' style='color:{0}'><br>\n----------- LIST OF COCKTAILS AVAILABLE---------</p>".format(color))

		for c,k in e[1].items():
			f.write("\n<p class = 'cocktail_name'>Nom : {0}<br></p>\n".format(c))
			f.write("Key ingredients: {0}<br>\n".format(k))


def get_combination_price(e):
	price = (' '.join(['{1}'.format(k, v) for k,v in e[0].items()])).split(" ") # extract price of ingredients
	price = str(sum([int(i) for i in price if type(i) == type("a")])) #sum them to get total price of combination
	return price

def search(n,ingredients,cocktails_list):
	ingredients_combinations = list(itertools.combinations(ingredients,n))

	for combination in ingredients_combinations:
		all_comb.append(find_combination(cocktails_list,combination))
	print_infos(find_best_combinations(all_comb))
	create_html(find_best_combinations(all_comb),"view_combinations.html")
	webbrowser.open_new_tab('view_combinations.html')


def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


if __name__ == "__main__":
	
	#--------------------- LOADING DATA --------------------------
	config = cp.ConfigParser()
	config.read('cocktail_infos.ini')
	dict_ingredients = {}
	cocktails_list_dic = {}
		# format cocktail_name [key] => ingredient1 ingredient2 [value]
	cocktails_list_dic = dict(config.items('cocktails'))
	dict_ingredients = dict(config.items('key_ingredients'))

		# cocktail_name [key] => price [value]
	cocktails_prices = load_cocktails_prices(cocktails_list_dic,dict_ingredients)
	parser = argparse.ArgumentParser()

	parser.add_argument(
	'-b', '--budget',required=True, type=int, 
	help="budget in the currency of your choice (€ by default)")

	parser.add_argument(
	'-n', '--number',required=True, type=int, 
	help="Number of ingredients to buy")

	args = parser.parse_args()

	if args:
		budget = args.budget
		all_comb = []
		cocktail_list = []
		for value in cocktails_list_dic.values():
			cocktail_list.append(value.split(" "))

		search(args.number,dict_ingredients,cocktails_list_dic)
