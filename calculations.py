


import math

def calculate_averaging(current_qty, current_avg_price, market_price, target_avg_price):
    total_cost = current_qty * current_avg_price

    if target_avg_price == market_price:
        shares_to_buy, new_avg = 0, current_avg_price
    elif target_avg_price > market_price:
        numerator = target_avg_price * current_qty - total_cost
        denominator = market_price - target_avg_price
        if denominator == 0 or numerator / denominator < 0:
            return None, None, None
        shares_to_buy = math.ceil(numerator / denominator)
    else:
        numerator = total_cost - target_avg_price * current_qty
        denominator = target_avg_price - market_price
        if denominator == 0 or numerator / denominator < 0:
            return None, None, None
        shares_to_buy = math.ceil(numerator / denominator)

    new_total_qty = current_qty + shares_to_buy
    if new_total_qty == 0:
        return None, None, None

    new_avg = (total_cost + shares_to_buy * market_price) / new_total_qty
    estimated_profit = (target_avg_price - new_avg) * new_total_qty

    return shares_to_buy, new_avg, estimated_profit
