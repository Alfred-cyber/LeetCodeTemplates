"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║             THE ULTIMATE LEETCODE PATTERN TEMPLATES                          ║
║                                                                              ║
║   "Every hard problem is just a pattern you haven't seen enough times yet."  ║
║                                                                              ║
║   Patterns Covered:                                                          ║
║   1.     Sliding Window                                                      ║
║   2.     Two Pointers                                                        ║
║   3.     Binary Search                                                       ║
║   4.     Hash Map / Frequency Counter                                        ║
║   5.     Binary Tree Traversals (DFS + BFS)                                  ║
║   6.     Dynamic Programming                                                 ║
║   7.     Linked List Tricks                                                  ║
║   8.     Stack & Monotonic Stack                                             ║
║   9.     Prefix Sum                                                          ║
║   10.    Backtracking                                                        ║
║   11.    Graph Traversal (DFS + BFS)                                         ║
║   12.    Heap / Priority Queue                                               ║
║   13.    Merge Intervals                                                     ║
║   14.    Fast & Slow Pointers (Floyd's Cycle)                                ║
║   15.    Bit Manipulation                                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from collections import defaultdict, deque, Counter
from typing import List, Optional, Dict, Tuple
import heapq


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 1: SLIDING WINDOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: Imagine a window sliding over an array.
#   The window GROWS by moving the right edge forward.
#   The window SHRINKS by moving the left edge forward.
#
#   USE WHEN:
#   Problem asks for "longest/shortest subarray/substring"
#   Problem involves a contiguous sequence
#   Problem has a constraint on the window (max k distinct, sum ≤ target)
#
#   TWO FLAVORS:
#   → Fixed Size Window  : window size never changes (e.g., max sum of k elements)
#   → Variable Size Window: window shrinks when a condition is violated
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sliding_window_fixed_size(numbers: List[int], window_size: int) -> int:
    """
    Template: Fixed-size sliding window.
    Example use case: Maximum sum of k consecutive elements.

    Time: O(n)  |  Space: O(1)
    """
    if len(numbers) < window_size:
        return 0

    #  Build the first window from scratch
    current_window_sum = sum(numbers[:window_size])
    best_sum_seen = current_window_sum

    # 🪟 Slide the window one step at a time
    for right_edge in range(window_size, len(numbers)):
        element_entering_window = numbers[right_edge]
        element_leaving_window  = numbers[right_edge - window_size]

        current_window_sum += element_entering_window
        current_window_sum -= element_leaving_window

        best_sum_seen = max(best_sum_seen, current_window_sum)

    return best_sum_seen


def sliding_window_variable_size(numbers: List[int], target_sum: int) -> int:
    """
    Template: Variable-size sliding window.
    Example use case: Smallest subarray with sum >= target.

    Time: O(n)  |  Space: O(1)
    """
    left_edge              = 0
    current_window_sum     = 0
    shortest_length_found  = float('inf')

    for right_edge in range(len(numbers)):

        #  Expand window — absorb the new element on the right
        current_window_sum += numbers[right_edge]

        #   Shrink window from the left as long as condition is satisfied
        while current_window_sum >= target_sum:
            window_length         = right_edge - left_edge + 1
            shortest_length_found = min(shortest_length_found, window_length)

            #   Expel the leftmost element and move left edge inward
            current_window_sum -= numbers[left_edge]
            left_edge          += 1

    return 0 if shortest_length_found == float('inf') else shortest_length_found


def sliding_window_with_character_frequency(text: str, num_distinct_chars_allowed: int) -> int:
    """
    Template: Sliding window with a frequency map.
    Example use case: Longest substring with at most K distinct characters.

    Time: O(n)  |  Space: O(k)
    """
    left_edge           = 0
    longest_found       = 0
    character_frequency = defaultdict(int)  # tracks how often each char appears in window

    for right_edge in range(len(text)):
        new_character = text[right_edge]
        character_frequency[new_character] += 1

        # Window violated the constraint — shrink from the left
        while len(character_frequency) > num_distinct_chars_allowed:
            leftmost_character = text[left_edge]
            character_frequency[leftmost_character] -= 1

            if character_frequency[leftmost_character] == 0:
                del character_frequency[leftmost_character]

            left_edge += 1

        #   Window is valid — update the best answer
        longest_found = max(longest_found, right_edge - left_edge + 1)

    return longest_found


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 2: TWO POINTERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: Two people walking on a number line.
#   They can walk toward each other (opposite ends → middle)
#   Or walk in the same direction (slow & fast pointers)
#
#   USE WHEN:
#     Array is sorted (or can be sorted)
#     Looking for a pair, triplet, or subsequence
#     Comparing elements from both ends
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def two_pointers_find_pair_with_target_sum(sorted_numbers: List[int], target: int) -> List[int]:
    """
    Template: Two pointers from opposite ends.
    Example use case: Two Sum II (sorted array).

    Time: O(n)  |  Space: O(1)
    """
    left_pointer  = 0
    right_pointer = len(sorted_numbers) - 1

    while left_pointer < right_pointer:
        current_sum = sorted_numbers[left_pointer] + sorted_numbers[right_pointer]

        if current_sum == target:
            return [left_pointer + 1, right_pointer + 1]  # 1-indexed answer

        elif current_sum < target:
            left_pointer += 1   #  Sum is too small — move left pointer right to increase

        else:
            right_pointer -= 1  #  Sum is too large — move right pointer left to decrease

    return []  # No pair found


def two_pointers_find_all_triplets_summing_to_zero(numbers: List[int]) -> List[List[int]]:
    """
    Template: Two pointers inside a loop (3Sum pattern).
    Example use case: 3Sum — find all triplets that sum to zero.

    Time: O(n²)  |  Space: O(1) excluding output
    """
    numbers.sort()
    all_valid_triplets = []

    for first_index, first_number in enumerate(numbers):

        #   Skip duplicate values to avoid duplicate triplets
        if first_index > 0 and first_number == numbers[first_index - 1]:
            continue

        # Two pointers scan the remaining portion of the array
        left_pointer  = first_index + 1
        right_pointer = len(numbers) - 1

        while left_pointer < right_pointer:
            triplet_sum = first_number + numbers[left_pointer] + numbers[right_pointer]

            if triplet_sum == 0:
                all_valid_triplets.append([first_number, numbers[left_pointer], numbers[right_pointer]])
                left_pointer  += 1
                right_pointer -= 1

                # Skip duplicates on both sides
                while left_pointer < right_pointer and numbers[left_pointer] == numbers[left_pointer - 1]:
                    left_pointer += 1
                while left_pointer < right_pointer and numbers[right_pointer] == numbers[right_pointer + 1]:
                    right_pointer -= 1

            elif triplet_sum < 0:
                left_pointer  += 1
            else:
                right_pointer -= 1

    return all_valid_triplets


def two_pointers_remove_duplicates_in_place(sorted_numbers: List[int]) -> int:
    """
    Template: Slow/fast pointer in same direction.
    Example use case: Remove duplicates from sorted array in-place.

    Time: O(n)  |  Space: O(1)
    """
    if not sorted_numbers:
        return 0

    slow_writer = 0  #  Points to the last unique position written

    for fast_reader in range(1, len(sorted_numbers)):  #   Scans ahead
        if sorted_numbers[fast_reader] != sorted_numbers[slow_writer]:
            slow_writer += 1
            sorted_numbers[slow_writer] = sorted_numbers[fast_reader]

    number_of_unique_elements = slow_writer + 1
    return number_of_unique_elements


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 3: BINARY SEARCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: Guess a number 1-100. Each guess, you're told "higher" or
#   "lower". Binary search is the optimal guessing strategy.
#
#   USE WHEN:
#     The search space is sorted (or has a monotonic property)
#     You can decide in O(1) which HALF to discard
#     Problem says "find minimum X where condition holds" → binary search on answer!
#
#     THE KEY INSIGHT: Binary search isn't just for sorted arrays.
#   Any time you can split the answer space in half, you can binary search.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def binary_search_classic(sorted_array: List[int], target: int) -> int:
    """
    Template: Classic binary search — find exact target.

    Time: O(log n)  |  Space: O(1)
    """
    left  = 0
    right = len(sorted_array) - 1

    while left <= right:
        mid_index  = left + (right - left) // 2   #   Avoids integer overflow vs (left+right)//2
        mid_value  = sorted_array[mid_index]

        if mid_value == target:
            return mid_index        #   Found it!

        elif mid_value < target:
            left = mid_index + 1    #   Target is in the RIGHT half

        else:
            right = mid_index - 1   #   Target is in the LEFT half

    return -1   # Target not found


def binary_search_find_leftmost_position(sorted_array: List[int], target: int) -> int:
    """
    Template: Binary search — find FIRST occurrence (leftmost insertion point).
    Also called "lower bound".

    Time: O(log n)  |  Space: O(1)
    """
    left   = 0
    right  = len(sorted_array)  # ← Note: right is EXCLUSIVE (one past the end)
    result = -1

    while left < right:
        mid_index = left + (right - left) // 2
        mid_value = sorted_array[mid_index]

        if mid_value == target:
            result = mid_index
            right  = mid_index      #   Keep searching LEFT for an earlier occurrence

        elif mid_value < target:
            left   = mid_index + 1  #   Go right

        else:
            right  = mid_index      #   Go left

    return result


def binary_search_on_answer(piles_of_bananas: List[int], hours_available: int) -> int:
    """
    Template: Binary search on the ANSWER SPACE (not the array).
    Example use case: Koko Eating Bananas — find minimum eating speed.

    KEY PATTERN: "Find the minimum/maximum X such that condition(X) is True"
    → Binary search between min_possible_answer and max_possible_answer

    Time: O(n log m)  |  Space: O(1)
    """
    import math

    def can_finish_all_bananas_at_this_speed(eating_speed: int) -> bool:
        total_hours_needed = sum(
            math.ceil(pile / eating_speed) for pile in piles_of_bananas
        )
        return total_hours_needed <= hours_available

    #   Search in the space of possible answers
    slowest_possible_speed = 1
    fastest_possible_speed = max(piles_of_bananas)
    minimum_valid_speed    = fastest_possible_speed

    left  = slowest_possible_speed
    right = fastest_possible_speed

    while left <= right:
        candidate_speed = left + (right - left) // 2

        if can_finish_all_bananas_at_this_speed(candidate_speed):
            minimum_valid_speed = candidate_speed
            right = candidate_speed - 1   # ← Try to find something even slower (smaller)

        else:
            left = candidate_speed + 1    # ← This speed is too slow, go faster

    return minimum_valid_speed


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 4: HASH MAP / FREQUENCY COUNTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: A hash map is your notebook. You write things down so you
#   don't have to re-scan the array to remember what you've already seen.
#
#   USE WHEN:
#     You need to look up something you've seen before in O(1)
#     Counting frequencies of elements
#     Grouping elements by some property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def hashmap_two_sum(numbers: List[int], target: int) -> List[int]:
    """
    Template: Hash map to store previously seen values.
    Example use case: Two Sum.

    Time: O(n)  |  Space: O(n)
    """
    # Maps each number we've seen → the index where we saw it
    number_to_its_index: Dict[int, int] = {}

    for current_index, current_number in enumerate(numbers):
        complement_needed = target - current_number

        if complement_needed in number_to_its_index:
            index_of_complement = number_to_its_index[complement_needed]
            return [index_of_complement, current_index]

        #   Write this number into our "have we seen this?" notebook
        number_to_its_index[current_number] = current_index

    return []


def hashmap_group_anagrams(list_of_words: List[str]) -> List[List[str]]:
    """
    Template: Group elements by a computed key.
    Example use case: Group Anagrams.

    Time: O(n * k log k) where k = average word length  |  Space: O(n)
    """
    # Maps sorted-letters → all words that produce those sorted letters
    anagram_groups: Dict[str, List[str]] = defaultdict(list)

    for word in list_of_words:
        sorted_letters = tuple(sorted(word))   #  The "fingerprint" of an anagram group
        anagram_groups[sorted_letters].append(word)

    return list(anagram_groups.values())


def hashmap_subarray_sum_equals_k(numbers: List[int], target_k: int) -> int:
    """
    Template: Prefix sum + hash map to count subarrays.
    Example use case: Subarray Sum Equals K.

    KEY INSIGHT: If prefix_sum[j] - prefix_sum[i] == k,
                 then the subarray from i+1 to j has sum k.
                 We check: "have we seen (current_prefix_sum - k) before?"

    Time: O(n)  |  Space: O(n)
    """
    # Maps prefix_sum → how many times we've reached this prefix sum
    times_we_have_seen_each_prefix_sum: Dict[int, int] = {0: 1}

    running_prefix_sum  = 0
    total_valid_subarrays = 0

    for number in numbers:
        running_prefix_sum += number

        complement_prefix_sum = running_prefix_sum - target_k

        if complement_prefix_sum in times_we_have_seen_each_prefix_sum:
            total_valid_subarrays += times_we_have_seen_each_prefix_sum[complement_prefix_sum]

        times_we_have_seen_each_prefix_sum[running_prefix_sum] = (
            times_we_have_seen_each_prefix_sum.get(running_prefix_sum, 0) + 1
        )

    return total_valid_subarrays


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 5: BINARY TREE TRAVERSALS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TreeNode:
    """Standard binary tree node used in LeetCode problems."""
    def __init__(self, value: int = 0, left=None, right=None):
        self.value = value
        self.left  = left
        self.right = right


def tree_dfs_inorder(root: Optional[TreeNode]) -> List[int]:
    """
    Template: DFS Inorder — Left → Root → Right
      Result is SORTED for a BST!

    Time: O(n)  |  Space: O(h) where h = tree height
    """
    visited_values = []

    def visit_subtree(node: Optional[TreeNode]):
        if node is None:
            return

        visit_subtree(node.left)          #  Go left first
        visited_values.append(node.value)  #   Process this node
        visit_subtree(node.right)         #  Go right last

    visit_subtree(root)
    return visited_values


def tree_dfs_preorder(root: Optional[TreeNode]) -> List[int]:
    """
    Template: DFS Preorder — Root → Left → Right
      Useful for copying/serializing a tree (you process root BEFORE children)

    Time: O(n)  |  Space: O(h)
    """
    visited_values = []

    def visit_subtree(node: Optional[TreeNode]):
        if node is None:
            return

        visited_values.append(node.value)  #   Process this node FIRST
        visit_subtree(node.left)
        visit_subtree(node.right)

    visit_subtree(root)
    return visited_values


def tree_bfs_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Template: BFS Level Order — process nodes level by level.
    Uses a queue. Essential for problems asking about levels/depth.

    Time: O(n)  |  Space: O(w) where w = max width of tree
    """
    if root is None:
        return []

    result_by_level    = []
    queue_of_nodes     = deque([root])

    while queue_of_nodes:
        number_of_nodes_in_this_level = len(queue_of_nodes)
        values_at_this_level          = []

        for _ in range(number_of_nodes_in_this_level):
            current_node = queue_of_nodes.popleft()
            values_at_this_level.append(current_node.value)

            if current_node.left:
                queue_of_nodes.append(current_node.left)
            if current_node.right:
                queue_of_nodes.append(current_node.right)

        result_by_level.append(values_at_this_level)

    return result_by_level


def tree_dfs_max_depth(root: Optional[TreeNode]) -> int:
    """
    Template: Recursive DFS returning a computed value bottom-up.
    Example use case: Maximum Depth of Binary Tree.

      MENTAL MODEL: Ask each subtree "how tall are you?" and add 1 for yourself.

    Time: O(n)  |  Space: O(h)
    """
    if root is None:
        return 0

    depth_of_left_subtree  = tree_dfs_max_depth(root.left)
    depth_of_right_subtree = tree_dfs_max_depth(root.right)
    depth_of_this_subtree  = 1 + max(depth_of_left_subtree, depth_of_right_subtree)

    return depth_of_this_subtree


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 6: DYNAMIC PROGRAMMING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: DP is just "smart recursion". Instead of solving the same
#   subproblem twice, you remember (memoize) the answer.
#
#   TWO APPROACHES:
#   → Top-Down (Memoization): Start from the big problem, recurse down,
#                              cache results. (More intuitive to write)
#   → Bottom-Up (Tabulation):  Start from smallest subproblems, build up.
#                              (Usually faster in practice)
#
#   THE DP RECIPE:
#   1. Define what dp[i] MEANS in plain English
#   2. Find the RECURRENCE (how dp[i] depends on smaller values)
#   3. Set BASE CASES
#   4. Determine the correct ITERATION ORDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def dp_fibonacci_top_down(n: int) -> int:
    """
    Template: Top-down DP with memoization.
    Example use case: Climbing Stairs / Fibonacci.

    Time: O(n)  |  Space: O(n)
    """
    answers_we_already_know: Dict[int, int] = {}

    def compute_fibonacci(position: int) -> int:
        if position <= 1:
            return position   #  Base case

        if position in answers_we_already_know:
            return answers_we_already_know[position]   #  Already solved — return cached answer

        answer = compute_fibonacci(position - 1) + compute_fibonacci(position - 2)
        answers_we_already_know[position] = answer
        return answer

    return compute_fibonacci(n)


def dp_climbing_stairs_bottom_up(number_of_stairs: int) -> int:
    """
    Template: Bottom-up DP (tabulation).
    Example use case: Climbing Stairs (1 or 2 steps at a time).

    dp[i] = "number of distinct ways to reach stair i"
    Recurrence: dp[i] = dp[i-1] + dp[i-2]
    (reach stair i either from stair i-1 or from stair i-2)

    Time: O(n)  |  Space: O(1) — we only need the last two values
    """
    if number_of_stairs <= 2:
        return number_of_stairs

    ways_to_reach_two_stairs_ago = 1   # dp[1]
    ways_to_reach_one_stair_ago  = 2   # dp[2]

    for stair in range(3, number_of_stairs + 1):
        ways_to_reach_current_stair  = ways_to_reach_one_stair_ago + ways_to_reach_two_stairs_ago
        ways_to_reach_two_stairs_ago = ways_to_reach_one_stair_ago
        ways_to_reach_one_stair_ago  = ways_to_reach_current_stair

    return ways_to_reach_one_stair_ago


def dp_longest_increasing_subsequence(numbers: List[int]) -> int:
    """
    Template: 1D DP where dp[i] depends on ALL previous values.
    Example use case: Longest Increasing Subsequence (LIS).

    dp[i] = "length of the longest increasing subsequence ENDING at index i"

    Time: O(n²)  |  Space: O(n)
    """
    if not numbers:
        return 0

    # Every element by itself is a valid subsequence of length 1
    longest_subsequence_ending_here = [1] * len(numbers)

    for current_index in range(1, len(numbers)):
        for previous_index in range(current_index):
            current_number  = numbers[current_index]
            previous_number = numbers[previous_index]

            if previous_number < current_number:
                can_extend_previous = longest_subsequence_ending_here[previous_index] + 1
                longest_subsequence_ending_here[current_index] = max(
                    longest_subsequence_ending_here[current_index],
                    can_extend_previous
                )

    return max(longest_subsequence_ending_here)


def dp_knapsack_zero_one(item_weights: List[int], item_values: List[int], bag_capacity: int) -> int:
    """
    Template: 0/1 Knapsack — classic 2D DP.
    Each item can be taken ONCE (hence "0/1").

    dp[item_index][remaining_capacity] = "max value using first (item_index) items
                                          with (remaining_capacity) capacity left"

    Time: O(n * capacity)  |  Space: O(capacity) after space optimization

    Space-optimized version shown below (1D array, iterating in REVERSE).
    """
    number_of_items = len(item_weights)

    # dp[capacity] = max value achievable with exactly 'capacity' remaining space
    best_value_with_this_capacity = [0] * (bag_capacity + 1)

    for item_index in range(number_of_items):
        this_item_weight = item_weights[item_index]
        this_item_value  = item_values[item_index]

        #   MUST iterate in REVERSE to ensure each item is picked at most once
        for current_capacity in range(bag_capacity, this_item_weight - 1, -1):
            capacity_after_taking_this_item = current_capacity - this_item_weight
            value_if_we_take_this_item = best_value_with_this_capacity[capacity_after_taking_this_item] + this_item_value
            value_if_we_skip_this_item = best_value_with_this_capacity[current_capacity]

            best_value_with_this_capacity[current_capacity] = max(
                value_if_we_take_this_item,
                value_if_we_skip_this_item
            )

    return best_value_with_this_capacity[bag_capacity]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 7: LINKED LIST TRICKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ListNode:
    """Standard singly linked list node."""
    def __init__(self, value: int = 0, next=None):
        self.value = value
        self.next  = next


def linked_list_reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Template: Iterative linked list reversal.
    Time: O(n)  |  Space: O(1)
    """
    previous_node = None
    current_node  = head

    while current_node is not None:
        next_node_to_visit    = current_node.next   #  Save next before we overwrite it
        current_node.next     = previous_node        #  Flip the pointer
        previous_node         = current_node         #  Advance previous
        current_node          = next_node_to_visit   #  Advance current

    new_head = previous_node
    return new_head


def linked_list_with_dummy_head(head: Optional[ListNode], value_to_remove: int) -> Optional[ListNode]:
    """
    Template: Use a dummy head node to simplify edge cases.
    Example use case: Remove Elements from linked list.

      MENTAL MODEL: The dummy node acts like a "fake head" so we never have
    to special-case removing the actual head node.

    Time: O(n)  |  Space: O(1)
    """
    dummy_head           = ListNode(value=0, next=head)
    previous_node        = dummy_head

    while previous_node.next is not None:
        node_to_examine = previous_node.next

        if node_to_examine.value == value_to_remove:
            previous_node.next = node_to_examine.next    #   Skip over this node
        else:
            previous_node = previous_node.next           #  Move forward

    return dummy_head.next   # The real head


def linked_list_find_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Template: Fast & slow pointers to find middle of linked list.
    Time: O(n)  |  Space: O(1)
    """
    slow_pointer = head
    fast_pointer = head

    while fast_pointer is not None and fast_pointer.next is not None:
        slow_pointer = slow_pointer.next          #   One step at a time
        fast_pointer = fast_pointer.next.next     #   Two steps at a time

    # When fast reaches the end, slow is at the middle
    middle_node = slow_pointer
    return middle_node


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 8: STACK & MONOTONIC STACK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: A stack is a stack of plates — you can only touch the top.
#   A MONOTONIC stack keeps plates in sorted order by throwing away plates
#   that violate the order before adding a new one.
#
#   USE WHEN:
#     "Next greater element" / "Previous smaller element"
#     Valid parentheses / matching brackets
#     Histogram / largest rectangle problems
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def stack_valid_parentheses(bracket_string: str) -> bool:
    """
    Template: Stack for matching pairs.
    Example use case: Valid Parentheses.

    Time: O(n)  |  Space: O(n)
    """
    stack_of_open_brackets       = []
    matching_closer_for_opener   = {'(': ')', '[': ']', '{': '}'}

    for character in bracket_string:
        is_an_opening_bracket = character in matching_closer_for_opener

        if is_an_opening_bracket:
            stack_of_open_brackets.append(character)

        else:  # It's a closing bracket
            if not stack_of_open_brackets:
                return False   # Closing bracket with nothing open → invalid

            most_recent_opener          = stack_of_open_brackets.pop()
            expected_closer             = matching_closer_for_opener[most_recent_opener]
            this_closer_matches_opener  = (character == expected_closer)

            if not this_closer_matches_opener:
                return False

    all_openers_were_closed = len(stack_of_open_brackets) == 0
    return all_openers_were_closed


def monotonic_stack_next_greater_element(numbers: List[int]) -> List[int]:
    """
    Template: Monotonic DECREASING stack for "next greater element".

      MENTAL MODEL: Imagine people standing in a line. Each person looks right
    for the first person taller than them. The stack holds people who haven't
    found their "next greater person" yet.

    Time: O(n)  |  Space: O(n)
    """
    next_greater = [-1] * len(numbers)           # Default: no greater element found
    stack_of_indices_waiting_for_greater = []    # Stores indices of elements

    for current_index, current_number in enumerate(numbers):

        #   Pop anyone from the stack who finally found their "next greater"
        while stack_of_indices_waiting_for_greater and \
              numbers[stack_of_indices_waiting_for_greater[-1]] < current_number:

            index_of_resolved_element   = stack_of_indices_waiting_for_greater.pop()
            next_greater[index_of_resolved_element] = current_number

        stack_of_indices_waiting_for_greater.append(current_index)

    return next_greater


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 9: PREFIX SUM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: prefix_sum[i] = sum of all elements from index 0 to i-1.
#   Sum of subarray [left, right] = prefix_sum[right+1] - prefix_sum[left]
#   This turns O(n) range queries into O(1)!
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def prefix_sum_range_query(numbers: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    Template: Prefix sum for O(1) range sum queries.

    Time: O(n + q) where q = number of queries  |  Space: O(n)
    """
    #   Build prefix sum array (length n+1, prefix_sums[0] = 0 as sentinel)
    prefix_sums = [0] * (len(numbers) + 1)

    for index, number in enumerate(numbers):
        prefix_sums[index + 1] = prefix_sums[index] + number

    def get_sum_of_range(left_index: int, right_index: int) -> int:
        # Sum from left_index to right_index (inclusive)
        return prefix_sums[right_index + 1] - prefix_sums[left_index]

    return [get_sum_of_range(left, right) for left, right in queries]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     PATTERN 10: BACKTRACKING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: Backtracking = "Try everything, but take it back if it fails."
#   Like solving a maze: walk forward, hit a wall, back up, try a different path.
#
#   THE TEMPLATE ALWAYS LOOKS LIKE:
#   def explore(current_path):
#       if goal_reached: record answer; return
#       for each_choice in available_choices:
#           make_choice(each_choice)         #   Choose
#           explore(updated_path)            #  Recurse
#           undo_choice(each_choice)         #    Unchoose (BACKTRACK)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def backtracking_all_subsets(numbers: List[int]) -> List[List[int]]:
    """
    Template: Backtracking to generate all subsets (power set).

    Time: O(n * 2ⁿ)  |  Space: O(n)
    """
    all_subsets   = []
    current_subset = []

    def explore_subsets_starting_from(start_index: int):
        #   Every state of current_subset is a valid subset — record it
        all_subsets.append(list(current_subset))

        for index in range(start_index, len(numbers)):
            current_subset.append(numbers[index])   #   Choose this number
            explore_subsets_starting_from(index + 1) #  Explore further
            current_subset.pop()                     #    Unchoose (backtrack)

    explore_subsets_starting_from(start_index=0)
    return all_subsets


def backtracking_all_permutations(numbers: List[int]) -> List[List[int]]:
    """
    Template: Backtracking to generate all permutations.

    Time: O(n * n!)  |  Space: O(n)
    """
    all_permutations    = []
    numbers_already_used = set()

    def build_permutation(permutation_so_far: List[int]):
        if len(permutation_so_far) == len(numbers):
            all_permutations.append(list(permutation_so_far))
            return

        for index, number in enumerate(numbers):
            if index in numbers_already_used:
                continue

            permutation_so_far.append(number)     #   Choose
            numbers_already_used.add(index)

            build_permutation(permutation_so_far)  #   Recurse

            permutation_so_far.pop()              #    Unchoose
            numbers_already_used.remove(index)

    build_permutation(permutation_so_far=[])
    return all_permutations


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 11: GRAPH TRAVERSAL (DFS + BFS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL:
#   DFS = Go as deep as possible before backtracking. Like exploring a maze
#         by always turning left until you hit a dead end.
#   BFS = Explore all neighbors before going deeper. Like ripples in a pond.
#
#   BFS = shortest path in unweighted graph
#   DFS = connected components, cycle detection, topological sort
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def graph_dfs_count_islands(grid: List[List[str]]) -> int:
    """
    Template: DFS on a 2D grid to count connected components.
    Example use case: Number of Islands.

    Time: O(m * n)  |  Space: O(m * n) for recursion stack
    """
    if not grid:
        return 0

    number_of_rows    = len(grid)
    number_of_columns = len(grid[0])
    island_count      = 0

    def flood_fill_this_island(row: int, col: int):
        """Sink (mark as visited) all land connected to this cell."""
        out_of_bounds = (row < 0 or row >= number_of_rows or
                         col < 0 or col >= number_of_columns)
        already_water = (grid[row][col] == '0')

        if out_of_bounds or already_water:
            return

        grid[row][col] = '0'   #  Sink this land cell so we don't visit it again

        flood_fill_this_island(row + 1, col)   #  Down
        flood_fill_this_island(row - 1, col)   #  Up
        flood_fill_this_island(row, col + 1)   #  Right
        flood_fill_this_island(row, col - 1)   #  Left

    for row in range(number_of_rows):
        for col in range(number_of_columns):
            if grid[row][col] == '1':          #  Found new undiscovered land!
                island_count += 1
                flood_fill_this_island(row, col)

    return island_count


def graph_bfs_shortest_path(adjacency_list: Dict[int, List[int]],
                             start_node: int, end_node: int) -> int:
    """
    Template: BFS for shortest path in unweighted graph.

    Time: O(V + E)  |  Space: O(V)
    """
    visited_nodes     = {start_node}
    bfs_queue         = deque([(start_node, 0)])   # (node, distance_from_start)

    while bfs_queue:
        current_node, distance_from_start = bfs_queue.popleft()

        if current_node == end_node:
            return distance_from_start

        for neighboring_node in adjacency_list.get(current_node, []):
            if neighboring_node not in visited_nodes:
                visited_nodes.add(neighboring_node)
                bfs_queue.append((neighboring_node, distance_from_start + 1))

    return -1   # No path found


def graph_topological_sort(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Template: Topological sort using BFS (Kahn's Algorithm).
    Example use case: Course Schedule II.

    KEY CONCEPT: "In-degree" = number of prerequisites for a course.
    Start with courses that have 0 prerequisites.

    Time: O(V + E)  |  Space: O(V + E)
    """
    # Build: how many prerequisites does each course have?
    number_of_prerequisites = [0] * num_courses
    courses_that_unlock     = defaultdict(list)   # course → [courses it unlocks]

    for course, prereq in prerequisites:
        number_of_prerequisites[course] += 1
        courses_that_unlock[prereq].append(course)

    #Start with courses that have no prerequisites
    ready_to_take = deque(
        course for course in range(num_courses)
        if number_of_prerequisites[course] == 0
    )
    completed_courses = []

    while ready_to_take:
        current_course = ready_to_take.popleft()
        completed_courses.append(current_course)

        for unlocked_course in courses_that_unlock[current_course]:
            number_of_prerequisites[unlocked_course] -= 1

            if number_of_prerequisites[unlocked_course] == 0:
                ready_to_take.append(unlocked_course)

    all_courses_completed = len(completed_courses) == num_courses
    return completed_courses if all_courses_completed else []


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 12: HEAP / PRIORITY QUEUE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: A heap is a "priority queue" — like a VIP line.
#   The most important person (min or max) is always at the front.
#
#     Python's heapq is a MIN-HEAP by default.
#   To simulate MAX-HEAP: negate your values when pushing/popping.
#
#   USE WHEN:
#     "Find the Kth largest/smallest"
#     "Always process the current minimum/maximum"
#     Merging K sorted lists
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def heap_kth_largest_element(numbers: List[int], k: int) -> int:
    """
    Template: Use a min-heap of size K to find Kth largest.

      MENTAL MODEL: Keep a "squad" of the K biggest numbers seen so far.
    The smallest in the squad = the Kth largest overall.

    Time: O(n log k)  |  Space: O(k)
    """
    squad_of_k_biggest = []   # This is a min-heap

    for number in numbers:
        heapq.heappush(squad_of_k_biggest, number)

        if len(squad_of_k_biggest) > k:
            heapq.heappop(squad_of_k_biggest)   # Remove the smallest from our squad

    # The smallest in the squad is the Kth largest overall
    kth_largest = squad_of_k_biggest[0]
    return kth_largest


def heap_merge_k_sorted_lists(sorted_lists: List[List[int]]) -> List[int]:
    """
    Template: Merge K sorted lists using a min-heap.

    Time: O(n log k) where n = total elements  |  Space: O(k)
    """
    result_merged_list = []

    # Start by putting the first element of each list into the heap
    # Heap stores (value, which_list, index_in_that_list)
    min_heap = []
    for list_index, sorted_list in enumerate(sorted_lists):
        if sorted_list:
            heapq.heappush(min_heap, (sorted_list[0], list_index, 0))

    while min_heap:
        smallest_value, which_list, element_index = heapq.heappop(min_heap)
        result_merged_list.append(smallest_value)

        next_element_index = element_index + 1
        there_is_a_next_element = next_element_index < len(sorted_lists[which_list])

        if there_is_a_next_element:
            next_value = sorted_lists[which_list][next_element_index]
            heapq.heappush(min_heap, (next_value, which_list, next_element_index))

    return result_merged_list


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   PATTERN 13: MERGE INTERVALS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def merge_overlapping_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Template: Sort intervals by start time, then greedily merge.

    Two intervals [a, b] and [c, d] OVERLAP if c <= b.
    Merged interval = [a, max(b, d)]

    Time: O(n log n)  |  Space: O(n)
    """
    intervals.sort(key=lambda interval: interval[0])   #  Sort by start time
    merged_intervals = [intervals[0]]

    for current_start, current_end in intervals[1:]:
        last_merged_start, last_merged_end = merged_intervals[-1]

        intervals_overlap = current_start <= last_merged_end

        if intervals_overlap:
            #  Extend the last interval to cover both
            merged_intervals[-1][1] = max(last_merged_end, current_end)
        else:
            #  No overlap — start a new interval
            merged_intervals.append([current_start, current_end])

    return merged_intervals


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 14: FAST & SLOW POINTERS (FLOYD'S CYCLE DETECTION)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   MENTAL MODEL: Two runners on a circular track.
#   The fast runner (2x speed) will eventually lap the slow runner IF there's a cycle.
#   If no cycle, the fast runner reaches the end first.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fast_slow_detect_cycle(head: Optional[ListNode]) -> bool:
    """
    Template: Floyd's cycle detection.
    Example use case: Linked List Cycle.

    Time: O(n)  |  Space: O(1)
    """
    slow_runner = head
    fast_runner = head

    while fast_runner is not None and fast_runner.next is not None:
        slow_runner = slow_runner.next          #   Move one step
        fast_runner = fast_runner.next.next     #   Move two steps

        if slow_runner == fast_runner:
            return True   #   They met → cycle exists!

    return False   # Fast runner reached the end → no cycle


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    PATTERN 15: BIT MANIPULATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   CHEAT SHEET:
#   n & (n-1)    → Clears the lowest set bit of n        (count bits trick!)
#   n & (-n)     → Isolates the lowest set bit of n
#   n ^ n        → 0  (XOR of same number = 0)
#   n ^ 0        → n  (XOR with 0 = identity)
#   a ^ b ^ a    → b  (a cancels out — great for "find the single number")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def bit_manipulation_find_single_number(numbers: List[int]) -> int:
    """
    Template: XOR all numbers to find the one that appears once.
    Example use case: Single Number (all others appear twice).

      KEY INSIGHT: a ^ a = 0 and a ^ 0 = a
    XOR all numbers → pairs cancel out → only the single remains!

    Time: O(n)  |  Space: O(1)
    """
    xor_accumulator = 0

    for number in numbers:
        xor_accumulator ^= number   #   Pairs cancel each other out

    the_single_number = xor_accumulator
    return the_single_number


def bit_manipulation_count_set_bits(number: int) -> int:
    """
    Template: Brian Kernighan's algorithm — count '1' bits efficiently.

      KEY INSIGHT: n & (n-1) always clears the lowest set bit.
    Count how many times we can do this before reaching 0.

    Time: O(number of set bits)  |  Space: O(1)
    """
    count_of_ones = 0

    while number != 0:
        number          = number & (number - 1)   #   Clear the lowest '1' bit
        count_of_ones  += 1

    return count_of_ones


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    QUICK REFERENCE: PATTERN DECISION GUIDE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Problem says...                             → Use this pattern
─────────────────────────────────────────────────────────────────────────────
"longest/shortest subarray/substring"       →  Sliding Window
"pair/triplet in sorted array"              →  Two Pointers
"find in sorted array / minimize X"         →   Binary Search
"count/group/lookup previous values"        →    Hash Map
"tree traversal / path problems"            →  Tree DFS/BFS
"count ways / min cost / optimal value"     →   Dynamic Programming
"linked list cycle / middle / reverse"      →  Linked List /   Fast&Slow
"next greater / valid brackets"             →  Stack
"range sum queries"                         →  Prefix Sum
"generate all combinations/permutations"   →    Backtracking
"connected components / shortest path"     →   Graph DFS/BFS
"Kth largest / top K"                       →   Heap
"overlapping intervals"                     →  Merge Intervals
"duplicate / XOR tricks"                    →   Bit Manipulation
─────────────────────────────────────────────────────────────────────────────
"""
