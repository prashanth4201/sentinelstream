def ml_score(txn):
    # dummy ML logic
    if txn.amount > 10000:
        return -0.6
    return 0.2
