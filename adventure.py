"""
    Saul Toribio
    2/13/25
    CSE012 Spring 2024: Week 4 Coding Assignment
    IDE: VSCode; Python: 3.12.7
"""

import random

def display_player_status(player_health):
    """
        Displays the player's current health.

        Args:
            player_health (int): The player's current health.
    """
    print(f"Your current health: {player_health}\n")

def handle_path_choice(player_health):
    """
        Randomly chooses a path for the player to walk down. Either a good or bad thing happens.

        Args:
            player_health (int): The player's current health.

        Returns:
            int: The updated player health after the path event.
    """
    path = random.choice(["left", "right"])
    if path == "left":
        print("You decided to walk on the left path.\n")
        print("You encounter a friendly gnome who heals you for 10 health points.\n")

        player_health += 10
        player_health = min(player_health, 100)
    else:
        print("You decided to walk on the right path.\n")
        print("You fall into a pit and lose 15 health points.\n")

        player_health -= 15
        if player_health <= 0:
            player_health = 0
            print("You are barely alive!\n")
    return player_health

def player_attack(monster_health):
    """
        Handles a player attacking a monster.

        Args:
            monster_health (int): The monster's current health.

        Returns:
            int: The updated monster health after the player attacks.
    """
    print("You strike the monster for 15 damage!\n")
    monster_health -= 15
    return monster_health

def monster_attack(player_health):
    """
        Handles a monster attacking a player, with a chance of hitting a crit.

        Args:
            player_health (int): The player's current health.

        Returns:
            int: The updated player health after the monster attacks.
    """
    if player_health > 0:
        if random.random() < 0.5:
            print("The monster lands a critical hit for 20 damage!\n")
            player_health -= 20
        else:
            print("The monster hits you for 10 damage!\n")
            player_health -= 10
    return player_health

def combat_encounter(player_health, monster_health, has_treasure):
    """
        Handles the player and monster fight.

        Args:
            player_health (int): The player's current health.
            monster_health (int): The monster's current health.
            has_treasure (bool): The monster either has or doesn't have treasure.

        Returns:
            bool: True if the monster had treasure, False otherwise.
    """
    while True:
        monster_health = player_attack(monster_health)
        display_player_status(player_health)

        if monster_health > 0:
            player_health = monster_attack(player_health)

        if player_health <= 0:
            print("Game Over!\n")
            return False

        if monster_health <= 0:
            print("You defeated the monster!\n")
            return has_treasure

def check_for_treasure(has_treasure):
    """
        Checks if has_treasure is True or False.

        Args:
            has_treasure (bool): The monster either has or doesn't have treasure.
    """
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """
        Adds a item to the user's inventory.
    """
    print(f"You found a {item} in the room.\n")
    inventory.append(item) # Use append() to add item to the inventory
    return inventory

def display_inventory(inventory):
    """
        Displays the user's inventory.
    """
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(inventory, 1):
            print(f"{i}. {item}")

def enter_dungeon(player_health, inventory, dungeon_rooms):
    """
        Handles the dungeon encounter.
    """
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room
        print(f"\n{room_description}")

        if item:
            inventory = acquire_item(inventory, item)

        # Demonstrate tuple immutability
        # try:
        #     room[1] = "A ballroom"
        # except TypeError as error:
        #     print("tuples are immutable!")

        match (challenge_type):
            case "puzzle":
                print("You encounter a puzzle!")
                user_input = input("")

                if user_input == "solve":
                    success = random.choice([True, False])
                    print(challenge_outcome[0] if success else challenge_outcome[1])
                    player_health += challenge_outcome[2]
            case "trap":
                print("You see a potential trap!")
                user_input = input("")

                if user_input == "disarm":
                    success = random.choice([True, False])
                    print(challenge_outcome[0] if success else challenge_outcome[1])

                    if not success:
                        player_health += challenge_outcome[2]
            case _:
                print("You acquired a gold coins!")
                print("There doesn't seem to be a challenge in this room. You move on.")

        if player_health <= 0:
            print("You are barely alive!")
            player_health = 0

        # Use list concatenation (+) to extend inventory with additional items
        # inventory += ["gold bar", "gold nugget"]

        # Use remove() to remove an item
        #if "gold coins" in inventory:
        #    inventory.remove("gold coins")
        #    print("You used your gold coins.")

        display_inventory(inventory)

    print(f"\nYou exit the dungeon with {player_health} health remaining.")
    return player_health, inventory

def main():
    """
        The main function for the rest of the program.
    """
    player_health_initial = 100
    monster_health_initial = 75
    has_treasure = False

    inventory = []
    dungeon_rooms = [
        ("A puzzle chamber", None, "puzzle", ("Puzzle solved!", "Puzzle failed!", -10)),
        ("A narrow passage with a creaky floor", None, "trap", ("You skillfully avoid the trap!",
                                                                "You triggered a trap!", -10)),
        ("A treasure room", "gold coins", "none", None),
        ("A small room with a locked chest", "treasure", "puzzle", ("You cracked the code!",
                                                    "The chest remains stubbornly locked.", -5))
    ]

    player_health_initial = handle_path_choice(player_health_initial)
    has_treasure = random.choice([True, False])
    combat_encounter(player_health_initial, monster_health_initial, has_treasure)
    check_for_treasure(has_treasure)

    enter_dungeon(player_health_initial, inventory, dungeon_rooms)

if __name__ == "__main__":
    INTRO = (
        "After having one of the most vivid nightmares of your life, you awoke in "
        "a cold sweat. Rather than awakening in your bed, you found yourself in a crop circle,\n"
        "surrounded by towering walls of wheat, with no earthly idea of how you had gotten there. "
        "Despite feeling disoriented and nauseated,\nyou noticed a path forward—your \"way out.\" "
        "After walking for a while, you come across a fork in the path."
    )
    print(INTRO + "\n")
    main()
