def calculate_risk_score(tx):
    triggered = []
    score = 0
    # Finance risk assessment based on transaction attributes
    if tx["amount"] > 10000:
        score += 40
        triggered.append("HIGH_AMOUNT")

    # Geographical risk based on country
    high_risk_countries = {"NG", "PK", "RU"}
    if tx["country"] in high_risk_countries:
        score += 30
        triggered.append("RISKY_COUNTRY")

    # User behavior risk
    if tx["is_new_user"] and tx["amount"] > 5000:
        score += 25
        triggered.append("NEW_USER_LARGE_TX")

    if tx["failed_attempts"] >= 3:
        score += 35
        triggered.append("FAILED_ATTEMPTS")

    # Velocity risk based on recent transaction count
    if tx["recent_tx_count"] >= 5:
        score += 30
        triggered.append("HIGH_VELOCITY")

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
        "amount": 15000,
        "country": "NG",
        "is_new_user": True,
        "failed_attempts": 2,
        "recent_tx_count": 6
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
