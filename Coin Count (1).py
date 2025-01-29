import os
import pandas as pd
import time
# Dictionary of Data (Values and Weight)
coin_data = {
    "£2": {"value": 20, "weight": 120.00},
    "£1": {"value": 20, "weight": 175.00},
    "50p": {"value": 10, "weight": 160.00},
    "20p": {"value": 10, "weight": 250.00},
    "10p": {"value": 5, "weight": 325.00},
    "5p": {"value": 5, "weight": 235.00},
    "2p": {"value": 1, "weight": 356.00},
    "1p": {"value": 1, "weight": 356.00},
}
# Volunteer data structure
volunteers = []

# Loading data from a file (If it exists)
def load_data(filename="CoinCount.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                name, bags_counted, bags_correct, total_value = line.strip().split(",")
                volunteers.append({
                    "name": name,
                    "bags_counted": int(bags_counted),
                    "bags_correct": int(bags_correct),
                    "total_value": float(total_value)
                })

# Function to save data to a file
def save_data(filename="CoinCount.txt"):
    with open(filename, "w") as file:
        for volunteer in volunteers:
            file.write(f"{volunteer['name']},{volunteer['bags_counted']},{volunteer['bags_correct']},{volunteer['total_value']}\n")

# Function to check the coin weight and return if it's correct
def check_weight(coin_type, bag_weight):
    expected_weight = coin_data[coin_type]["weight"]
    if bag_weight != expected_weight:
        correct_coins = round(bag_weight / expected_weight)
        return False, correct_coins
    return True, 0

# Main Program that Runs
def main():
    load_data()
# Main Menu
    while True:
        print("\nMenu:")
        print("1. Input Volenteer and Coin Details")
        print("2. Display total number of bags and total value")
        print("3. Display volunteer accuracy")
        print("4. Display Weights and Values of coins.")
        print("5. Save and exit")

        choice = input("Choose an option: ")

        if choice == "1":
            volunteer_name = input("Enter volunteer name: ")
            coin_type = input("Enter coin type (£2, £1, 50p, 20p, 10p, 5p, 2p, 1p): ")
            if coin_type not in coin_data:
                print("Invalid coin type.")
                continue

            try:
                bag_weight = float(input("Enter bag weight (g): "))
            except ValueError:
                print("Invalid weight.")
                continue

            correct, coins_needed = check_weight(coin_type, bag_weight)

            # Find volunteer
            volunteer = next((v for v in volunteers if v["name"] == volunteer_name), None)
            if not volunteer:
                volunteer = {"name": volunteer_name, "bags_counted": 0, "bags_correct": 0, "total_value": 0}
                volunteers.append(volunteer)
                
            volunteer["bags_counted"] += 1
            bag_value = coin_data[coin_type]["value"]
            volunteer["total_value"] += bag_value

            if correct:
                volunteer["bags_correct"] += 1
                print(f"Bag is correct. Added {bag_value} to total value.")
            else:
                print(f"Bag is incorrect. Add or remove {coins_needed} coins.")

        elif choice == "2":
            total_bags = sum(v["bags_counted"] for v in volunteers)
            total_value = sum(v["total_value"] for v in volunteers)
            print(f"Total number of bags: {total_bags}")
            print(f"Total value: £{total_value:.2f}")
            time.sleep(2)

        elif choice == "3":
            sorted_volunteers = sorted(volunteers, key=lambda v: (v["bags_counted"] > 0)
            and (v["bags_correct"] / v["bags_counted"]), reverse=True)

            print(f"{'Volunteer':<15}{'Bags Counted':<15}{'Accuracy (%)'}")

            for volunteer in sorted_volunteers:
                accuracy = (volunteer["bags_correct"] / volunteer["bags_counted"]) * 100 if volunteer["bags_counted"] > 0 else 0

                print(f"{volunteer['name']:<15}{volunteer['bags_counted']:<15}{accuracy:.2f}")

        elif choice == "4":
            dataCoin = {'Coins': ['£2','£1','50p','20p','10p','5p','2p','1p'],
                        'Values':['20','20','10','10','5','5','1','1'],
                        'Weights':['120.00', '175.00', '160.00','250.00','325.00','235.00','356.00','356.00'],
                        }
            df = pd.DataFrame(dataCoin)

            df2 = df.to_string(index=False)
            print(df2)
            time.sleep(2)

            continue

        elif choice == "5":
            save_data()
            print("Data saved. Exiting...")
            time.sleep(2)
            break

        else:
            print("Invalid option, please try again.")

# Run the program
if __name__ == "__main__":
    main()