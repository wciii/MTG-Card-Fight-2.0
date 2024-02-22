from flask import Flask, request, render_template, url_for
import requests

app = Flask(__name__)

# Function to get card details
def get_card_details(card_name):
    card_name = card_name.replace(' ', '+')
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        card_data = response.json()

        image_url = card_data.get("image_uris", {}).get("normal") or card_data.get("image_uris", {}).get("large")

        return {
            "name": card_data.get("name"),
            "power": card_data.get("power"),
            "toughness": card_data.get("toughness"),
            "image_url": image_url
        }
    except requests.RequestException as e:
        print(f"Error fetching card data: {e}")
        return None

# Function to simulate the fight
def simulate_fight(card1, card2):
    creature1 = get_card_details(card1)
    creature2 = get_card_details(card2)

    if creature1 and creature2:
        try:
            creature1_power = int(creature1["power"])
            creature2_power = int(creature2["power"])
            creature1_toughness = int(creature1["toughness"])
            creature2_toughness = int(creature2["toughness"])

            fight_result = f"{creature1['name']} deals {creature1_power} damage to {creature2['name']}. "
            fight_result += f"{creature2['name']} deals {creature2_power} damage to {creature1['name']}. "

            creature1_toughness -= creature2_power
            creature2_toughness -= creature1_power

            creature1_status = "dead" if creature1_toughness <= 0 else "alive"
            creature2_status = "dead" if creature2_toughness <= 0 else "alive"

            if creature1_toughness <= 0:
                fight_result += f"{creature1['name']} is dead. "
            else:
                fight_result += f"{creature1['name']} has {creature1_toughness} toughness remaining. "

            if creature2_toughness <= 0:
                fight_result += f"{creature2['name']} is dead. "
            else:
                fight_result += f"{creature2['name']} has {creature2_toughness} toughness remaining. "

            return {
                "result": fight_result,
                "creature1_image_url": creature1.get("image_url"),
                "creature2_image_url": creature2.get("image_url"),
                "creature1_status": creature1_status,
                "creature2_status": creature2_status
            }
        except ValueError:
            return {"result": "Invalid power or toughness for one of the creatures."}
    else:
        return {"result": "Could not fetch details for one or both creatures."}

# Home page route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Fight result route
@app.route('/fight', methods=['POST'])
def fight():
    card1 = request.form.get('card1')
    card2 = request.form.get('card2')
    fight_details = simulate_fight(card1, card2)
    return render_template('result.html', **fight_details)

if __name__ == '__main__':
    app.run(debug=True)