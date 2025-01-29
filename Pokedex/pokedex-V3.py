import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import requests
import os

# Constants
USER_DATA_FILE = "UserData.csv"
POKEMON_LIMIT = 6

# Ensure the CSV file exists with the correct columns
if not os.path.exists(USER_DATA_FILE):
    columns = ["Username", "Password"]
    
    # Add columns for each Pokémon slot (Poké1 to Poké6) with Name, ID, and Types
    for i in range(1, POKEMON_LIMIT + 1):
        columns += [f"Poké{i}_Name", f"Poké{i}_ID", f"Poké{i}_Types"]
    
    # Create the initial dataframe with empty values for Pokémon slots
    initial_data = {
        "Username": [],
        "Password": [],
    }
    
    # Adding empty slots for each Pokémon
    for i in range(1, POKEMON_LIMIT + 1):
        initial_data[f"Poké{i}_Name"] = []
        initial_data[f"Poké{i}_ID"] = []
        initial_data[f"Poké{i}_Types"] = []
    
    # Create the DataFrame and save it to CSV
    pd.DataFrame(initial_data, columns=columns).to_csv(USER_DATA_FILE, index=False)

# Global variables
user_data = pd.read_csv(USER_DATA_FILE)
current_user = None

# Save user data
def save_user_data():
    global user_data
    user_data.to_csv(USER_DATA_FILE, index=False)

# Fetch Pokémon data from PokéAPI
def fetch_pokemon_data(query):
    url = f"https://pokeapi.co/api/v2/pokemon/{query.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": data["sprites"]["front_default"],
            "artwork": data["sprites"]["other"]["official-artwork"]["front_default"]
        }
    return None

# Register a new user
def register():
    global user_data
    username = entry_username.get()
    password = entry_password.get()

    # Define columns inside the register function
    columns = ["Username", "Password"]
    for i in range(1, POKEMON_LIMIT + 1):
        columns += [f"Poké{i}_Name", f"Poké{i}_ID", f"Poké{i}_Types"]

    # Check if username already exists
    if username in user_data["Username"].values:
        messagebox.showerror("Error", "Username already exists.")
        return

    # Create a new user row with the correct number of columns
    new_user = pd.DataFrame([[username, password] + [None] * (POKEMON_LIMIT * 3)], columns=columns)

    # Append the new user to the existing data and save
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    save_user_data()

    messagebox.showinfo("Success", "Account created successfully!")

# Login functionality
def login():
    global current_user, user_data
    username = entry_username.get()
    password = entry_password.get()

    user_row = user_data[(user_data["Username"] == username) & (user_data["Password"] == password)]
    if not user_row.empty:
        current_user = username
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        
        # Hide the login frame and show the main menu
        login_frame.pack_forget()  # Hides the login frame
        menu_frame.pack()  # Shows the menu frame
        
        update_party_display()  # Update the Pokémon party display
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Update the Pokémon party display
def update_party_display():
    global user_data, current_user
    if current_user:
        user_row = user_data[user_data["Username"] == current_user]
        
        party_listbox.delete(0, tk.END)
        for i in range(POKEMON_LIMIT):
            name = user_row.iloc[0, 2 + i * 3]
            pokemon_id = user_row.iloc[0, 3 + i * 3]
            types = user_row.iloc[0, 4 + i * 3]
            if pd.notna(name):
                party_listbox.insert(
                    i,
                    f"{name} (ID: {pokemon_id}) - Types: {types}"
                )
            else:
                party_listbox.insert(i, "Empty Slot")

# Function to add a Pokémon to the user's team
def add_pokemon():
    global user_data, current_user
    # Prompt the user to enter the Pokémon name or ID
    pokemon_input = simpledialog.askstring("Add Pokémon", "Enter the name or ID of the Pokémon to add:")
    
    if pokemon_input:
        # Fetch Pokémon data from PokéAPI
        pokemon_data = fetch_pokemon_data(pokemon_input)
        
        if pokemon_data:
            # If valid Pokémon data is found, add it to the user's team
            pokemon_name = pokemon_data["name"]
            pokemon_id = pokemon_data["id"]
            types = ", ".join(pokemon_data["types"])

            # Check all 6 Pokémon slots to find the first available empty slot (None value)
            for i in range(1, POKEMON_LIMIT + 1):
                # Check if the slot is empty (None value)
                if pd.isna(user_data.loc[user_data["Username"] == current_user, f"Poké{i}_Name"]).iloc[0]:
                    # Found an empty slot, add the new Pokémon
                    user_data.loc[user_data["Username"] == current_user, f"Poké{i}_Name"] = pokemon_name
                    user_data.loc[user_data["Username"] == current_user, f"Poké{i}_ID"] = pokemon_id
                    user_data.loc[user_data["Username"] == current_user, f"Poké{i}_Types"] = types
                    messagebox.showinfo("Success", f"{pokemon_name} added to your team!")
                    break
            else:
                # If all slots are full, ask the user which Pokémon to replace
                replace_pokemon = simpledialog.askstring("Replace Pokémon", "Your party is full. Which Pokémon would you like to replace (1-6)?")
                try:
                    replace_slot = int(replace_pokemon)
                    if 1 <= replace_slot <= POKEMON_LIMIT:
                        # Replace the chosen Pokémon
                        user_data.loc[user_data["Username"] == current_user, f"Poké{replace_slot}_Name"] = pokemon_name
                        user_data.loc[user_data["Username"] == current_user, f"Poké{replace_slot}_ID"] = pokemon_id
                        user_data.loc[user_data["Username"] == current_user, f"Poké{replace_slot}_Types"] = types
                        messagebox.showinfo("Success", f"{pokemon_name} replaced the old Pokémon in slot {replace_slot}.")
                    else:
                        messagebox.showerror("Error", "Invalid slot number! Please choose a slot between 1 and 6.")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid slot number (1-6).")
            
            # Save the updated user data to the CSV
            save_user_data()
            
            # Update the party display to reflect changes
            update_party_display()
        else:
            messagebox.showerror("Error", "Pokémon not found. Please enter a valid Pokémon name or ID.")

# Main application window
app = tk.Tk()
app.title("Pokemon Team Builder")

# Login/Register Window
login_frame = tk.Frame(app)
tk.Label(login_frame, font=('Helvetica bold', 16), text="Username:").grid(row=0, column=0, padx=5, pady=15, )
entry_username = tk.Entry(login_frame)
entry_username.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_frame, font=('Helvetica bold', 16), text="Password:").grid(row=1, column=0, padx=5, pady=10)
entry_password = tk.Entry(login_frame, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

tk.Button(login_frame, font=('Comfortaa', 10), text="Login", command=login).grid(row=3, column=0, padx=10, pady=5)
tk.Button(login_frame, font=('Comfortaa', 10), text="Register", command=register).grid(row=3, column=1, padx=5, pady=5)

# Menu Frame
menu_frame = tk.Frame(app)
tk.Label(menu_frame, height=3, width=40, font=('comfortaa', 14), text="Your Pokemon Party:").pack(padx=5, pady=3)
party_listbox = tk.Listbox(menu_frame, font=('comfortaa', 11), height=POKEMON_LIMIT, width=80)
party_listbox.pack(padx=10, pady=5)

tk.Button(menu_frame, font=('Helvetica bold', 14), text="Add Pokémon", command=add_pokemon).pack(padx=5, pady=3)

# Start with Login Window
login_frame.pack()

# Start the Tkinter loop
app.mainloop()
