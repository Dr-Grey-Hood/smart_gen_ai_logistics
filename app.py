from flask import Flask, request, jsonify, render_template
from utils.router import choose_model
from models import data_storage as ds
from models.blockchain import blockchain, Block
import time
import csv
import os

app = Flask(__name__)

# === Initialize M4 Brain Storage ===
DB_PATH = "ai_brain_data.db"
ds.init_db(DB_PATH)

# === Load Orders CSV for Verification ===
ORDERS_FILE = "orders.csv"

def verify_order(tracking_id, mobile_number):
    """Check if tracking_id and mobile_number exist in the CSV."""
    if not os.path.exists(ORDERS_FILE):
        return False
    with open(ORDERS_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["tracking_id"] == tracking_id and row["mobile_number"] == mobile_number:
                return True
    return False


# === ROUTES ===

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    return jsonify({
        "status": "Smart Gen AI Logistics Server Active",
        "message": "Welcome to the AI + Blockchain Logistics API"
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Step-by-step:
    1. Verify order from CSV.
    2. Predict using AI.
    3. Save in SQLite.
    4. Add blockchain transaction + mine.
    """
    data = request.get_json() or {}
    tracking_id = data.get("tracking_id")
    mobile_number = data.get("mobile_number")

    if not tracking_id or not mobile_number:
        return jsonify({"error": "tracking_id and mobile_number are required"}), 400

    # Verify order
    if not verify_order(tracking_id, mobile_number):
        return jsonify({"error": "Invalid tracking ID or mobile number"}), 400

    print(f"[Frontend] Verified Tracking: {tracking_id}, Mobile: {mobile_number}")

    # === Step 2: AI Prediction ===
    user_input = f"Predict logistics status for tracking ID {tracking_id} and mobile {mobile_number}"
    ai_response = choose_model(user_input)

    # === Step 3: Store in SQLite ===
    features = {
        "word_count": len(user_input.split()),
        "is_question": int(user_input.strip().endswith("?"))
    }
    record_id = ds.insert_record(
        input_text=user_input,
        prediction=ai_response,
        features=features,
        confidence=None,
        meta={"source": "AI+Blockchain"}
    )

    # === Step 4: Blockchain Transaction ===
    tx_data = {
        "type": "prediction",
        "record_id": record_id,
        "tracking_id": tracking_id,
        "mobile_number": mobile_number,
        "prediction": ai_response,
        "timestamp": time.time()
    }

    blockchain.new_transaction(tx_data)

    # Mine new block
    last_block = blockchain.last_block()
    new_block = Block(
        index=last_block.index + 1,
        timestamp=time.time(),
        transactions=blockchain.get_pending_transactions(),
        previous_hash=blockchain.hash_block(last_block),
        nonce=0
    )
    nonce, block_hash = blockchain.proof_of_work(new_block)
    mined_block = blockchain.add_block(nonce, previous_hash=blockchain.hash_block(last_block))

    # === Step 5: Return Full Response ===
    return jsonify({
        "message": "Prediction recorded and added to blockchain",
        "tracking_id": tracking_id,
        "mobile_number": mobile_number,
        "prediction": ai_response,
        "record_id": record_id,
        "block_info": mined_block.to_dict(),
        "block_hash": block_hash
    })


# === Feedback Route ===
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json() or {}
    record_id = data.get("record_id")
    actual = data.get("actual")

    if not record_id or actual is None:
        return jsonify({"error": "record_id and actual are required"}), 400

    ds.update_record_actual(record_id, actual, mark_processed=True)
    return jsonify({"ok": True, "message": "Feedback recorded successfully."})


# === Export Route ===
@app.route('/export', methods=['GET'])
def export_data():
    output_path = "training_data.csv"
    ds.export_to_csv(output_path, include_unprocessed_only=False)
    return jsonify({"message": f"Data exported to {output_path}"})


# === Blockchain Explorer Routes ===
@app.route('/blockchain/chain', methods=['GET'])
def get_chain():
    return jsonify({"length": len(blockchain.chain), "chain": blockchain.get_chain()})


@app.route('/blockchain/validate', methods=['GET'])
def validate_chain():
    ok = blockchain.is_valid_chain()
    return jsonify({"valid": ok})


# === Run Server ===
if __name__ == "__main__":
    print("🚀 Smart Gen AI Logistics (AI + Blockchain) server running...")
    app.run(debug=True)
