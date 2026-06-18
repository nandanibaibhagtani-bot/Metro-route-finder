import random
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend compatibility

# Localized Pakistan Metro Station Info
STATIONS = [
    {"id": "KHI-01", "name": "Numaish", "city": "Karachi", "line": "Green Line"},
    {"id": "KHI-02", "name": "Saddar", "city": "Karachi", "line": "Green Line"},
    {"id": "KHI-03", "name": "Tower", "city": "Karachi", "line": "Green Line"},
    {"id": "KHI-04", "name": "Gulshan", "city": "Karachi", "line": "Green Line"},
    {"id": "LHR-01", "name": "Ali Town", "city": "Lahore", "line": "Orange Line"},
    {"id": "LHR-02", "name": "Thokar", "city": "Lahore", "line": "Orange Line"},
    {"id": "LHR-03", "name": "Kalma Chowk", "city": "Lahore", "line": "Orange Line"},
    {"id": "ISB-01", "name": "Faiz Ahmed Faiz", "city": "Islamabad", "line": "Blue Line"},
    {"id": "ISB-02", "name": "Pak Secretariat", "city": "Islamabad", "line": "Blue Line"},
]

@app.route("/api/predict/crowd", methods=["GET"])
def predict_crowd():
    """
    Simulates crowd percentage estimation for a given station and hour.
    Morning peak: 8:00 AM - 10:00 AM
    Evening peak: 5:00 PM - 7:00 PM
    """
    station_id = request.args.get("station", "KHI-02")
    try:
        hour = int(request.args.get("hour", 8))
    except ValueError:
        hour = 8

    # Core logic: Peak crowd hours
    if 8 <= hour <= 10 or 17 <= hour <= 19:
        base_crowd = random.randint(65, 88)
        confidence = round(random.uniform(0.85, 0.96), 2)
        recommendation = "Heavy volume detected. Consider traveling outside peak hours or arriving 10 minutes early."
    else:
        base_crowd = random.randint(20, 50)
        confidence = round(random.uniform(0.78, 0.90), 2)
        recommendation = "Low/Moderate volume. Optimal conditions for a comfortable trip."

    return jsonify({
        "stationId": station_id,
        "hour": hour,
        "crowdPercentage": base_crowd,
        "confidence": confidence,
        "recommendation": recommendation,
        "success": True
    })

@app.route("/api/predict/delay", methods=["GET"])
def predict_delay():
    """
    Predicts operational delays (in minutes) for different metro lines based on simulated telemetry.
    """
    line_name = request.args.get("line", "Orange Line").lower()
    
    # Simulate realistic delay scenarios
    if "orange" in line_name:
        delay = random.choice([0, 0, 0, 4, 6]) # 40% chance of small delay
        status = "Signal synchronization issues at Kalma Chowk" if delay > 0 else "Operating on time"
    elif "green" in line_name:
        delay = random.choice([0, 0, 0, 0, 2])
        status = "Minor boarding delay at Saddar" if delay > 0 else "Operating on time"
    else:
        delay = 0
        status = "Operating on time"

    return jsonify({
        "line": line_name.title(),
        "delayMinutes": delay,
        "status": status,
        "confidence": round(random.uniform(0.82, 0.98), 2),
        "success": True
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Fast NLP parser utilizing regular expressions to answer user transit queries locally.
    """
    data = request.json or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"reply": "I did not receive a message. How can I help you?", "success": False})

    # Regex matches
    route_match = re.search(r"(?:route|from|go)\s+([\w\s]+)\s+(?:to|towards)\s+([\w\s]+)", message)
    crowd_match = re.search(r"(?:crowd|busy|traffic|passenger)", message)
    delay_match = re.search(r"(?:delay|late|time|schedule|status)", message)
    fare_match = re.search(r"(?:fare|ticket|cost|price|pkr|money)", message)
    greet_match = re.search(r"(?:hi|hello|salam|helo|hey|howdy)", message)

    if route_match:
        origin = route_match.group(1).strip().title()
        destination = route_match.group(2).strip().title()
        duration = random.randint(8, 25)
        cost = random.choice([20, 30, 40, 55])
        
        reply = f"🚇 **Routing Engine**: Best path between **{origin}** and **{destination}** computed.\n" \
                f"• Expected duration: **{duration} minutes**\n" \
                f"• Estimated Fare: **PKR {cost}**\n" \
                f"• System status: **Green Line and Orange Line operating smoothly.**\n" \
                f"Enjoy your trip! Let me know if you need another route."
    elif crowd_match:
        reply = "📊 **Crowd Density Matrix**:\n" \
                "• Karachi Saddar Station — **73%** (Peak Congestion)\n" \
                "• Lahore GPO Station — **42%** (Moderate Commuters)\n" \
                "• Islamabad Secretariat — **28%** (Low Volume)\n\n" \
                "**AI Tip**: Travel between 11:00 AM and 4:00 PM to avoid commuter rushes."
    elif delay_match:
        reply = "⚠️ **Live Delay Forecast**:\n" \
                "• **Karachi Green Line**: On Time ✅\n" \
                "• **Lahore Orange Line**: 4 mins delay (Switch maintenance at GPO)\n" \
                "• **Islamabad Blue Line**: On Time ✅\n\n" \
                "All systems indicate normal operations elsewhere."
    elif fare_match:
        reply = "💰 **Fare System Guidelines**:\n" \
                "• Minimum fare: **PKR 15** (Twin Cities Metro)\n" \
                "• Green Line base fare: **PKR 20** (max PKR 75 for Surjani-Saddar)\n" \
                "• Orange Line flat rate: **PKR 40** (Ali Town to Dera Gujran)\n\n" \
                "Recharge your card via the Smart Card Dashboard to receive travel discounts!"
    elif greet_match:
        reply = "👋 **Salam!** Welcome to **GO METRO AI**.\n\n" \
                "I am your virtual assistant. Ask me to:\n" \
                "• \"Calculate route from Saddar to Gulshan\"\n" \
                "• \"Check crowd reports\"\n" \
                "• \"Show current system delay status\""
    else:
        reply = "I'm not sure I understood that request. I can help with **route planning**, **crowd forecasting**, **fares**, and **live system alerts**. Please try rephrasing."

    return jsonify({
        "reply": reply,
        "success": True
    })

if __name__ == "__main__":
    # Start python server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
