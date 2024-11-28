from flask import Flask, jsonify, abort
import json
import os
app = Flask(__name__)

def load_items():
    if not os.path.exists('./products/v1.json'):
        abort(500, description="Data file not found")
    
    with open('./products/v1.json', 'r') as file:
        items = json.load(file)  
  
    return items

def retrieve_item_by_id(item_id):
    items = load_items()  
    for item in items:
        if item['id'] == item_id:
            return item
    return None 

def retrieve_item_by_name(item_name):
    items = load_items()
    for item in items:
        if item['name'].lower() == item_name.lower():
            return item
    return None


def retrieve_items_by_category(category):
    items = load_items()
    filtered_items = [item for item in items if item['category'].lower() == category.lower()]
    return filtered_items


@app.route('/products/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = retrieve_item_by_id(item_id)
    if not item:
        abort(404, description="Item not found")
    return jsonify({'item': item})

@app.route('/products/name/<string:item_name>', methods=['GET'])
def get_item_by_name(item_name):
    item = retrieve_item_by_name(item_name)
    if not item:
        abort(404, description="Item not found")
    return jsonify({'item': item})

@app.route('/products/category/<string:category>', methods=['GET'])
def get_items_by_category(category):
    items = retrieve_items_by_category(category)
    if not items:
        abort(404, description="No items found in this category")
    return jsonify({'items': items})


@app.route('/')
def home():
    return "Product API"

if __name__ == '__main__':
    app.run(debug=True)