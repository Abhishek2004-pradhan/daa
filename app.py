from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

class Node:
    def __init__(self, level, profit, weight, bound, selected):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.selected = selected

    def __lt__(self, other):
        return self.bound > other.bound  # Max heap (priority queue)

def bound(node, n, budget, investments):
    if node.weight >= budget:
        return 0  
    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + investments[j]["cost"] <= budget:
        total_weight += investments[j]["cost"]
        profit_bound += investments[j]["return_value"]
        j += 1

    if j < n:
        profit_bound += (budget - total_weight) * (investments[j]["return_value"] / investments[j]["cost"])

    return profit_bound

def knapsack_branch_bound(investments, budget):
    investments.sort(key=lambda x: x["return_value"] / x["cost"], reverse=True)  # Sort by return-to-cost ratio
    n = len(investments)
    priority_queue = []
    max_profit = 0
    best_selection = []

    root = Node(level=-1, profit=0, weight=0, bound=0, selected=[])
    root.bound = bound(root, n, budget, investments)
    heapq.heappush(priority_queue, root)

    while priority_queue:
        node = heapq.heappop(priority_queue)

        if node.bound > max_profit:
            next_level = node.level + 1

            if next_level < n:
                left_child = Node(next_level, node.profit + investments[next_level]["return_value"],
                                  node.weight + investments[next_level]["cost"], 0,
                                  node.selected + [investments[next_level]])

                left_child.bound = bound(left_child, n, budget, investments)

                if left_child.weight <= budget and left_child.profit > max_profit:
                    max_profit = left_child.profit
                    best_selection = left_child.selected

                if left_child.bound > max_profit:
                    heapq.heappush(priority_queue, left_child)

                right_child = Node(next_level, node.profit, node.weight, 0, node.selected)
                right_child.bound = bound(right_child, n, budget, investments)

                if right_child.bound > max_profit:
                    heapq.heappush(priority_queue, right_child)

    return best_selection, max_profit

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    budget = int(data["budget"])
    investments = [{"name": item["name"], "cost": int(item["cost"]), "return_value": int(item["return_value"])}
                   for item in data["investments"]]

    selected_investments, max_return = knapsack_branch_bound(investments, budget)

    result = {
        "selected": selected_investments,
        "max_return": max_return
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run()


    
