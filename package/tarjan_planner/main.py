from package.tarjan_planner.route_planner import Route
import argparse
import re

def arg_parser():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Tarjan Planner CLI - A tool with boolean options."
    )
    
    # Add boolean arguments
    parser.add_argument(
        '-c', '--cost',
        action='store_true',
        help='Enable the parameter flag (defaults to False).'
    )
    parser.add_argument(
        '-b', '--bicycle',
        action='store_true',
        help='Enable the boolean flag (defaults to False).'
    )

    parser.add_argument(
        '-p', '--plot',
        action='store_true',
        help='Enable the boolean flag (defaults to False).'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Access the arguments
    cost = args.cost            # True if -c/--cost is specified, False otherwise
    bicycle = args.bicycle      # True if -b/--bicycle is specified, False otherwise
    plot = args.plot            # True if -p/--plot is specified, False otherwise
    
    return cost, bicycle, plot


def main():
    cost, bicycle, plot = arg_parser()

    if not bicycle:
        print("Hello Tarjan! Let's plan your optimal trip this festival season!")
        
        # Loop until valid input is received for bicycle
        while True:
            bicycle_usr = input("Do you have a bicycle? (y/n): ").strip()
            if re.fullmatch(r'[yYnN]', bicycle_usr):  # Regex to match 'y', 'Y', 'n', or 'N'
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if bicycle_usr.capitalize() == "Y":
                bicycle = True

    if not cost:
        # Loop until valid input is received for cost
        while True:
            cost_usr = input("Do you want to prioritize cost instead of time? (y/n): ").strip()
            if re.fullmatch(r'[yYnN]', cost_usr):  # Regex to match 'y', 'Y', 'n', or 'N'
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        if cost_usr.capitalize() == "Y":
            cost = True
    
    my_route = Route(bicycle_available=bicycle, prioritize_cost=cost)
    my_route.print_best_route()

    if not plot:
        while True:
                plot_usr = input("Would you like to see the plot? (y/n): ").strip()
                if re.fullmatch(r'[yYnN]', plot_usr):  # Regex to match 'y', 'Y', 'n', or 'N'
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        
        if plot_usr.capitalize() == "Y":
            my_route.plot_graph()
    else:
        my_route.plot_graph()

if __name__=="__main__":
    main()