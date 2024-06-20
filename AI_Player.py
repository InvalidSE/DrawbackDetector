# Play random moves via selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import time
import json

game_no = 0

# Set up the browser
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
browser = webdriver.Chrome(options=ChromeOptions)
browser.get('https://drawbackchess.com/')
browser.implicitly_wait(1)

# If empty, set up JSON file
with open("./drawbacks.json", "r") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        data = {"drawbacks": []}
        with open("./drawbacks.json", "w") as f:
            json.dump(data, f)
            print(f"[DRIVER] JSON file created.")

# Select AI game "Play vs AI"
try:
    print("[DRIVER] Starting...")

    browser.find_element(By.XPATH, '//*[text()="Intermediate"]').click()
    time.sleep(0.5)
    browser.find_element(By.XPATH, '//*[text()="Close"]').send_keys(Keys.ESCAPE)
    time.sleep(0.5)

    
    while True:
        game_no += 1
        print("[DRIVER] Starting game", game_no)
        browser.find_element(By.XPATH, '//*[text()="Play vs AI"]').click()
        time.sleep(1)
        browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div[2]/button[2]').click()
        time.sleep(2)
        print("[DRIVER] AI game selected.")
        
        # Get list of spans
        drawback_list = browser.find_elements(By.XPATH, "//*[contains(@class, 'handicap')]/div/span")
        drawback_text = ""
        
        for span in drawback_list:
            drawback_text += (" " + span.text)
        drawback_text = drawback_text.strip()
        drawback = {"title": drawback_text.split(":")[0], "description": drawback_text.split(":")[1].strip()}

        print("[DRIVER] Drawback:", drawback_text)

        # Add to JSON file
        with open("./drawbacks.json", "r") as f:
            data = json.load(f)
        with open("./drawbacks.json", "w") as f:
            if drawback["title"] not in data:
                data["drawbacks"].append(drawback)
                json.dump(data, f)
                print(f"[DRIVER] Drawback added to JSON file.")    
            else:
                print(f"[DRIVER] Drawback already in JSON file.")

        browser.get('https://drawbackchess.com/')
        time.sleep(1.5)

except Exception as e:
    print("Error: ", e.with_traceback())

while True:
    continue


# DEFINITIONS FROM WEBSITE, MAY BE CHANGED PER DRAWBACK
# 'piece': 'A piece is ANY chess piece, including pawns.',
# 'adjacent': 'A square is adjacent to another square if they are adjacent diagonally OR orthogonally.',
# 'distance': 'Distance is calculated by adding the horizontal and vertical distances ("Manhattan distance"); for example, the distance a knight moves is 3, and pieces move farther diagonally than orthogonally.',
# 'value': 'Piece value is calculated using 1-3-3-5-9: pawns are 1, bishops and knights are 3, rooks are 5, and queens are 9. Kings have infinite value.',
# 'rim': 'The rim is any square on the first rank, the last rank, the A-file, or the H-file.',
# 'lose': 'Drawbacks that make you lose are only checked at the start of your turn.'
