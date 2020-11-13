import json, random, os, time

t0 = time.time()

def main():
    # TODO: allow them to choose from multiple JSON files?
    print('Loading game...')
    library = []
    for path in os.listdir():
        if path.endswith(".json"):
            with open(path) as fp:
                data = json.load(fp)
                library.append(data)
            print(" {}. {} in {}".format(len(library), data['__metadata__']['title'], path))
    choice = int(input('> '))
    game = 0
    if choice == 1:
        game = library[0]
    elif choice == 2:
        game = library[1]
    else:
        print('Please run the program again and choose from the list above')
        return
    play(game)
    

def no_bridges_to_nowhere(game):
    for x in game:
        if x != '__metadata__':
            here = game[x]
            for y in here['exits']:
                exit = y['destination']
                if exit not in game:
                    print(exit)
                    return False
    return True

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if len(here["items"]) > 0:
            print("There's a", here["items"], "in this room.")

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        if action == "stuff":
            if len(stuff) == 0:
                print("Your stuff is empty")
            else:
                print("Your stuff contains", stuff)
            continue
        
        if action == "take":
            print("What would you like to take?")
            item = input("> ").lower().strip()
            try:
                here['items'].remove(item)
                stuff.append(item)
                print("You have taken a ", item)
            except:
                print("'{}' is not available".format(item))
            continue
        
        if action == "drop":
            print("What item do you want to leave behind?")
            item = input("> ").lower().strip()
            try:
                stuff.remove(item)
                here["items"].append(item)
                print('You left the', item, 'behind.')
            except:
                print("You can't drop '{}' because it's not in your stuff.".format(item))
            continue
        
        if action == "find":
            hidden_exits = find_hidden_exits(here, stuff)
            if len(hidden_exits) == 0:
                print("There was nothing to find.")
                continue
            for i in here['exits']:
                if 'required_key' in i and i['required_key'] in stuff:
                    print("You search the room and find the following:")
                    for exit in hidden_exits:
                        print(exit['description'])
                        exit["hidden"] = False
                elif 'required_key' in i and i['required_key'] not in stuff:
                    print("You don't have anything to help you search")
            continue
        
        if action == "help":
            print_instructions()
            continue
        
        if action == "time":
            elapsed = int(time.time() - t0)
            minutes = elapsed // 60
            seconds = elapsed % 60
            print(minutes, 'minutes', seconds, 'seconds')
            continue
        
        #Black Cat
        
        current_cat_room = random.choice(find_non_win_rooms(rooms))   
        if current_cat_room == current_place:
            print('You found a cat!')
            if 'sashimi' and 'caviar' in here['items']:
                current_cat_room = destination['name']
                print('Cat is purrrring and decides it will stay in the', destination['name'],'indefinitly.') 
            
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
    
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep


def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
