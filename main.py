from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy

app = Flask(__name__)
cors = CORS(app)


@app.route('/Siter', methods=['POST'])
def main():
    data = request.json
    print(data)
    text = data['selectedText']
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    highlighted_text = ""
    prev_end = 0
    for ent in doc.ents:
        start = ent.start_char
        end = ent.end_char
        highlighted_text += text[prev_end:start]
        highlighted_text += f'<span class="{ent.label_}">{text[start:end]}</span>'
        prev_end = end
    highlighted_text += text[prev_end:]
    print(highlighted_text)

    return jsonify({'highlightedText': highlighted_text})

if __name__ == '__main__':
    app.run(debug=True)
