# The Torchbearer

**Student Name:** Mohamed Rabi
**Student ID:**   827682382
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  Dijkstra from S finds the cheapest path to each node, but
  visiting all relics means choosing an order and different orders have
  different total costs, and a single run cannot compare them.

- **What decision remains after all inter-location costs are known:**
  The order to visit the relics. Once we calaulate the travel costs between all relics,
  we need to arrange them to minimize the fuel consumption.
- **Why this requires a search over orders (one sentence):**
  Greedy choices don't guarantee the best result, so all permutations must be checked.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Spawn node | Route always starts here because its the distances from spawn to all relics and exit |
| Each relic node | We need a map of the distances between every relic and the exit to find the fastest way out. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | A source node u which is the starting point of a shortest-path query |
| What the values represent | dist_table[u][v] = minimum fuel cost from u to any node v in the graph |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | looking up dist_table[u][v] hashes u then v directly to the stored value with no traversal needed |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k + 1 
- **Cost per run:** O((V + E) log V)
- **Total complexity:** O((k + 1)(V + E) log V)
- **Justification (one line):** Each run processes every edge once and every heap costs O(log V), repeated k + 1 times.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.


### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _Your answer here._
  dist[u] is the true shortest distance it doesn't change.


- **For nodes not yet finalized (not in S):**
  _Your answer here._
  dist[v] is the best distance found so far, but may still improve.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _Your answer here._
  dist[source] = 0 before any iteration. Everything else is float('inf') since no paths have been explored yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Your answer here._
  We always get the node with the smallest distance.
  Since edge weights are nonnegative, no unfinalized path can do better, so
  locking it in is safe. Relaxing neighbors can lower their distances.

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Your answer here._
  Once the heap is empty, every reachable node is finalized and
  holds its true shortest distance. Unreachable nodes stay as float('inf').

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Your answer here._
Wrong distances would cause find_optimal_route to pick
the wrong relic order and return a suboptimal route.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Picking the nearest unvisited relic each step can cause expensive moves later.
- **Counter-example setup:** Spawn S, relics B, C, D, exit T. Edges: S-B=1, S-C=2, S-D=2, B-D=1, B-T=1, C-B=1, C-T=1, D-B=1, D-C=1.
- **What greedy picks:** Nearest to S is B and cost 1, nearest remaining from B is D and cost 1, then C cost 1, then T cost 1. Total = 4.
- **What optimal picks:** Same cost in this example, but greedy has no guarantee changing one weight breaks it while search still finds the true minimum.
- **Why greedy loses:** It commits to a local choice without seeing how it affects the remaining steps.

### What the Algorithm Must Explore

- The algorithm must consider every possible order of visiting the relics and return the one with the lowest total fuel cost.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node (str or int) | The node the torchbearer is currently at |
| Relics already collected | relics_visited_order | list[node] | Ordered of relics visited so far |
| Fuel cost so far | cost_so_far | float | Total cost from spawn to current location |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | Python set for relics_remaining |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) set.remove(relic) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) set.add(relic) |
| Why this structure fits | Backtracking needs fast add and remove a set gives O(1) for both with no duplicates |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** At each level of the search we branch once for each remaining relic k choices, then k-1, then k-2, down to 1, which is k! in the worst case.
---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** The minimum total fuel cost found so far and the relic order both stored in the list called best.
- **When it is used:** At the start of every recursive callbefore branching into relic.
- **What it allows the algorithm to skip:** Any branch where cost_so_far already is equal to or greater than best[0] the whole subtree gets abandoned.


### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** cost_so_far, the set of remaining relics, and the shortest path distances between all relevant nodes.
- **What the lower bound accounts for:** The exact cost so far.
- **Why it never overestimates:** cost_so_far is the exact cost of steps already taken not an estimate, so its a lower bound.

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._
- Pruning is safe because all edge weights are nonnegative. Once cost_so_far >= best[0] it adds zero or more cost so the final total can never beat best[0]. No optimal solution gets skipped.
- The condition uses >= so it also prunes ties and we already have a solution of equal cost so no duplicates.

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
Class lecture slides
