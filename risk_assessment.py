"""
A simple risk assessment engine for financial transactions. It evaluates transactions based on predefined rules and assigns a risk score, 
which is then categorized into risk levels with corresponding actions.
This script includes:
- Base rules with simple comparisons (e.g., amount thresholds, country checks).
- Custom rules that require more than one comparison logic (e.g., new users making large transactions).
- A scoring system to quantify risk and determine appropriate actions (approve, review, reject).
"""
import random

# Thresholds
NEW_USER_AMOUNT_THRESHOLD = 5000
HIGH_AMOUNT_THRESHOLD = 10000
RISKY_COUNTRIES = {"NG", "PK", "RU"}
FAILED_ATTEMPTS_THRESHOLD = 3
HIGH_VELOCITY_THRESHOLD = 5


# Base rule with comparisons
BASE_RULE_SET = {
    # High amount transactions
    "HIGH_AMOUNT": {
        "trx_key": "amount",
        "operator": ">",
        "value": HIGH_AMOUNT_THRESHOLD,
        "score": 40,
    },
    # Transactions from risky countries
    "RISKY_COUNTRY": {
        "trx_key": "country",
        "operator": "in",
        "value": RISKY_COUNTRIES,
        "score": 30,
    },
    # Multiple failed attempts
    "FAILED_ATTEMPTS": {
        "trx_key": "failed_attempts",
        "operator": ">=",
        "value": FAILED_ATTEMPTS_THRESHOLD,
        "score": 35,
    },
    # High velocity of transactions
    "HIGH_VELOCITY": {
        "trx_key": "recent_trx_count",
        "operator": ">=",
        "value": HIGH_VELOCITY_THRESHOLD,
        "score": 30,
    }
}

# Custom rule function for new users making large transactions
def new_user_large_trx(trx: dict) -> bool:
    return trx["is_new_user"] and trx["amount"] > NEW_USER_AMOUNT_THRESHOLD

# Custom rules that require more than one comparison logic
MULTIPLE_RULE_SET = {
    "NEW_USER_LARGE_TRX": {
        "function": new_user_large_trx,
        "score": 25,
    }
}

# Operators mapping
OPERATORS = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "in": lambda a, b: a in b,
}

# Risk thresholds for final scoring
RISK_THRESHOLDS = [
    (80, "High", "REJECT"),
    (50, "Medium", "REVIEW"),
    (0,  "Low", "APPROVE"),
]


def calculate_risk_score(trx: dict):
    """
    Calculate the risk score for a transaction based on defined rules.
    
    Args:
        trx (dict): A dictionary containing transaction details.
    
    Returns:
        int: The calculated risk score.
        list: List of triggered rules.
    """
    triggered = []
    score = 0

    for rule_name, rule in BASE_RULE_SET.items():
        operator = OPERATORS[rule["operator"]]
        trx_value = trx[rule["trx_key"]]
        compre_value = rule["value"]

        if operator(trx_value, compre_value):
            score += rule["score"]
            triggered.append(rule_name)
    
    for rule_name, rule in MULTIPLE_RULE_SET.items():
        if rule["function"](trx):
            score += rule["score"]
            triggered.append(rule_name)

    return score, triggered


def determine_risk_level(score: int):
    """
    Determine the risk level and recommended action based on the calculated score.
    Args:
        score (int): The calculated risk score.
    Returns:
        tuple: A tuple containing the risk level (str) and recommended action (str).
    """
    for threshold, level, action in RISK_THRESHOLDS:
        if score >= threshold:
            return level, action


def main():
    # Generate random transaction data for testing
    transaction = {
        "amount": random.randint(1000, 20000),
        "country": random.choice(["NG", "PK", "RU", "US", "GB"]),
        "is_new_user": random.choice([True, False]),
        "failed_attempts": random.randint(0, 5),
        "recent_trx_count": random.randint(0, 10)
    }

    # Calculate risk score and triggered rules
    risk_score, triggered_rules = calculate_risk_score(transaction)
    # Determine risk level and recommended action based on the risk score
    risk_level, action = determine_risk_level(risk_score)

    print(f"=====Transaction Details=====")
    print(f"Amount: {transaction['amount']} USD")
    print(f"Country: {transaction['country']}")
    print(f"Is New User: {transaction['is_new_user']}")
    print(f"Failed Attempts: {transaction['failed_attempts']}")
    print(f"Recent Transaction Count: {transaction['recent_trx_count']}")
    print(f"==============================")
    print(f"Risk Score: {risk_score}")
    print(f"Triggered Rules: {triggered_rules}")
    print(f"Risk Level: {risk_level}")
    print(f"Recommended Action: {action}")


if __name__ == "__main__":
    main()
