# -*- coding: iso-8859-15 -*-
"""
Must have python, chrome, and selenium installed.
Download the chrome driver from here http://code.google.com/p/chromedriver/downloads/list
Enter your email address, password, and the location of the chrome driver below.
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

# PUT YOUR INFORMATION HERE
email = 'email@gmail.com'
password = 'password'
chromedriver = r'C:/Data/computer and tech/python/adventurito/chromedriver.exe'


credentials = [(email, password)]
base_url = "https://chipotle.promo.eprize.com"
timeout = 5
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(timeout)
driver.set_window_position(2000, 100)
driver.get(base_url + "/20th/")


def get_puzzles():
    puzzles = {1: (text_fields, ['pork utopia']),
               2: (text_fields, ['48.872007', '2.340091']),
               3: (text_fields, ['13', '2013', '20', '7305', '3', '2', '411', '140', '2', '20', '10', '20', '50', '2063']),
               4: (text_fields, ['supersized pig on steroids']),
               5: (combo_sentences, ["Usually when you roll something ~this good, ~it's illegal.",
                                     "~The Happy Pill. Now ~in ~a 567,000mg dose.",
                                     "Open wide, no wider.",
                                     "~The gourmet restaurant where ~you eat with your hands.",
                                     "They beep when they backup."]),
               6: (text_fields, ['Alex', 'Steve', 'Monty']),
               7: (text_fields, ['758524899876']),
               8: (text_fields, ['Wiers Farm']),
               9: (text_fields, ['1993']),
               10: (text_fields, ['Guacamole']),
               11: (text_fields, ['36']),
               12: (text_fields, ['Omnivore']),
               13: (text_fields, ['40', '8', '36', '16', '10']),
               14: (solve_14, ['First', 'Start', 'IPO', 'No']),
               15: (text_fields, ['Acidosis']),
               16: (text_fields, ['Greedy']),
               17: (text_fields, ['I81UCN2']),
               18: (text_fields, ['Bestfriends', 'Blitzen Trapper', 'LP', 'Youngblood Hawke']),
               19: (nothing, []),
               20: (solve_20, [])}
    return puzzles


def main():
    for username, password in credentials:
        login(username, password)

        if check_final_challenge():
            solve_20_part_2()
        elif check_you_made_it():
            pass
        else:
            for puzzle_num in range(1, 21):
                hover_over_puzzles()
                if puzzle_already_solved(puzzle_num):
                    continue
                select_puzzle(puzzle_num)
                solve_puzzle(puzzle_num)
        logout()


def check_final_challenge():
    return check_exists(driver.find_element_by_xpath, "//div[.='20. The Final-Final Challenge']")


def check_you_made_it():
    return check_exists(driver.find_element_by_xpath, "//p[.='PHEW, YOU MADE IT.']")


def login(username, password):
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("chipotle_password").send_keys(password)
    driver.find_element_by_id("loginButton").click()


def logout():
    element = driver.find_element_by_xpath("//strong[@class='user_name']")
    action_chain = ActionChains(driver)
    action_chain.move_to_element(element)
    action_chain.perform()
    driver.find_element_by_xpath("//a[@href='./']").click()


def popup():
    if check_exists(driver.find_element_by_id, 'introContent'):
        element = driver.find_element_by_id('introContent')
        element_class = str(element.get_attribute('class'))
        if element_class == 'container reg chippie haunting updateForm notEmailOpted notMobileOpted':
            print 'Stupid pop up'
            driver.find_element_by_id("introClose").click()


def hover_over_puzzles():
    element = driver.find_element_by_id("puzzlesSolvedCopy")
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()


def puzzle_already_solved(puzzle_num):
    element = driver.find_element_by_id("puzzleToken_{0}".format(puzzle_num))
    element_class = str(element.get_attribute('class'))

    if element_class == 'token  yes_solved solved':
        print 'Puzzle {0} already solved.'.format(puzzle_num)
        solved = True
    elif element_class == 'token  not_solved available':
        print 'Puzzle {0} not solved.'.format(puzzle_num)
        solved = False
    elif element_class == 'token  not_solved locked':
        print 'Puzzle {0} locked.'.format(puzzle_num)
        solved = True
    else:
        raise Exception('unexpected class for puzzle token')

    return solved


def select_puzzle(puzzle_num):
    print 'Selecting puzzle {0}'.format(puzzle_num)
    if puzzle_num == 20:
        time.sleep(2)
        driver.find_element_by_id("puzzleIcon20").click()
        time.sleep(10)
    else:
        driver.find_element_by_id("puzzleToken_{0}".format(puzzle_num)).click()

    element = driver.find_element_by_id("puzzleTitle")
    if not element.text.split('.')[0] == str(puzzle_num):
        raise Exception('Puzzle {0} not loaded'.format(puzzle_num))


def check_exists(find_function, find_arg):
    driver.implicitly_wait(2)
    try:
        find_function(find_arg)
    except NoSuchElementException:
        return False
    finally:
        driver.implicitly_wait(timeout)
    return True


def check_correct(puzzle_num):
    if check_exists(driver.find_element_by_class_name, "correct_banner"):
        print 'Puzzle {0} correctly solved.'.format(puzzle_num)
    elif check_exists(driver.find_element_by_class_name, "incorrect_answer"):
        raise Exception('Puzzle {0} answer was incorrect.'.format(puzzle_num))
    elif check_you_made_it():
        print 'YOU MADE IT!'
    else:
        raise Exception('solution banner not found')


def submit(puzzle_num):
    if puzzle_num == 5:
        element = driver.find_element_by_class_name("submit_puzzle5_button")
    elif puzzle_num == 14:
        element = driver.find_element_by_id("puzzle_submit_button")
    elif puzzle_num == 19:
        element = driver.find_element_by_id("submit_puzzle_no")
    elif puzzle_num == 20:
        return
    else:
        element = driver.find_element_by_id("submit_puzzle")

    if element.is_enabled():
        element.click()
    else:
        raise Exception('Submit button not enabled')


def solve_puzzle(puzzle_num):
    puzzles = get_puzzles()
    print 'Solving Puzzle {0}'.format(puzzle_num)
    puzzles[puzzle_num][0](puzzles[puzzle_num][1])
    submit(puzzle_num)
    check_correct(puzzle_num)


def nothing(empty_list):
    pass


def text_fields(answers):
    for num, answer in enumerate(answers, start=1):
        driver.find_element_by_id("puzzle_answer{0}".format(num)).send_keys(answer)


def combo_box(box_name, choice):
    driver.find_element_by_xpath("//a[@class='select'][@data-name='{0}']".format(box_name)).click()
    driver.find_element_by_xpath("//li[@data-value='{0}' "
                                 "and ancestor-or-self::*[@data-for='{1}']]".format(choice, box_name)).click()


def combo_sentence(q_num, sentence):
    words = [x for x in sentence.split(' ') if not x.startswith('~')]
    for num, word in enumerate(words, start=1):
        fixed_word = word.lower().rstrip('.').rstrip(',')
        print 'Combo box', fixed_word
        combo_box('q{0}_option{1}'.format(q_num, num), fixed_word)


def combo_sentences(sentences):
    for num, sentence in enumerate(sentences, start=1):
        combo_sentence(num, sentence)


def solve_14(event_names):
    image_size = 186
    offsets = [2 * image_size, 2 * image_size, image_size, image_size]
    for event_name, offset in zip(event_names, offsets):
        element = driver.find_element_by_xpath("//li[@data-id='{0}']".format(event_name))
        action_chain = ActionChains(driver)
        action_chain.click_and_hold(element)
        action_chain.move_by_offset(-offset, 0)
        action_chain.release()
        action_chain.perform()


def solve_20(empty_list):
    solve_20_part_1()
    driver.find_element_by_id("submit_puzzle").click()
    time.sleep(1)
    driver.find_element_by_id("really_submit_puzzle").click()
    solve_20_part_2()
    driver.find_element_by_id("submit_puzzle").click()
    time.sleep(1)
    driver.find_element_by_id("really_submit_puzzle").click()


def solve_20_part_1():
    answers = ['28 to 1',
               '25',
               '$115.56',
               "McDonald’s",
               "Chipotle’s rejection of the sub-therapeutic use of antibiotics in animals",
               'Chopped All-Stars',
               'Fajita Vegetables',
               'Chez Panisse',
               'Russ Kremer',
               '350',
               'Large rope handle bag',
               'Ohio, Minnesota, Kansas, Missouri, Arizona',
               '$22.00',
               'The Beatles',
               'Simon Cowell',
               'SWV (Sisters With Voices) – “Weak”',
               'THE GOURMET RESTAURANT WHERE YOU EAT WITH YOUR HANDS.',
               'GM2',
               'Bruce']

    for answer in answers:
        print 'selecting', answer
        element = driver.find_element_by_id('puzzle_copy')
        action_chain = ActionChains(driver)
        action_chain.move_to_element(element)
        action_chain.perform()

        element = driver.find_element_by_xpath("//label["
                                               ".='A. {0}' or "
                                               ".='B. {0}' or "
                                               ".='C. {0}' or "
                                               ".='D. {0}' or "
                                               ".='E. {0}']"
                                               "/preceding-sibling::*[1]".format(answer))

        location = element.location
        driver.execute_script("window.scrollTo({0}, {1});".format(location['x'], location['y'] - 500))
        element.click()


def solve_20_part_2():
    sentences = ['STEVE', 'ELLS', 'FOUNDED', 'CHIPOTLE', 'IN', 'CO', 'IN', '1993',
                 'THE', 'FIRST', 'MENU', 'DID', 'NOT', 'HAVE', 'BARBACOA',
                 'IN', 'FACT', 'THERE', 'WERE', 'NO', 'MENU', 'BOARDS', 'AT', 'ALL',
                 'HAPPY', '20TH', 'CHIPOTLE']

    for word_num, word in enumerate(sentences, start=1):
        for letter_num, letter in enumerate(word, start=1):
            element = driver.find_element_by_xpath("//div[@id='word{0}']/*[{1}]".format(word_num, letter_num))

            location = element.location
            driver.execute_script("window.scrollTo({0}, {1});".format(location['x'], location['y'] - 500))

            element.click()
            element.send_keys(Keys.DELETE)
            element.send_keys(letter)


if __name__ == '__main__':
    main()