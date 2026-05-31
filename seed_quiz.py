import os
import random
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Klap.settings"
)

django.setup()

from detection.models import Question


# =========================================
# CLEAR OLD QUESTIONS
# =========================================

Question.objects.all().delete()


# =========================================
# DATA
# =========================================

fruits = [

    "apple",
    "banana",
    "grapes",
    "mango",
    "orange",
    "pineapple",
    "pomegranate",
    "watermelon"

]

animals = [

    "buffalo",
    "cat",
    "cow",
    "dog",
    "elephant",
    "hen",
    "lion",
    "monkey",
    "tiger"

]

vegetables = [

    "potato",
    "tomato",
    "carrot",
    "onion",
    "brinjal",
    "cabbage",
    "cauliflower",
    "peas"

]


# =========================================
# IMAGE PATH HELPER
# =========================================

def get_image_path(name):

    if os.path.exists(
        f"media/quiz/{name}.jpg"
    ):

        return f"quiz/{name}.jpg"

    elif os.path.exists(
        f"media/quiz/{name}.png"
    ):

        return f"quiz/{name}.png"

    return None


# =========================================
# CATEGORY MAP
# =========================================

category_data = {

    "fruit": fruits,

    "animal": animals,

    "vegetable": vegetables

}


# =========================================
# TEXT QUESTIONS
# MIXED OPTIONS
# =========================================

for _ in range(40):

    category = random.choice([
        "fruit",
        "animal",
        "vegetable"
    ])


    # -------------------------
    # FRUIT
    # -------------------------

    if category == "fruit":

        correct = random.choice(fruits)

        wrong1 = random.choice(animals)

        wrong2 = random.choice(vegetables)

        q_text = "Which is a fruit?"


    # -------------------------
    # ANIMAL
    # -------------------------

    elif category == "animal":

        correct = random.choice(animals)

        wrong1 = random.choice(fruits)

        wrong2 = random.choice(vegetables)

        q_text = "Which is an animal?"


    # -------------------------
    # VEGETABLE
    # -------------------------

    else:

        correct = random.choice(vegetables)

        wrong1 = random.choice(fruits)

        wrong2 = random.choice(animals)

        q_text = "Which is a vegetable?"


    options = [
        correct,
        wrong1,
        wrong2
    ]

    random.shuffle(options)

    Question.objects.create(

        question_type="text",

        question_text=q_text,

        correct_answer=correct.capitalize(),

        option1=options[0].capitalize(),

        option2=options[1].capitalize(),

        option3=options[2].capitalize(),

        category=category
    )


# =========================================
# IMAGE QUESTIONS
# SAME CATEGORY OPTIONS
# =========================================

for _ in range(30):

    category = random.choice([
        "fruit",
        "animal",
        "vegetable"
    ])

    items = category_data[category]

    item = random.choice(items)

    wrong = random.sample(
        [x for x in items if x != item],
        2
    )

    options = [item] + wrong

    random.shuffle(options)

    Question.objects.create(

        question_type="image_question",

        question_text="What is this?",

        correct_answer=item.capitalize(),

        option1=options[0].capitalize(),

        option2=options[1].capitalize(),

        option3=options[2].capitalize(),

        image=get_image_path(item),

        category=category
    )


# =========================================
# IMAGE OPTION QUESTIONS
# SAME CATEGORY OPTIONS
# =========================================

for _ in range(30):

    category = random.choice([
        "fruit",
        "animal",
        "vegetable"
    ])

    items = category_data[category]

    item = random.choice(items)

    wrong = random.sample(
        [x for x in items if x != item],
        2
    )

    options = [item] + wrong

    random.shuffle(options)

    Question.objects.create(

        question_type="image_option",

        question_text=f"Select the image of {item.capitalize()}",

        correct_answer=item.capitalize(),

        option1=options[0].capitalize(),

        option2=options[1].capitalize(),

        option3=options[2].capitalize(),

        option1_image=get_image_path(options[0]),

        option2_image=get_image_path(options[1]),

        option3_image=get_image_path(options[2]),

        category=category
    )


print("✅ 100 CLEAN Questions Added Successfully!")