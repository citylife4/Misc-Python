import requests
import datetime
import names
from time import sleep
from random import Random
import random
import copy
import threading
import logging


visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

mastercardPrefixList = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

amexPrefixList = [['3', '4'], ['3', '7']]

discoverPrefixList = [['6', '0', '1', '1']]

dinersPrefixList = [
        ['3', '0', '0'],
        ['3', '0', '1'],
        ['3', '0', '2'],
        ['3', '0', '3'],
        ['3', '6'],
        ['3', '8']]

enRoutePrefixList = [['2', '0', '1', '4'], ['2', '1', '4', '9']]

jcbPrefixList = [['3', '5']]

voyagerPrefixList = [['8', '6', '9', '9']]


def completed_number(rnd, prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(rnd.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, howMany):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(rnd, ccnumber, length))

    return result


def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)



def send_info(name, runs):
    for i in range(runs):
        generator = Random()
        generator.seed()        # Seed from current time
        card = list()

        type_card   = random.randint(0,2)
        card_number = random.randint(0,9)

        card.append(credit_card_number(generator, mastercardPrefixList, 16, 10))
        card.append(credit_card_number(generator, visaPrefixList, 16, 10))
        #card.append(credit_card_number(generator, visaPrefixList, 13, 10))
        card.append(credit_card_number(generator, amexPrefixList, 15, 10))

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2030, 2, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        #print(random_date.strftime("%m/%Y"))


        send_json = {
            "fname": names.get_first_name(),
            "lname": names.get_last_name(),
            "card": str(int(float(card[type_card][card_number]))),
            "exp": random_date.strftime("%m/%Y"),
            "cvv": random.randint(100,999)
        }

        logging.info("Sending %s: %s", name, send_json)
        while True:
            exita = 0
            try:
                r = requests.post('https://merceriacandelaria.es/wp-includes/images/-/manage/send/card.php', json=send_json)
                logging.info("Sending %s: %i", name, r.status_code)
                exita = 1
            except:
                logging.info("Sending %s: Problems", name)
                sleep(2)
            if exita:
                break


#for i in range(runs):
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    runs = 1000
    threads = 100
    for i in range(threads):
        x = threading.Thread(target=send_info, args=(i,runs))
        x.start()