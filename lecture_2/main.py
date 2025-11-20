def generate_profile(age: int) -> str:
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"


# 1. User info
user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")

birth_year = int(birth_year_str)
current_age = 2025 - birth_year

# 2. Collect hobbies
hobbies = []

while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ").strip().lower()
    if hobby == "stop":
        break
    hobbies.append(hobby)

# 3. Determine life stage
life_stage = generate_profile(current_age)

# 4. Build profile dictionary
user_profile = {
    "name": user_name,
    "age": current_age,
    "life_stage": life_stage,
    "hobbies": hobbies,
}

# 5. Display result
print("\n\nProfile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['life_stage']}")

if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for h in hobbies:
        print(f"- {h}")
