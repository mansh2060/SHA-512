from flask import Flask, render_template, request
from final_hash_calculation import HashCalculation


app = Flask(__name__)

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    hash_result = None

    if request.method == "POST":
        text = request.form["text"]  # Get text input from user
        binary_encoded_list = list(''.join(format(ord(c), '08b') for c in text))  # Convert to binary

        # Run SHA-512 processing
        hash_calc = HashCalculation(text, binary_encoded_list)
        hash_result = hash_calc.hash_calulation()

        # Convert hash values to readable hex format
        hash_result = [h[2:].zfill(16) for h in hash_result]  # Remove '0x' prefix and pad

    return render_template("index.html", hash_result=hash_result)

if __name__ == "__main__":
    app.run(debug=True)
