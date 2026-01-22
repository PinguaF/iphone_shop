import sqlite3

class Product:
    def __init__(self, id, category):
        self.id = id
        self.category = category
        with sqlite3.connect("data\catalog\catalog.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT * FROM `{category}` WHERE `id` == {id};""")
            llist = cursor.fetchall()[0]
            if category == 'iphone':
                self.availability = llist[1]
                self.line = llist[2]
                self.color = llist[3]
                self.memory = llist[4]
                self.price = llist[5]
                self.photo = llist[6]
        
    def get_version(self):
        with sqlite3.connect("data\catalog\catalog.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT `color` FROM `{self.category}` WHERE `line` == '{self.line}';""")
            colors = convert_to_set(cursor.fetchall())
            cursor.execute(f"""SELECT `memory` FROM `{self.category}` WHERE `line` == '{self.line}';""")
            memorys = convert_to_set(cursor.fetchall())
            return colors, memorys


def get_all_category(category):
    with sqlite3.connect("data\catalog\catalog.db") as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT * FROM `{category}` ORDER BY `id` DESC;""")
        llist = cursor.fetchall()
        return llist
    

def get_id_for_product(category, line, color, memory):
    with sqlite3.connect("data\catalog\catalog.db") as db:
        cursor = db.cursor()
        if category == 'iphone':
            cursor.execute(f"""SELECT `id` FROM `{category}` WHERE `line`='{line}' and `color`='{color}' and `memory`='{memory}';""")
        else:
            raise ValueError(f"Неверная категория продута: {category}")
        id = cursor.fetchall()[0][0]
        return id

def transform_order(order):
    result = dict()
    order_price = 0
    for cat in order:
        if order[cat]:
            result[cat] = {}
        for id in order[cat]:
            product = Product(id, cat)
            end_price = round(int(order[cat][id]['count'])*float(product.price.replace(' ', '')), 2)
            order_price += end_price
            if cat == "iphone":
                result['iphone'][id] = {'count': order[cat][id]['count'], 'line':product.line, 
                                        'color':product.color, 'memory':product.memory,
                                        'price':product.price, 'end_price':end_price,
                                        'photo':product.photo}
    return result, round(order_price, 2)

def convert_to_set(parametr_tuple):
    result = list()
    for i in parametr_tuple:
        result.append(i[0])
    return set(result)
