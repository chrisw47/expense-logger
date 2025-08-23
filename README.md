# Expense Logger

A Python-based personal finance tracking tool that helps you log expenses, categorize spending, and visualize monthly financial data.

## Features

- **Expense Tracking**: Log and categorize expenses across different spending categories
- **Data Visualization**: Generate pie charts showing expense breakdown by category
- **Monthly Summaries**: Track income, expenses, and net worth changes over time
- **Excel Integration**: Read from and write to Excel files for data persistence

## Expense Categories

The system uses the following predefined categories:

1. Basic life expenses
2. Health
3. Investments
4. Misc. Wants
5. Subscriptions
6. Transportation
7. Income

You will need to write a dictionary containing your expenses in the form before running the main script:

```
expenses_dict = {
    'Expense Name': [list of expense names],
    'Expense Class': [list of expense classes adhering to predefined categories],
    'Change in Net Worth': [list of expense quantities; expenses have a negative sign while incomes are positive]
}
```

## Requirements

- pandas
- matplotlib
- numpy

Install dependencies:

```
pip install pandas matplotlib numpy
```

## Usage

Run the script:

```
python logger.py
```

The program will prompt you for:
1. **Expense file name**: Existing Excel file to update, or type "None" to create new
2. **Monthly totals file name**: File to track monthly summaries, or type "None" to create new

## File Structure

The program creates/updates two types of files:

## Monthly Expense File (`YYYY-MM.xlsx`)

Contains detailed expense records with columns:
- Expense Name
- Expense Class
- Change in Net Worth

## Monthly Totals File (`monthly totals.xlsx`)
Contains summary data with columns:

- Month
- Income
- Total Expenses
- Approx. Change in Net Worth

(note that this is still a work in progress, need to fix a small issues)

## Output

- **Excel files**: Updated expense logs and monthly summaries
- **Pie chart**: Visual breakdown of expenses saved as PNG file
- **Console display**: Interactive pie chart showing expense distribution

## Configuration

Edit the `EXP_MONTH` variable at the top of the file to set the target month:

```
EXP_MONTH = pd.to_datetime('2025-09').to_period('M')
```

Modify the `expense_dict` variable to add your specific expenses before running.

*Note that the auxiliary attached files are example monthly excel spreadsheets and monthly total trend graphs.*
