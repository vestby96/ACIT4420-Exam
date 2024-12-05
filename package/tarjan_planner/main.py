from package.tarjan_planner.route_planner import Route
import argparse
import os

def arg_parser():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Tarjan Planner CLI - A tool with boolean options."
    )
    
    parser.add_argument(
        '-c', '--cost',
        type=str,
        choices=['y', 'n'],
        help="Prioritize cost ('y' for Yes, 'n' for No)."
    )

    parser.add_argument(
        '-b', '--bicycle',
        type=str,
        choices=['y', 'n'],
        help="Do you have a bicycle ('y' for Yes, 'n' for No)."
    )

    parser.add_argument(
        '-p', '--plot',
        type=str,
        choices=['y', 'n'],
        help="Show the plot ('y' for Yes, 'n' for No)."
    )

    parser.add_argument(
        '-t', '--transport',
        type=str,
        help='Path to the input file for transport modes (optional).'
    )

    # Add string argument for file
    parser.add_argument(
        '-l', '--locations',
        type=str,
        help='Path to the input file for locations (optional).'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Access the arguments
    cost = args.cost                # 'y' or 'n' if specified, None otherwise
    bicycle = args.bicycle          # 'y' or 'n' if specified, None otherwise
    plot = args.plot                # 'y' or 'n' if specified, None otherwise
    transport = args.transport      # Path to the file if -f/--file is specified, None otherwise
    locations = args.locations      # Path to the file if -f/--file is specified, None otherwise
    
    return cost, bicycle, plot, transport, locations

def get_user_input(prompt, valid_responses):
    while True:
        try:
            response = input(prompt).strip()
            if response not in valid_responses:
                raise ValueError(f"Invalid input: {response}. Valid options are {', '.join(valid_responses)}.")
            return response
        except ValueError as e:
            print(e)

def main():
    try:
        print("Hello Tarjan! Let's plan your optimal trip this festival season!")
        cost, bicycle, plot, transport, locations = arg_parser()
        
        # Check for the given files
        base_path = "./package/tarjan_planner/"
        if not transport:
            transport = base_path + "transport_modes.json"
        else:
            transport = base_path + transport

        try:
            if not os.path.exists(transport):
                raise FileNotFoundError(f"Transport file not found at path: {transport}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)  # Exit program if critical file is missing

        if not locations:
            locations = base_path + "locations.json"
        else:
            locations = base_path + locations

        try:
            if not os.path.exists(locations):
                raise FileNotFoundError(f"Locations file not found at path: {locations}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)

        # If no arguments are given the program promts the user for more information
        if bicycle == None and cost == None and plot == None:
            if bicycle == None:
                bicycle_usr = get_user_input("Do you have a bicycle? (y/n): ", ["y", "n"])
                if bicycle_usr.capitalize() == "Y":
                        bicycle = True

            if cost == None:
                cost_usr = get_user_input("Do you want to prioritize cost instead of time? (y/n): ", ["y", "n"])
                if cost_usr.capitalize() == "Y":
                    cost = True
            
            if plot == None:
                plot_usr = get_user_input("Would you like to see the plot? (y/n): ", ["y", "n"])
                if plot_usr.capitalize() == "Y":
                    plot = True

        my_route = Route(transport_modes=transport, locations=locations, bicycle_available=bicycle, prioritize_cost=cost)
        my_route.print_best_route()

        if plot == True:
            my_route.plot_graph()
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__=="__main__":
    main()