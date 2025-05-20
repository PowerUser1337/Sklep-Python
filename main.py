import json

PRODUCTS_FILE = "products.json"
HISTORY_FILE = "history.json"

class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def to_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    @staticmethod
    def from_obj(data):
        return Product(
            data["id"],
            data["name"],
            data["price"],
            data["stock"]
        )

class History:
    def __init__(self, product):
        self.product = product

    def to_obj(self):
        return {
            "product": self.product
        }
    
    @staticmethod
    def from_obj(data):
        return History(data['product'])

def loadData(filename, cls):
    with open(filename, "r") as f:
        return [cls.from_obj(item) for item in json.load(f)]

def saveData(filename, data):
    with open(filename, "w") as f:
        json.dump([item.to_obj() for item in data], f, indent=2)

def findProduct(products, id):
    for p in products:
        if p.id == id:
            return p
    return None

def addProduct(products):
    try:
        id = input("ID produktu: ")
        if findProduct(products, id):
            print("Produkt o tym ID już istnieje.")
            return
        name = input("Nazwa produktu: ")
        price = float(input("Cena: "))
        stock = int(input("Stan magazynowy: "))
        products.append(Product(id, name, price, stock))
        print("Produkt dodany.")
    except Exception as e:
        print(f"Błąd: {e}")

def editProduct(products):
    id = input("ID produktu do edycji: ")
    p = findProduct(products, id)
    if not p:
        print("Nie znaleziono produktu.")
        return
    try:
        p.name = input(f"Nazwa ({p.name}): ") or p.name
        p.price = float(input(f"Cena ({p.price}): ") or p.price)
        p.stock = int(input(f"Stan magazynowy ({p.stock}): ") or p.stock)
        print("Produkt zaktualizowany.")
    except Exception as e:
        print(f"Błąd: {e}")

def deleteProduct(products):
    id = input("ID produktu do usunięcia: ")
    p = findProduct(products, id)
    if p:
        products.remove(p)
        print("Produkt usunięty.")
    else:
        print("Nie znaleziono produktu.")

def listProducts(products):
    if not products:
        print("Brak produktów.")
        return
    for p in products:
        print(f"{p.id}: {p.name}, cena: {p.price}, stan: {p.stock}")

def listAvailableProducts(products):
    available = [p for p in products if p.stock > 0]
    if not available:
        print("Brak dostępnych produktów.")
        return
    for p in available:
        print(f"{p.id}: {p.name}, cena: {p.price}, stan: {p.stock}")

def sellProduct(products, history):
    id = input("ID produktu do sprzedania: ")
    p = findProduct(products, id)
    if not p:
        print("Nie znaleziono produktu.")
    else:
        if not p.stock > 0:
            print("Brak w magazynie")
        else:
            p.stock -= 1
            history.append(History(p.name))
            print("Sprzedano")

def main():
    products = loadData(PRODUCTS_FILE, Product)
    history = loadData(HISTORY_FILE, History)

    menu = """
1. Dodaj produkt
2. Edytuj produkt
3. Usuń produkt
4. Wyświetl produkty
5. Lista dostępnych produktów.
6. Sprzedaj produkt.
7. Zapisz i zakończ
"""
    while True:
        print(menu)
        choice = input("Wybierz opcję: ")
        if choice == "1":
            addProduct(products)
        elif choice == "2":
            editProduct(products)
        elif choice == "3":
            deleteProduct(products)
        elif choice == "4":
            listProducts(products)
        elif choice == "5":
            listAvailableProducts(products)
        elif choice == "6":
            sellProduct(products, history)
        elif choice == "7":
            saveData(PRODUCTS_FILE, products)
            saveData(HISTORY_FILE, history)
            print("Dane zapisane. Do widzenia!")
            break
        else:
            print("Nieprawidłowa opcja.")

main()
