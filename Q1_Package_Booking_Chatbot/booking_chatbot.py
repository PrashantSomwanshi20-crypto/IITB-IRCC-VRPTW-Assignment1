import google.generativeai as genai
import json
import random

# 1. API Key Setup - Yahan apni Gemini API Key daalein
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

# 2. Define Tools
def get_vehicle_options(weight: float, length: float, width: float, height: float) -> str:
    """Get a list of available vehicles based on package weight (kg) and dimensions (cm)."""
    print("\n[System API Call -> get_vehicle_options]")
    if weight < 10 and length <= 50 and width <= 50 and height <= 50:
        return json.dumps([{"vehicle": "Bike", "capacity_kg": 15}, {"vehicle": "Small Van", "capacity_kg": 50}])
    else:
        return json.dumps([{"vehicle": "Large Truck", "capacity_kg": 500}])

def check_package_compatibility(vehicle: str, weight: float, length: float, width: float, height: float) -> str:
    """Check if the selected vehicle can carry the package based on weight and dimensions."""
    print("\n[System API Call -> check_package_compatibility]")
    if vehicle == "Bike" and (length > 50 or width > 50 or height > 50 or weight > 15):
        return json.dumps({"compatible": False, "reason": "Dimensions or weight too large for a Bike."})
    return json.dumps({"compatible": True, "reason": "Fits perfectly."})

def save_booking(destination: str, vehicle: str, weight: float, length: float, width: float, height: float) -> str:
    """Save the final booking ONLY after the user confirms everything."""
    print("\n[System API Call -> save_booking]")
    booking_id = f"BKG{random.randint(1000,9999)}"
    return json.dumps({"status": "Success", "booking_id": booking_id, "destination": destination, "vehicle": vehicle})

# 3. System Prompt
system_instruction = """
You are a highly efficient Package Booking Assistant. 
Your goal is to book a package delivery strictly following these steps:
1. Greet the user and ask for package details: Dimensions (Length, Width, Height in cm), Weight (in kg), and Destination.
2. If ANY information is missing, politely ask the user to provide it. Do NOT make assumptions.
3. Once ALL details are collected, call 'get_vehicle_options'. Present the options and ask them to choose.
4. After they choose, call 'check_package_compatibility'. 
5. If compatible, summarize details and EXPLICITLY ask for confirmation to book (e.g., "Type Yes to confirm").
6. ONLY after the user confirms, call 'save_booking'.
"""

# 4. Initialize Model with Tools
model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    tools=[get_vehicle_options, check_package_compatibility, save_booking],
    system_instruction=system_instruction
)

# 5. Start Chat
chat = model.start_chat(enable_automatic_function_calling=True)

print("🤖 Chatbot is ready! (Type 'exit' to stop)\n")

# 6. Main Chat Loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
        
    try:
        response = chat.send_message(user_input)
        print(f"Bot: {response.text}\n")
    except Exception as e:
        print(f"Error: {e}\n")