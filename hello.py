# import heapq

# class Node:
#     """Represents a node in the decision tree for branch and bound."""
#     def __init__(self, level, profit, weight, bound, selected):
#         self.level = level  # Current investment index
#         self.profit = profit  # Current return value
#         self.weight = weight  # Current total cost
#         self.bound = bound  # Upper bound of max profit
#         self.selected = selected  # List of selected investments

#     def __lt__(self, other):
#         return self.bound > other.bound  # Max heap (priority queue)

# def bound(node, n, budget, investments):
#     """Calculate upper bound of max possible return for a given node."""
#     if node.weight >= budget:
#         return 0  # If budget exceeded, bound is 0

#     profit_bound = node.profit
#     j = node.level + 1
#     total_weight = node.weight

#     while j < n and total_weight + investments[j].cost <= budget:
#         total_weight += investments[j].cost
#         profit_bound += investments[j].return_value
#         j += 1

#     if j < n:
#         profit_bound += (budget - total_weight) * (investments[j].return_value / investments[j].cost)

#     return profit_bound
    
# class Investment:
#     def __init__(self, name, cost, return_value):
#         self.name = name
#         self.cost = cost
#         self.return_value = return_value

# # Example investment options
# investments = [
#     Investment("Stocks A", 50000, 70000),
#     Investment("Stocks B", 60000, 80000),
#     Investment("Bonds C", 40000, 50000),
#     Investment("Real Estate D", 100000, 150000),
#     Investment("Gold E", 30000, 40000)
# ]

# budget = 150000  # Budget (knapsack capacity)

# # Run the optimizer
# selected_investments, max_return = knapsack_branch_bound(investments, budget)

# # Display the best investment plan
# print("\nOptimal Investment Portfolio:")
# for inv in selected_investments:
#     print(f"- {inv.name} (Cost: ₹{inv.cost}, Expected Return: ₹{inv.return_value})")

# print(f"\nTotal Expected Return: ₹{max_return}")

# def knapsack_branch_bound(investments, budget):
#     """Solves the 0/1 knapsack problem using Branch and Bound."""
#     investments.sort(key=lambda x: x.return_value / x.cost, reverse=True)  # Sort by return-to-cost ratio

#     n = len(investments)
#     priority_queue = []
#     max_profit = 0
#     best_selection = []

#     root = Node(level=-1, profit=0, weight=0, bound=0, selected=[])
#     root.bound = bound(root, n, budget, investments)
#     heapq.heappush(priority_queue, root)

#     while priority_queue:
#         node = heapq.heappop(priority_queue)

#         if node.bound > max_profit:
#             next_level = node.level + 1

#             if next_level < n:
#                 left_child = Node(next_level, node.profit + investments[next_level].return_value,
#                                   node.weight + investments[next_level].cost, 0,
#                                   node.selected + [investments[next_level]])

#                 left_child.bound = bound(left_child, n, budget, investments)

#                 if left_child.weight <= budget and left_child.profit > max_profit:
#                     max_profit = left_child.profit
#                     best_selection = left_child.selected

#                 if left_child.bound > max_profit:
#                     heapq.heappush(priority_queue, left_child)

#                 right_child = Node(next_level, node.profit, node.weight, 0, node.selected)
#                 right_child.bound = bound(right_child, n, budget, investments)

#                 if right_child.bound > max_profit:
#                     heapq.heappush(priority_queue, right_child)

#     return best_selection, max_profit

# # Run the optimizer
# selected_investments, max_return = knapsack_branch_bound(investments, budget)

# # Display the best investment plan
# print("\nOptimal Investment Portfolio:")
# for inv in selected_investments:
#     print(f"- {inv.name} (Cost: ₹{inv.cost}, Expected Return: ₹{inv.return_value})")

# print(f"\nTotal Expected Return: ₹{max_return}")
