def analyze(
        revenue,
        cost):

    margin = revenue - cost

    if margin < 30000:
        return (
            "Risk Alert: "
            "Low margin detected."
        )

    return (
        "Project healthy."
    )

result = analyze(
    120000,
    95000
)

print(result)