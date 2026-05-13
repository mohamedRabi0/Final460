# Development Log – The Torchbearer

**Student Name:** Mohamed Rabi
**Student ID:**   827682382
> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [05/11]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

_Your entry here._
My plan is to implement the pipeline in order: start with run_dijkstra since
everything else depends on the correct shortest path distances, then build
select_sources and precompute_distances, and finish with the
backtracking search. The most difficult part is _explore, getting
pruning correct and making sure backtracking works. I'll 
test each function on small graphs before running the actual tests.

---

## Entry 2 – [05/11]: [Short description]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

_Your entry here._
Instead of checking every single spot, I'm only starting from the spawn and relics. 
Since the exit is only a destination, this makes the pre-calculation much faster.

---

## Entry 3 – [05/13]: [Short description]

_Your entry here._
I started with a list and used list.remove() during backtracking, but
remove() is O(k). Switched to a set since add and remove are both O(1), making backtracking a clean one-liner.
Kept a separate list just to track visit order for the return value.

---

## Entry 4 – [05/13]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._
Everything passes all five provided tests. If I had more time I would add a
tighter lower bound to the pruning — for example adding the cheapest edge
out of the current node before comparing against best[0], which would cut
more branches on dense graphs. I would also look into bitmask DP to bring
worst-case complexity from O(k!) down to O(2^k * k^2).

---

## Final Entry – [05/13]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 0.5 |
| Part 2: Precomputation Design | 0.75 |
| Part 3: Algorithm Correctness | 0.5 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 0.5 |
| Part 6: Pruning | 0.5 |
| Part 7: Implementation | 2.0 |
| README and DEVLOG writing | 1.0 |
| **Total** | **6.25** |