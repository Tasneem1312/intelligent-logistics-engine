from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(distance_matrix, demands, num_vehicles, vehicle_capacity):
    """
    Stores the data for the routing problem.
    """
    data = {}
    data['distance_matrix'] = distance_matrix
    data['demands'] = demands          # The weight of each package
    data['num_vehicles'] = num_vehicles
    data['vehicle_capacities'] = [vehicle_capacity] * num_vehicles # Assume identical trucks
    data['depot'] = 0                  # The index of the Hub (Node 0)
    return data

def solve_cvrp(distance_matrix, demands, num_vehicles=3, vehicle_capacity=150):
    """
    Solves the Capacitated Vehicle Routing Problem (CVRP).
    """
    # 1. Instantiate the data problem
    data = create_data_model(distance_matrix, demands, num_vehicles, vehicle_capacity)

    # 2. Create the Routing Index Manager
    # This keeps track of the nodes (Hub + Delivery points)
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot']
    )

    # 3. Create Routing Model (The actual solver)
    routing = pywrapcp.RoutingModel(manager)

    # 4. Define cost of each edge (The distance between points)
    def distance_callback(from_index, to_index):
        # Convert from routing variable to distance matrix index
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # Tell the solver that we want to minimize this distance
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 5. Add Capacity Constraints (Don't overload the trucks)
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack (no extra buffer)
        data['vehicle_capacities'],  # maximum load per vehicle
        True,  # start cumul to zero (trucks start empty)
        'Capacity'
    )

    # 6. Set Search Parameters (How hard the AI should think)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # Use 'PATH_CHEAPEST_ARC' as the first guess
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Let the solver run for a maximum of 3 seconds to find the absolute best route
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(3)

    # 7. Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # 8. Extract the results if a solution is found
    if solution:
        routes = []
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            route = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route.append(node_index)
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index)) # Add the return to Hub
            routes.append(route)
        return routes
    else:
        return None