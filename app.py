from flask import Flask, request, jsonify, render_template
import hashlib
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

def generate_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_document():
    content = request.form.get("content", "")
    if not content:
        return jsonify({"error": "Missing 'content'"}), 400

    doc_hash = generate_hash(content)
    blockchain.add_block(doc_hash)
    return jsonify({
        "message": "Document notarized",
        "document_hash": doc_hash,
        "block_index": len(blockchain.chain) - 1
    })

@app.route("/verify", methods=["POST"])
def verify_document():
    content = request.form.get("content", "")
    if not content:
        return jsonify({"error": "Missing 'content'"}), 400

    doc_hash = generate_hash(content)
    is_verified, index = blockchain.verify_document(doc_hash)
    if is_verified:
        return jsonify({"verified": True, "block_index": index})
    else:
        return jsonify({"verified": False, "message": "Document not found"})

if __name__ == "__main__":
    app.run(debug=True)
