import os
import django
import random
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobbox.settings")  # Use your actual settings module
django.setup()

from accounts.models import CustomUser, WorkerProfile, ShopOrIndividualProfile

in_names = [
    "Abhishek", "Nilesh", "Deepanshu", "Virat", "Ritvik",
    "Samar", "Ishan", "Reyansh", "Aditya", "Yug",
    "Bhanu", "Ronav", "Eshan", "Aryan", "Divyansh",
    "Aarav", "Pranay", "Atharv", "Darsh", "Rudra",
    "Aarush", "Shaurya", "Vivaan", "Neel", "Lakshay",
    "Dhruv", "Tanish", "Arnav", "Veer", "Ayaan",
    "Krishna", "Harveer", "Agastya", "Manan", "Hriday",
    "Tej", "Vedant", "Anvay", "Ritayan", "Aadhav",
    "Siddhanth", "Riaan", "Aakesh", "Devraj", "Hrithik",
    "Ronavdeep", "Moksh", "Vyan", "Aarohan", "Prithvi"
]

name_dict = {
    "Bhavesh": "bhavesh",
    "Alok": "alok",
    "Rajiv": "rajiv",
    "Rakesh": "rakesh",
    "Kishore": "kishore",
    "Tejas": "tejas",
    "Vinay": "vinay",
    "Mukul": "mukul",
    "Parth": "parth",
    "Rajat": "rajat",
    "Anup": "anup",
    "Jatin": "jatin",
    "Sagar": "sagar",
    "Hemendra": "hemendra",
    "Lalit": "lalit",
    "Keshav": "keshav",
    "Sharvan": "sharvan",
    "Inder": "inder",
    "Harsh": "harsh",
    "Madhav": "madhav",
    "Siddhant": "siddhant",
    "Omkar": "omkar",
    "Ashwin": "ashwin",
    "Aniket": "aniket",
    "Nirav": "nirav",
    "Ritwik": "ritwik",
    "Mayank": "mayank",
    "Tushar": "tushar",
    "Abhinav": "abhinav",
    "Devansh": "devansh",
    "Bhaskar": "bhaskar",
    "Satyam": "satyam",
    "Chandan": "chandan",
    "Tanmay": "tanmay",
    "Kamal": "kamal",
    "Harshit": "harshit",
    "Pranav": "pranav",
    "Raghav": "raghav",
    "Sameer": "sameer",
    "Ramesh": "ramesh",
    "Kiran": "kiran",
    "Nandan": "nandan",
    "Suraj": "suraj",
    "Lokesh": "lokesh",
    "Avinash": "avinash",
    "Anshuman": "anshuman",
    "Umesh": "umesh",
    "Rajendra": "rajendra",
    
    # 50 more names added below
    "Yash": "yash",
    "Aman": "aman",
    "Arjun": "arjun",
    "Rahul": "rahul",
    "Deepak": "deepak",
    "Nikhil": "nikhil",
    "Varun": "varun",
    "Gaurav": "gaurav",
    "Sandeep": "sandeep",
    "Ajay": "ajay",
    "Amit": "amit",
    "Pawan": "pawan",
    "Vivek": "vivek",
    "Kunal": "kunal",
    "Manoj": "manoj",
    "Prashant": "prashant",
    "Sourav": "sourav",
    "Tarun": "tarun",
    "Vikas": "vikas",
    "Dinesh": "dinesh",
    "Naveen": "naveen",
    "Sanjay": "sanjay",
    "Arvind": "arvind",
    "Hemant": "hemant",
    "Naresh": "naresh",
    "Mahesh": "mahesh",
    "Sharad": "sharad",
    "Balaji": "balaji",
    "Suhas": "suhas",
    "Anil": "anil",
    "Jayant": "jayant",
    "Yuvraj": "yuvraj",
    "Karthik": "karthik",
    "Chirag": "chirag",
    "Dev": "dev",
    "Uday": "uday",
    "Ravi": "ravi",
    "Prem": "prem",
    "Saurabh": "saurabh",
    "Tarak": "tarak",
    "Harendra": "harendra",
    "Vikram": "vikram",
    "Rohit": "rohit",
    "Lakshya": "lakshya",
    "Ishaan": "ishaan",
    "Ketan": "ketan",
    "Hardik": "hardik",
    "Mihir": "mihir",
    "Bhavya": "bhavya",
}



worker_names = [
    "Bhavesh", "Alok", "Rajiv", "Rakesh", "Kishore", "Tejas", "Vinay", "Mukul", "Parth", "Rajat",
    "Anup", "Jatin", "Sagar", "Hemendra", "Lalit", "Keshav", "Sharvan", "Inder", "Harsh", "Madhav",
    "Siddhant", "Rajat", "Omkar", "Ashwin", "Aniket", "Nirav", "Ritwik", "Mayank", "Tushar", "Abhinav",
    "Devansh", "Bhaskar", "Satyam", "Chandan", "Naveen", "Tanmay", "Kamal", "Harshit", "Pranav", "Raghav",
    "Sameer", "Ramesh", "Kiran", "Nandan", "Suraj", "Lokesh", "Avinash", "Anshuman", "Umesh", "Rajendra"
]


owner_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Rohan", "Krishna", "Sai", "Ishaan", "Kunal",
    "Rahul", "Amit", "Abhishek", "Siddharth", "Deepak", "Manish", "Ravi", "Ajay", "Varun", "Anil",
    "Vikram", "Gaurav", "Sunil", "Rajesh", "Dinesh", "Ashok", "Harish", "Suresh", "Naveen", "Pankaj",
    "Sanjay", "Prem", "Karthik", "Pradeep", "Nitin", "Yash", "Jayant", "Uday", "Chirag", "Balaji",
    "Nikhil", "Tarun", "Arvind", "Amar", "Dev", "Mahesh", "Surya", "Hemant", "Naresh", "Sharad"
]


categorized_shop_names = {
    "Food/Beverages": [
        "Tasty Treats Café", "Brew & Bite", "The Spice Market", "Urban Bakes", "Fresh Squeeze Juice Bar",
        "The Hungry Fork", "Flavors of India", "Choco Bliss Bakery", "The Daily Grind Café", "Taste Corner"
    ],
    "Electrical/Electronics": [
        "ElectroZone", "Gadget Galaxy", "SparkTech Electronics", "Watt & Wire", "BrightVolt",
        "TechNest Solutions", "Home Circuit Hub", "The LED Store", "VoltEdge Electronics", "Smart Living Systems"
    ],
    "Grocery": [
        "Green Basket", "FreshMart", "Daily Essentials", "Nature's Cart", "Family Grocers",
        "Harvest & Pantry", "Budget Basket", "Farm2Home", "Quick Pick Grocers", "Urban Harvest Market"
    ],
    "Clothing/Textiles": [
        "Style Street", "The Fabric Loft", "Trendy Threads", "Elegance Wardrobe", "Cotton & Co.",
        "Urban Vogue", "Royal Stitches", "The Style Studio", "Fashion Den", "Silk & Stitch"
    ],
    "Automobile/Workshop": [
        "GearUp Garage", "AutoFix Solutions", "Torque Motors", "RapidRide Workshop", "DriveSafe Auto Care",
        "PitStop Garage", "WheelWorks", "MotorMate Repairs", "SpeedZone Garage", "Precision Auto Works"
    ],
    "Construction": [
        "Brick & Beam Builders", "UrbanNest Constructions", "Solid Foundations", "Skyline InfraWorks", "Concrete Vision",
        "NextGen Builders", "DreamCraft Constructions", "SteelBrick Projects", "PrimeBuild Associates", "Stronghold Infra"
    ]
}
def generate_username(shop_name):
    return re.sub(r'[^a-zA-Z0-9]', '', shop_name).lower()

# Track used shop names to avoid duplicates
used_shop_names = set()
used_w_names = set()

locations = ["Thodupuzha", "Muvattupuzha", "Kothamangalam", "Palai", "Kochi", "Thrissur", "Kozhikode", "Kollam"]

# Sample Shop Categories
shop_categories = ["Food/Beverages", "Electrical/Electronics", "Grocery", "Clothing/Textiles", "Automobile/Workshop", "Construction"]

# Sample Worker Professions (Matching Shop Categories)
worker_professions = {
    "Food/Beverages": ["Cook/Chef", "Waiter"],
    "Electrical/Electronics": ["Electrician", "Maintenance Worker"],
    "Grocery": ["Salesman","Accountant"],
    "Clothing/Textiles": ["Tailor", "Salesman"],
    "Automobile/Workshop": ["Mechanic", "Driver"],
    "Construction": ["Mason", "Construction Worker"],
}

# Sample Household Workers for Individuals
household_workers = ["Security Guard", "Maidservant", "Gardener", "Driver", "Baby Sitter"]

# --------------- Creating Shops ---------------
for i in range(50):
    while True:    
        category = random.choice(list(categorized_shop_names.keys()))
        shop_name=random.choice(categorized_shop_names[category])
        if shop_name not in used_shop_names:
            used_shop_names.add(shop_name)
            break
    username = generate_username(shop_name)
    location = random.choice(locations)
    shop_user = CustomUser.objects.create(
        username=username,
        email=f"{username}@gmail.com",
        contact_number=f"98765432{i}",
        location=location,
        user_type="shop",
        shop_name=shop_name,
        owner_name=random.choice(owner_names),
        category=category,
        description=f"This is {category} shop",
    )
    
    ShopOrIndividualProfile.objects.create(
        user=shop_user,
        user_type="shop",
        shop_name=shop_user.shop_name,
        owner_name=shop_user.owner_name,
        category=shop_user.category,
        description=shop_user.description,
        email=shop_user.email,
        contact_number=shop_user.contact_number,
        location=shop_user.location,
    )

print("✅ 50 Shops Added Successfully!")

# --------------- Creating Workers ---------------
for i in range(50):
    while True:    
        Name = random.choice(list(name_dict.keys()))
        base_username = name_dict[Name]
        username = f"{base_username}{random.randint(1000, 9999)}"
        if username not in used_w_names:
            used_w_names.add(username)
            break
    category = random.choice(shop_categories)
    profession = random.choice(worker_professions[category])
    location = random.choice(locations)

    worker_user = CustomUser.objects.create(
        username=username,
        email=f"{username}@gmail.com",
        contact_number=f"99988877{i}",
        location=location,
        user_type="worker",
        I_am_a=profession,
        experience_in_years=random.randint(1, 10),
    )

    WorkerProfile.objects.create(
        user=worker_user,
        Name=Name,
        I_am_a=profession,
        email=worker_user.email,
        contact_number=worker_user.contact_number,
        location=worker_user.location,
        experience_in_years=worker_user.experience_in_years,
    )

print("✅ 50 Workers Added Successfully!")

# --------------- Creating Individuals ---------------
for i in range(50):
    location = random.choice(locations)
    username = random.choice(in_names)
    individual_user = CustomUser.objects.create(
        username=f"{username}{i*13}",
        email=f"{username}{i*13}@jobbox.com",
        contact_number=f"77766655{i}",
        location=location,
        user_type="individual",
    )

    ShopOrIndividualProfile.objects.create(
        user=individual_user,
        user_type="individual",
        Name=username,
        email=individual_user.email,
        contact_number=individual_user.contact_number,
        location=individual_user.location,
    )

print("✅ 50 Individuals Added Successfully!")
