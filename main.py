def p_ingredient(s):
    name,quantity,measure= s.split(' | ')
    return{'ingredient_name': name.strip(), 'quantity': int(quantity.strip()),'measure': measure.strip()}



def r_cook_book(path):
    cook_book={}

    with open('text.txt','r',encoding='UTF-8') as f:
        for line in f:
            dish_name=line.strip()
            if not dish_name:
                continue
            ingredient_count=int(f.readline().strip())
            ingredient_list=[]
            for i in range(ingredient_count):
                line_ingr=f.readline().strip()
                dict_ingr=p_ingredient(line_ingr)
                ingredient_list.append(dict_ingr)
            cook_book[dish_name]= ingredient_list
    return cook_book

print (r_cook_book('text.txt'))

cook_book=r_cook_book('text.txt')

def get_shop_list_by_dishes(dishes,person_count):
    shop_list={}
    for dish in dishes:
        if dish in cook_book:
            ingredients=cook_book[dish]
            for ingredient in ingredients:
                name = ingredient['ingredient_name']
                measure = ingredient['measure']
                quantity = ingredient['quantity'] * person_count
                if name in shop_list:
                    shop_list[name]['quantity'] += quantity
                else:
                    shop_list[name]={'measure': measure, 'quantity': quantity}
    return shop_list
dishes=['Запеченный картофель', 'Омлет']
print(get_shop_list_by_dishes(dishes,2))