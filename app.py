from flask import Flask, request, jsonify
from find_category_of_product import process_image
from get_global_rating_of_product import get_global_rating

app = Flask(__name__)

# find similar

@app.route('/process-image', methods=['POST'])
def process_image_route():
    """
    Endpoint to process an image and return the detected category.
    """
    app.logger.info('POST request received at /process-image')
    if 'image' not in request.files:
        app.logger.error('No image provided in the request.')
        return jsonify({'categories': []}), 200

    file = request.files['image']

    try:
        app.logger.info('Image processing started.')
        best_category_ids, best_category, results = process_image(file)

        if not best_category:
            app.logger.info('No matching category found.')
            return jsonify({'categories': [], 'yolo_output': str(results)}), 200

        app.logger.info(f'Best category detected: {best_category}')
        return jsonify({'categories': [best_category_ids], 'yolo_output': str(results)})

    except ValueError as e:
        app.logger.error(f'Image processing error: {e}')
        return jsonify({'categories': []}), 200

    except Exception as e:
        app.logger.error(f'Error during YOLOv8 inference: {e}')
        return jsonify({'categories': []}), 200


# global rating
@app.route('/get_global_rating', methods=['POST'])
def get_global_rating_endpoint():
    """Ürün adını alır ve tüm sitedlerin değerlendirme bilgilerini döndürür."""
    try:
        app.logger.info('POST request received at /get_global_rating')
        data = request.get_json()
        app.logger.info(f'Received data: {data}')

        product_name = data.get('product_name')

        if not product_name:
            app.logger.error('Product name is missing in the request.')
            return jsonify({"error": "Product name is required"}), 400

        # get_global_rating_of_product.py'deki fonksiyonu çağır
        rating_info = get_global_rating(product_name)
        app.logger.info(f'Returned rating info: {rating_info}')
        return jsonify(rating_info), 200
    except Exception as e:
        app.logger.error(f'Error: {str(e)}')
        return jsonify({"error": str(e)}), 500


# port ayarlama
if __name__ == '__main__':
    app.run(debug=True, port=5000)
