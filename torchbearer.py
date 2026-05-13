"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Mohamed Rabi
Student ID:   827682382

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    
    return """
    - **Why a single shortest-path run from S is not enough:**
    Dijkstra from S finds the cheapest path to each node, but
    visiting all relics means choosing an order and different orders have
    different total costs, and a single run cannot compare them.

    - **What decision remains after all inter-location costs are known:**
    The order to visit the relics. Once we calaulate the travel costs between all relics,
    we need to arrange them to minimize the fuel consumption.
    - **Why this requires a search over orders (one sentence):**
    Greedy choices don't guarantee the best result, so all permutations must be checked.

    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return """
    ## Part 3: Algorithm Correctness

    ### Part 3a: What the Invariant Means

    - **For nodes already finalized (in S):**
    dist[u] is the true shortest distance — it won't change.


    - **For nodes not yet finalized (not in S):**
    dist[v] is the best distance found so far, but may still improve.

    ### Part 3b: Why Each Phase Holds

    - **Initialization : why the invariant holds before iteration 1:**
    dist[source] = 0 before any iteration. Everything else is float('inf') since no paths have been explored yet.

    - **Maintenance : why finalizing the min-dist node is always correct:**
    We always get the node with the smallest distance.
    Since edge weights are nonnegative, no unfinalized path can do better, so
    locking it in is safe. Relaxing neighbors can lower their distances.

    - **Termination : what the invariant guarantees when the algorithm ends:**
    Once the heap is empty, every reachable node is finalized and
    holds its true shortest distance. Unreachable nodes stay as float('inf').

    ### Part 3c: Why This Matters for the Route Planner
    Wrong distances would cause find_optimal_route to pick
    the wrong relic order and return a suboptimal route.
    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    return """
    ## Part 4: Search Design

    ### Why Greedy Fails

    - **The failure mode:** Picking the nearest unvisited relic each step can cause expensive moves later.
    - **Counter-example setup:** Spawn S, relics B, C, D, exit T. Edges: S-B=1, S-C=2, S-D=2, B-D=1, B-T=1, C-B=1, C-T=1, D-B=1, D-C=1.
    - **What greedy picks:** Nearest to S is B and cost 1, nearest remaining from B is D and cost 1, then C cost 1, then T cost 1. Total = 4.
    - **What optimal picks:** Same cost in this example, but greedy has no guarantee changing one weight breaks it while search still finds the true minimum.
    - **Why greedy loses:** It commits to a local choice without seeing how it affects the remaining steps.

    ### What the Algorithm Must Explore

    - The algorithm must consider every possible order of visiting the relics and return the one with the lowest total fuel cost.

    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    if not relics:
        cost = dist_table.get(spawn, {}).get(exit_node, float('inf'))
        return (cost, [])

    best = [float('inf'), []] 

    relics_remaining = set(relics)
    _explore(dist_table, spawn, relics_remaining, [], 0.0, exit_node, best)

    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    # Base case
    if not relics_remaining:
        cost_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total = cost_so_far + cost_to_exit
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    # if cost so far already >= the best known solution, nothing can improve it because all edge weights are nonnegative
    if cost_so_far >= best[0]:
        return

    # Recursive case
    for relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(relic, float('inf'))
        if travel_cost == float('inf'):
            continue  
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(dist_table, relic, relics_remaining,
                 relics_visited_order, cost_so_far + travel_cost,
                 exit_node, best)
        relics_visited_order.pop()
        relics_remaining.add(relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)



# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
