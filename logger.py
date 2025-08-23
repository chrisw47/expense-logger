import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

input_month = input('Please enter the month you\'d like to log in \"YYYY-MM\" format.')
EXP_MONTH = pd.to_datetime(input_month).to_period('M')  # set month of expense

mapping = {1: 'Basic life expenses',
           2: 'Health',
           3: 'Investments',
           4: 'Misc. Wants',
           5: 'Subscriptions',
           6: 'Transportation',
           7: 'Income',
           ' ': ' '
           }

mapping_inverse = {'Basic life expenses': 1,
                   'Health': 2,
                   'Investments': 3,
                   'Misc. Wants': 4,
                   'Subscriptions': 5,
                   'Transportation': 6,
                   'Income': 7,
                   ' ': ' '
                   }


def initialize(expenses_file):
    '''
    ## Initialize file

    Initializes an expenses file. If user input is `None`, then it creates a new pandas `dataframe`. Otherwise, it reads
    the inputted expense file and converts it into a `dataframe` before returning.
    '''
    return pd.DataFrame(columns=['Expense Name', 'Expense Class', 'Change in Net Worth']) if expenses_file is None else pd.read_excel(expenses_file, names=['Expense Name', 'Expense Class', 'Change in Net Worth'])


def update_expenses(expenses_file, expenses_dict):
    '''
    ## Update expense log

    Once an expenses file is selected, this function checks to see whether it has more than one row. If it does, it will
    prune the last row, which should contain the total expenditure from previous expense log updates. From there, it takes
    a dictionary corresponding to the new expenses — contains three keys and *n* values corresponding to each key for
    *n* expenses — and concatenates it to the file.
    '''

    if len(expenses_file['Expense Name']) > 1:
        expenses_file = expenses_file[:-1]  # Remove the last row

    expenses_file['Expense Class'] = expenses_file['Expense Class'].map(
        mapping_inverse)
    expenses_file = pd.concat(
        [expenses_file, pd.DataFrame(expenses_dict)], ignore_index=True)
    expense_total = {'Expense Name': 'Net', 'Expense Class': ' ',
                     'Change in Net Worth': sum(expenses_file['Change in Net Worth'])}
    expenses_file = pd.concat(
        [expenses_file, pd.DataFrame([expense_total])], ignore_index=True)  # concat new expense inputs

    expenses_file['Expense Class'] = expenses_file['Expense Class'].map(
        mapping)  # apply mapping for readability

    return expenses_file


def update_totals(date, totals_file: pd.ExcelFile, total_income, total_expenses, delta_networth) -> pd.DataFrame:
    '''
    Updates parameters for monthly totals, to be used when plotting month-on-month trends.  

    `date`: takes a datetime string defining the year and month of relevant expenses.

    `totals_file`: file containing monthly totals as an Excel file.

    `total_income`: total income for that month.

    `total_expenses`: total expenses for that month.

    `delta_networth`: change in net worth for that month.

    Returns a dataframe object that can be easily converted to Excel.
    '''

    df = pd.DataFrame(columns=['Month', 'Income', 'Total Expenses', 'Approx. Change in Net Worth']) if totals_file is None else pd.read_excel(
        totals_file, names=['Month', 'Income', 'Total Expenses', 'Approx. Change in Net Worth'])
    to_add = {'Month': date,
              'Income': total_income,
              'Total Expenses': total_expenses,
              'Approx. Change in Net Worth': delta_networth
              }

    df = df[df['Month'] != date]
    df = pd.concat([df, pd.DataFrame([to_add])], ignore_index=True)

    return df


def clean_expenses(expense_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Simple expense cleaning to yeet out Income and Net Worth change columns.
    '''

    df = expense_df
    df = df[df['Expense Class'] != 'Income']
    cleaned = df[df['Expense Name'] != 'Net']
    return cleaned


def plot_expenses(cleaned_df: pd.DataFrame) -> np.ndarray:
    '''
    Obtains unique expenditure labels and corresponding amounts for that month using a `DataFrame` cleaned by `clean_expenses` method, then plots everything on a pie chart with specific labels and total expenditure annotated in the bottom right of the chart.
    '''

    labels = cleaned_df['Expense Class'].sort_values(ascending=True).unique()
    amounts = -np.array([sum(cleaned_df['Change in Net Worth']
                        [cleaned_df['Expense Class'] == category]) for category in labels])

    def autopct_fn(val):  # autopct function to display absolute values instead of percentages
        return f'${np.round(val/100*amounts.sum(),2)}'

    fig, ax = plt.subplots()
    colors = ['lightcoral', 'peachpuff', 'lemonchiffon',
              'palegreen', 'lightskyblue', 'lavender']  # color map
    ax.pie(amounts, labels=labels,
           autopct=autopct_fn, colors=colors)
    plt.text(
        0.75, -1.3, f'Total: ${np.round(amounts.sum(), 2)}', fontsize=12)
    plt.title('Expenses pie chart for ' + str(EXP_MONTH) + '.', fontsize=14)
    plt.savefig(str(EXP_MONTH) + ' pie chart.png', dpi=350)
    plt.show()

    return amounts


def calculate_monthly_totals(exp_df: pd.DataFrame, cleaned_df: pd.DataFrame, monthly_file) -> pd.DataFrame:
    '''
    Updates monthly totals on income, change in net worth, and total costs. Returns a `DataFrame` object.
    '''

    chart_amounts = plot_expenses(cleaned_df)
    income, change_in_net_worth = sum(exp_df['Change in Net Worth'][exp_df['Expense Class'] == 'Income']), sum(
        exp_df['Change in Net Worth'][exp_df['Expense Name'] != 'Net'])
    total_costs = np.round(chart_amounts.sum(), 2)

    return update_totals(str(EXP_MONTH), monthly_file, income, total_costs, change_in_net_worth)

def plot_monthly_trends(monthly_expenses: pd.DataFrame):
    '''
    Takes a monthly trends file (in this code, its variable name is `total_init` below) and plots income, total expenses, and change in net worth as a function of month.
    '''

    df = monthly_expenses
    x, y_inc, y_exp, y_delta = df['Month'], df['Income'], df['Total Expenses'], df['Approx. Change in Net Worth']

    plt.figure(figsize=(9,6), facecolor='lightcyan', edgecolor='lightskyblue', layout='constrained')
    plt.plot(x, y_inc, marker='o', linestyle='--', c='deepskyblue', label='Income')
    plt.plot(x, y_exp, marker='o', linestyle='--', c='maroon', label='Total Expenses')
    plt.plot(x, y_delta, marker='o', linestyle='--', c='chartreuse', label='Change in Net Worth')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Dollar amount ($)', fontsize=12)
    plt.ylim(bottom=0)
    plt.title('Monthly Plots for Income, Total Expenses, and Change in Net Worth.', fontsize=14)
    plt.legend(fontsize=11)
    plt.savefig('monthly-totals.png', dpi=400)
    plt.show()


expense_dict = {
    'Expense Name': ['Income',
                     'Rent'],
    'Expense Class': [7,
                      1],
    'Change in Net Worth': [3000,
                            -1400]
}

if __name__ == "__main__":
    # Clean data to exclude total and income for expense visualization

    expense_init = input(
        'Name the expense file you would like to update. If you want to initialize a file, write None.')  # takes user input
    totals_init = input(
        'Name the monthly totals file you would like to use/update. If you want to initialize a file, write None.')

    if expense_init == 'None':  # Change None inputs to `None`.
        expense_init = None

    if totals_init == 'None':
        totals_init = None
    

    expense_file = initialize(expense_init)
    expense_file = update_expenses(
        expense_file, expense_dict)  # update expenses log

    cleaned_expenses = clean_expenses(expense_file)

    monthly_totals = calculate_monthly_totals(
        expense_file, cleaned_expenses, totals_init)
    
    plot_monthly_trends(monthly_totals)
    expense_file.to_excel(str(EXP_MONTH) + '.xlsx', index=False)
    monthly_totals.to_excel('monthly totals.xlsx', index=False)


# # # Example expense dictionaries

# expense_dict = {
#     'Expense Name': ['Income 12/1-12/15',
#                      'Rent',
#                      'Groceries',
#                      'Roth IRA contribution',
#                      'Misc. foods',
#                      'Subs (overleaf, spotify, etc.)',
#                      'Gas'],
#     'Expense Class': [7,
#                       1,
#                       1,
#                       3,
#                       4,
#                       5,
#                       6],
#     'Change in Net Worth': [3000,
#                             -1400,
#                             -150,
#                             -500,
#                             -250,
#                             -40,
#                             -80]
#     }

# expense_dict = {
#     'Expense Name': ['Income 12/15-12/31',
#                      'Groceries',
#                      'Gas',
#                      'Registration for Half Marathon'],
#     'Expense Class': [7,
#                       1,
#                       6,
#                       2],
#     'Change in Net Worth': [3000,
#                             -250,
#                             -70,
#                             -150]
# }