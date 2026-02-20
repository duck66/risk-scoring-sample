import random

def new_user_large_tx(tx):
    return tx["is_new_user"] and tx["amount"] > 5000


BASE_RULE_SET = {
    "HIGH_AMOUNT": {
        "trx_key": "amount",
        "operator": ">",
        "value": 10000,
        "score": 40,
    },
    "RISKY_COUNTRY": {
        "trx_key": "country",
        "operator": "in",
        "value": {"NG", "PK", "RU"},
        "score": 30,
    },
    "FAILED_ATTEMPTS": {
        "trx_key": "failed_attempts",
        "operator": ">=",
        "value": 3,
        "score": 35,
    },
    "HIGH_VELOCITY": {
        "trx_key": "recent_tx_count",
        "operator": ">=",
        "value": 5,
        "score": 30,
    }
}

MULTIPLE_RULE_SET = {
    "NEW_USER_LARGE_TX": {
        "function": new_user_large_tx,
        "score": 25,
    }
}

OPERATORS = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "in": lambda a, b: a in b,
}

def calculate_risk_score(tx):
    triggered = []
    score = 0

    for rule_name, rule in BASE_RULE_SET.items():
        if OPERATORS[rule["operator"]](tx[rule["trx_key"]], rule["value"]):
            score += rule["score"]
            triggered.append(rule_name)
    
    for rule_name, rule in MULTIPLE_RULE_SET.items():
        if rule["function"](tx):
            score += rule["score"]
            triggered.append(rule_name)
    return score, triggered


def determine_risk_level(score):
    if score >= 80:
        level = 'High'
        action = 'REJECT'
    elif score >= 50:
        level = 'Medium'
        action = 'REVIEW'
    else:
        level = 'Low'
        action = 'APPROVE'
    return level, action


def main():
    # Sample transaction data
    transaction = {
        "amount": random.randint(1000, 20000),
        "country": random.choice(["NG", "PK", "RU", "US", "GB"]),
        "is_new_user": random.choice([True, False]),
        "failed_attempts": random.randint(0, 5),
        "recent_tx_count": random.randint(0, 10)
    }

    risk_score, triggered_rules = calculate_risk_score(transaction)
    risk_level, action = determine_risk_level(risk_score)

    print(f"Transaction: {transaction}")
    print(f"Risk Score: {risk_score}")
    print(f"Triggered Rules: {triggered_rules}")
    print(f"Risk Level: {risk_level}")
    print(f"Recommended Action: {action}")


if __name__ == "__main__":
    main()
