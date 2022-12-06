import machine
from machine import *


def check_resources(ingredients):
    for ingredient in ingredients:
        available_ingredient = resources[ingredient]
        needed_ingredient = ingredients[ingredient]
        if needed_ingredient > available_ingredient:
            print(f"Sorry, not enough {ingredient}")
            return False
    return True


def process_payment():
    total = 0
    adding_coins = True
    while adding_coins:
        inserted_coin = input("Insert coins:\n'10c', '20c', '50c', '1e' or '2e'. Type 'c' to cancel")
        if inserted_coin != "c" and inserted_coin in coin_values:
            total += coin_values[inserted_coin]
            print(f"Order price: {MENU[order]['cost']}. Current credits: {total}.")
            if total >= MENU[order]['cost']:
                answer = input(f"Type 'pay' to confirm or 'c' to cancel").lower()
                if answer == "pay":
                    return total
                else:
                    print(f"Payment cancelled. {round(total, 2)}e  refunded.")
                    return
        elif inserted_coin == "c":
            print(f"Payment cancelled. {round(total, 2)}e  refunded.")
            return
        else:
            exit("You broke it!... Shutting down...")


def finalize_order(received_money, order_price, order_recipe):
    if received_money >= order_price:
        refund = received_money - order_price
        machine.profit += order_price
        for item in order_recipe:
            resources[item] -= order_recipe[item]
        return print(f"Enjoy your {order}! ({refund}€ refunded.)")


is_on = True

while is_on:
    order = input("What would you like? (espresso/latte/cappuccino):\n").lower()
    if order == "off":
        is_on = False
    elif order == "report":
        for resource in resources:
            print(resource,  resources[resource])
        print("Profit: ", machine.profit)
    elif order in MENU:
        drink = MENU[order]['ingredients']
        cost = float(MENU[order]['cost'])
        if check_resources(drink):
            payment = process_payment()
            finalize_order(payment, cost, drink)


