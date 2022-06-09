from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure


# Zbiór funkcji wspomagający obsługę danych, w tym m.in. tworzenie wykresów

def get_outcome(json_list):
    outcome = 0
    for elem in json_list:
        if elem['is_outcome']:
            outcome += elem['amount']
    return round(outcome, 2)


def get_income(json_list):
    income = 0
    for elem in json_list:
        if not elem['is_outcome']:
            income += elem['amount']
    return round(income, 2)


def get_category(json_list, category):
    amount = 0
    for elem in json_list:
        if elem['category'] == category.value:
            if elem['is_outcome']:
                amount -= elem['amount']
            else:
                amount += elem['amount']
    return round(amount, 2)


def _get_plot(amount, json_list: list, figsize, dpi):
    amount += get_outcome(json_list)
    amount -= get_income(json_list)
    js_ls = json_list.copy()
    js_ls.reverse()
    seq = []
    x = []
    for i, elem in enumerate(js_ls):
        if elem['is_outcome']:
            amount -= elem['amount']
        else:
            amount += elem['amount']
        seq.append(amount)
        x.append(i)

    figure = Figure(figsize=figsize, dpi=dpi)
    axes = figure.add_subplot()
    axes.plot(x, seq, color='tab:blue')
    axes.set_title('Ostatnie 100 wpisów')
    axes.set_ylabel('stan konta')
    axes.xaxis.set_major_locator(MaxNLocator(integer=True))

    return figure


def get_plot(amount, json_list: list):
    return _get_plot(amount, json_list, (9, 4), 100)


def get_small_plot(amount, json_list: list):
    return _get_plot(amount, json_list, (5.85, 3.425), 75)
