
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# First, I read the CPI data and skipped the extra information at the top of the file.
# Note: The first 8 rows contain Bank of Canada information.
data = pd.read_csv("STATIC_INFLATIONCALC.csv", skiprows=8)

# Here, I made sure that the dates and CPI values were in the right format.
data["date"] = pd.to_datetime(data["date"])
data["STATIC_INFLATIONCALC"] = pd.to_numeric(data["STATIC_INFLATIONCALC"])

# Shortening the CPI column name makes things a lot easier, as learned in class.
data = data.rename(columns={"STATIC_INFLATIONCALC": "CPI"})

# It was required to find the yearly percentage change using the monthly CPI data. Python recommended pct_change!
# The data is monthly, so 12 months represent one year.
data["Annual Change"] = data["CPI"].pct_change(periods=12) * 100

# I aet up the graph to show how CPI has changed over time.
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(data["date"], data["CPI"], color="blue", label="CPI")
ax1.set_xlabel("Date")
ax1.set_ylabel("CPI")
ax1.set_title("Canadian Consumer Price Index and Annual Percentage Change")

# As instructed, I added a dotted line to show the base CPI level of 100. Easily done with axhline which I found by searching for reference lines in matplotlib,
ax1.axhline(y=100, color="gray", linestyle=":", label="Base Level (100)")

# Also as instructed, I used the right side of the graph for the annual percentage change with twinx. From class, I learned that a different color and line style is best for differentiation.
ax2 = ax1.twinx()
ax2.plot(
    data["date"],
    data["Annual Change"],
    color="orange",
    linestyle="--",
    label="Annual Percentage Change"
)
ax2.set_ylabel("Annual Percentage Change (%)")

# Here, both graph labels are in one legend so that everything is clear.
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2)

plt.tight_layout()

# Always save the finished graph!
plt.savefig("CPI_graph.png", dpi=300)
plt.show()

# Great use of old code with the loop to get the CPI value for a given date.
def get_cpi(date):
    """Find the CPI value using the month and year."""

    result = data.loc[
        (data["date"].dt.year == date.year) &
        (data["date"].dt.month == date.month),
        "CPI"
    ]

    if result.empty:
        return None

    return result.iloc[0]


# This code will not only ask for a price, but also make sure it is a valid positive number.
while True:
    try:
        price = float(input("Enter the price of the goods or services: $"))

        if not np.isfinite(price) or price <= 0:
            print("Please enter a price greater than zero.")
        else:
            break

    except ValueError:
        print("Please enter a valid number.")


# This will ask for the starting date and check that CPI data for it exists in the first place.
while True:
    first_date_input = input("Enter the first date (YYYY-MM-DD): ")

    try:
        first_date = pd.to_datetime(first_date_input, format="%Y-%m-%d")
        first_cpi = get_cpi(first_date)

        if first_cpi is None:
            print("Date is not available in the dataset.")
        else:
            break

    except (ValueError, OverflowError):
        print("Please enter a valid date in YYYY-MM-DD format.")


# Same thing as before, but for the second date, there's a check to make sure the second date is not earlier than the first date.
while True:
    second_date_input = input("Enter the second date (YYYY-MM-DD): ")

    try:
        second_date = pd.to_datetime(second_date_input, format="%Y-%m-%d")
        second_cpi = get_cpi(second_date)

        # Calculate the number of months between the two dates.
        number_of_months = (
            (second_date.year - first_date.year) * 12
            + (second_date.month - first_date.month)
        )

        if second_cpi is None:
            print("Date is not available in the dataset.")
        elif number_of_months < 0:
            print("The second date must not be earlier than the first date.")
        else:
            break

    except (ValueError, OverflowError):
        print("Please enter a valid date in YYYY-MM-DD format.")


# Here, we're calculating the percentage change in CPI.
percentage_change = ((second_cpi - first_cpi) / first_cpi) * 100

# Next, we're converting the number of months into years.
number_of_years = number_of_months / 12

# This will give the average yearly inflation rate, but if both dates are the same month, there's no point since there's no change.
if number_of_years == 0:
    annual_rate = None
else:
    annual_rate = (
        ((second_cpi / first_cpi) ** (1 / number_of_years)) - 1
    ) * 100

# Now, I've adjusted the original price using the change in CPI.
adjusted_price = price * (second_cpi / first_cpi)

# Finally, the results should show with clear labels and proper formatting.
print()
print("----- Inflation Calculator Results -----")
print(f"Original Price: ${price:,.2f} CAD")
print(f"First Period: {first_date.strftime('%Y-%m')}")
print(f"Second Period: {second_date.strftime('%Y-%m')}")
print(f"First Period CPI: {first_cpi:.1f}")
print(f"Second Period CPI: {second_cpi:.1f}")
print(f"Percentage Change: {percentage_change:.2f}%")
print(f"Number of Years: {number_of_years:.2f}")

if annual_rate is None:
    print("Annual Rate of Change: N/A (same month)")
else:
    print(f"Annual Rate of Change: {annual_rate:.2f}%")

print(f"Equivalent Price in Second Period: ${adjusted_price:,.2f} CAD")