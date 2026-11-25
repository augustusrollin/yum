SWIPES_PER_WEEK = {"14 Meal Plan": 14, "14 Flex": 14, "19 Meal Plan": 19, "19 Flex": 19, "All Access": 19}
RETAIL_SWIPES_PER_WEEK = {"14 Meal Plan": 2, "14 Flex": 7, "19 Meal Plan": 2, "19 Flex": 9, "All Access": 19}
STARTING_ITEM_SCORE = 1
LIKED_WORD_POINTS = 2
DISLIKED_WORD_POINTS = -4
RATING_POINTS = {"Liked it": 2, "Not for me": -4, "Swap": -1}
STATION_RATING_POINTS = {"Liked it": 1, "Not for me": -1, "Swap": 0}


# This class is everything the student tells the planner about themselves
class StudentProfile:

    # This method keeps the goals, the rules and the likes of one student
    def __init__(self, calorie_goal, protein_goal, allergies, diet, liked_words, disliked_words, meal_plan,
                 campus_meals):
        self.calorie_goal = calorie_goal
        self.protein_goal = protein_goal
        self.allergies = allergies
        self.diet = diet
        self.liked_words = liked_words
        self.disliked_words = disliked_words
        self.meal_plan = meal_plan
        self.campus_meals = campus_meals
        self.item_ratings = {}
        self.station_ratings = {}
        self.swapped_items = []

    # This method returns the swipes the student has each week
    def get_swipes(self):
        return SWIPES_PER_WEEK[self.meal_plan]

    # This method returns the retail swipes the student has each week
    def get_retail_swipes(self):
        return RETAIL_SWIPES_PER_WEEK[self.meal_plan]


# This function tells whether the student can eat an item
def item_is_allowed(item, student):
    for allergen in item.allergens:
        if allergen in student.allergies:
            return False
    if student.diet == "vegan" and "vegan" not in item.icons:
        return False
    if student.diet == "vegetarian" and "vegetarian" not in item.icons and "vegan" not in item.icons:
        return False
    return True


# This function returns how much the student likes one item
def get_item_score(item, student):
    score = STARTING_ITEM_SCORE
    name = item.name.lower()
    for word in student.liked_words:
        if word.lower() in name:
            score = score + LIKED_WORD_POINTS
    for word in student.disliked_words:
        if word.lower() in name:
            score = score + DISLIKED_WORD_POINTS
    if item.name in student.item_ratings:
        score = score + student.item_ratings[item.name]
    if item.station in student.station_ratings:
        score = score + student.station_ratings[item.station]
    return score


# This function changes the scores of an item and its station after a rating
def update_likes(student, item, rating):
    if rating not in RATING_POINTS:
        return -1
    if item.name not in student.item_ratings:
        student.item_ratings[item.name] = 0
    student.item_ratings[item.name] = student.item_ratings[item.name] + RATING_POINTS[rating]
    if item.station not in student.station_ratings:
        student.station_ratings[item.station] = 0
    student.station_ratings[item.station] = student.station_ratings[item.station] + STATION_RATING_POINTS[rating]
    if rating == "Swap":
        student.swapped_items.append(item.number)
    return student.item_ratings[item.name]
