import csv
import re

MENU_FILES = ["data/menus_week_1.csv", "data/menus_week_2.csv"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEALS = ["Breakfast", "Lunch", "Dinner"]
MORGAN = "Morgan Dining Hall"

TOP_9_ALLERGENS = {
    "milk": ["milk", "cheese", "butter", "buttermilk", "cream", "yogurt", "whey", "casein", "parmesan", "mozzarella",
             "cheddar", "ricotta", "crema", "tzatziki"],
    "eggs": ["egg", "eggs", "mayonnaise", "mayo"],
    "fish": ["fish", "salmon", "tuna", "cod", "tilapia", "pollock", "haddock", "anchovy", "anchovies"],
    "shellfish": ["shellfish", "shrimp", "crab", "lobster", "clam", "clams", "scallop", "scallops", "mussel",
                  "mussels"],
    "tree nuts": ["almond", "almonds", "walnut", "walnuts", "cashew", "cashews", "pecan", "pecans", "pistachio",
                  "pistachios", "hazelnut", "hazelnuts"],
    "peanuts": ["peanut", "peanuts"],
    "wheat": ["wheat", "flour", "bread", "breadcrumbs", "pasta", "couscous", "noodles", "linguine", "macaroni",
              "tortilla", "pita", "bun"],
    "soy": ["soy", "soybean", "soybeans", "tofu", "edamame"],
    "sesame": ["sesame", "tahini"],
}


# This class is one item on the menu for one meal on one day
class MenuItem:

    # This method keeps the columns of the item's row that the planner uses
    def __init__(self, number, row):
        self.number = number
        self.date = row["date"]
        self.day = row["day"]
        self.meal = row["meal"]
        self.location = row["location"]
        self.station = row["station"]
        self.name = row["item"]
        self.type = row["type"]
        self.portion = row["portion"]
        self.calories = float(row["calories"])
        self.protein = float(row["protein_g"])
        self.ingredients = row["ingredients"]
        self.icons = row["icons"].split(";")
        self.allergens = find_allergens(self.ingredients)


# This function returns the Top 9 allergens found in an ingredient list
def find_allergens(ingredients):
    words = re.split("[^a-z]+", ingredients.lower())
    found = []
    for allergen in TOP_9_ALLERGENS:
        for keyword in TOP_9_ALLERGENS[allergen]:
            if keyword in words:
                found.append(allergen)
                break
    return found


# This function reads one week of menus into a list of MenuItem objects
def load_menus(file_name):
    items = []
    with open(file_name, newline="", encoding="utf-8") as menu_file:
        for row in csv.DictReader(menu_file):
            items.append(MenuItem(len(items), row))
    return items
