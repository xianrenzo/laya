from flask import Flask, render_template_string, request

app = Flask(__name__)

# Prices for all 35 curtains and blinds with serial numbers and categories (from your provided data)
prices = {
    'Sheer Canvass': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 424'},
    'Sheer Strips White': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 425'},
    'Sheer Summer Khaki': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 506'},
    'Sheer Summer Peanut': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 504'},
    'Sheer Summer Sand': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 503'},
    'Sheer Summer Seal': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 512'},
    'Sheer Tetris Champagne': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 412'},
    'Sheer Tetris Smoke': {'price': 139.65, 'category': 'Sheer', 'code': 'SR 414'},
    'Sheer Voile Snow': {'price': 126.35, 'category': 'Sheer', 'code': 'SR 402'},
    'Sheer Voile White': {'price': 126.35, 'category': 'Sheer', 'code': 'SR 401'},
    'Sheer Zebra': {'price': 126.35, 'category': 'Sheer', 'code': 'SR 428'},
    'Soft Blackout Aphrodite': {'price': 126.35, 'category': 'Soft Blackout', 'code': 'AP 100'},
    'Soft Blackout Athena': {'price': 126.35, 'category': 'Soft Blackout', 'code': 'AT 200'},
    'Total Blackout GOTHAM': {'price': 239.40, 'category': 'Total Blackout', 'code': 'GT 1500'},
    'Total Blackout HERA': {'price': 172.90, 'category': 'Total Blackout', 'code': 'HR 1700'},
    'Total Blackout PERSIA': {'price': 246.05, 'category': 'Total Blackout', 'code': 'PS 1900'},
    'Total Blackout RAFIA': {'price': 246.05, 'category': 'Total Blackout', 'code': 'RF 2000'},
    'Total Blackout VESPER': {'price': 172.90, 'category': 'Total Blackout', 'code': 'VP 1600'},
    'Blackout Combi Adeline Premium': {'price': 123.69, 'category': 'Blackout Combi', 'code': 'A200'},
    'Blackout Combi Hannover Premium': {'price': 115.71, 'category': 'Blackout Combi', 'code': 'H500'},
    'Blackout Combi Luxury Premium': {'price': 115.71, 'category': 'Blackout Combi', 'code': 'L500'},
    'Blackout Combi Majesty Premium': {'price': 115.71, 'category': 'Blackout Combi', 'code': 'M500'},
    'Blackout Combi Picasso Premium': {'price': 115.71, 'category': 'Blackout Combi', 'code': 'P800'},
    'Blackout Combi Prima-S Supreme': {'price': 130.34, 'category': 'Blackout Combi', 'code': 'P500'},
    'Blackout Combi Ultima Supreme': {'price': 130.34, 'category': 'Blackout Combi', 'code': 'U500'},
    'Wood Combi Amira': {'price': 113.05, 'category': 'Wood Combi', 'code': 'A700'},
    'Wood Combi Crescendo': {'price': 95.20, 'category': 'Wood Combi', 'code': 'C600'},
    'Wood Combi Duology': {'price': 93.10, 'category': 'Wood Combi', 'code': 'D500'},
    'Wood Combi Kingswood': {'price': 92.40, 'category': 'Wood Combi', 'code': 'K500'},
    'Wood Combi Losa Wood': {'price': 92.40, 'category': 'Wood Combi', 'code': 'W500'},
    'Wood Combi Mono': {'price': 99.75, 'category': 'Wood Combi', 'code': 'M300'},
    'Wood Combi Natural Basic': {'price': 86.80, 'category': 'Wood Combi', 'code': 'N500 / B500'},
    'Wood Combi Natural Linen': {'price': 86.80, 'category': 'Wood Combi', 'code': 'L700'},
    'Wood Combi Trilogy': {'price': 88.20, 'category': 'Wood Combi', 'code': 'T620'},
    'Wood Combi Wider': {'price': 102.41, 'category': 'Wood Combi', 'code': 'G400'},
    'Wood Combi Woodlook Eluxe': {'price': 86.80, 'category': 'Wood Combi', 'code': 'D200'},
    'Wood Combi Woodlook Prime': {'price': 86.80, 'category': 'Wood Combi', 'code': 'W300'},
}

# HTML Template for the web page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layà Curtains and Blinds</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
        .container { width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; background-color: #fff; }
        h1 { text-align: center; }
        label { font-size: 14px; }
        input, select, button { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .quote-summary { margin-top: 20px; padding: 15px; background-color: #e9f5e9; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Layà Curtains and Blinds</h1>
        <form method="POST">
            <label for="blind-type">Select Blind Type:</label>
            <select name="blind-type" required>
                {% for blind, details in prices.items() %}
                    <option value="{{ blind }}">{{ blind }} - {{ details['price'] }} PHP per Meter (Code: {{ details['code'] }})</option>
                {% endfor %}
            </select>
            
            <label for="square-feet">Enter Square Feet:</label>
            <input type="number" name="square-feet" required min="1">
            
            <label for="motorized">Motorized Curtains (1200 PHP per meter + 7000 PHP for remote):</label>
            <input type="checkbox" name="motorized" onchange="toggleMotorizedInput()">
            
            <label for="motorized-meters" id="motorized-meters-label" style="display:none;">Enter Meters for Motorized Curtains:</label>
            <input type="number" name="motorized-meters" id="motorized-meters" placeholder="Enter Meters for Motorized Curtains" style="display:none;">
            
            <button type="submit">Generate Quote</button>
        </form>

        {% if quote %}
        <div class="quote-summary">
            <h3>Quote Summary</h3>
            <p>Blind Type: {{ quote.blind_type }}</p>
            <p>Square Feet: {{ quote.square_feet }}</p>
            <p>Price per Meter: {{ quote.price_per_meter }} PHP</p>
            <p>Motorized Price: {{ quote.motorized_price }} PHP</p>
            <p>Customization Fee: 1500 PHP</p>
            <h3>Total Quote: {{ quote.total_price }} PHP</h3>
        </div>
        {% endif %}
    </div>

    <script>
        function toggleMotorizedInput() {
            const motorizedCheckbox = document.querySelector('input[name="motorized"]');
            const motorizedInput = document.getElementById('motorized-meters');
            const motorizedLabel = document.getElementById('motorized-meters-label');
            if (motorizedCheckbox.checked) {
                motorizedInput.style.display = 'block';
                motorizedLabel.style.display = 'block';
            } else {
                motorizedInput.style.display = 'none';
                motorizedLabel.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    quote = None
    motorized_price = 0
    motorized = False  # Initialize motorized variable to False by default
    if request.method == "POST":
        # Get form data
        blind_type = request.form.get("blind-type")
        square_feet = int(request.form.get("square-feet"))
        motorized = 'motorized' in request.form  # Set motorized if checkbox is selected
        motorized_meters = int(request.form.get("motorized-meters", 0)) if motorized else 0
        
        # Calculate the base price per meter
        price_per_meter = prices.get(blind_type, {'price': 0})['price']
        total_price = price_per_meter * square_feet

        # Add motorized curtains cost
        if motorized:
            motorized_price = 1200 * motorized_meters + 7000  # Motorized charge per meter + remote price
            total_price += motorized_price

        # Apply customization fee
        total_price += 1500

        # Prepare quote details
        quote = {
            'blind_type': blind_type,
            'square_feet': square_feet,
            'price_per_meter': price_per_meter,
            'motorized_price': motorized_price,
            'total_price': total_price
        }
    
    return render_template_string(html_template, prices=prices, quote=quote, motorized=motorized)

if __name__ == "__main__":
    app.run(debug=True)

