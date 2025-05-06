import os
import re
import logging
import mimetypes
import traceback
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import bcrypt
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Configure logging with DEBUG level for detailed output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enable CORS for all origins
CORS(app)

# Load environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://kvejotrlwtxkzhgxtwre.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2ZWpvdHJsd3R4a3poZ3h0d3JlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxMDg3MDAsImV4cCI6MjA2MTY4NDcwMH0.LakaN0T-7EFF5bt6uD_mgn1es4Nu-l3TnY6HsnXI8vk')

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.debug("Supabase client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}\n{traceback.format_exc()}")
    raise

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    logger.debug(f"Hashing password for input length: {len(password)}")
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password: bytes, provided_password: str) -> bool:
    """Verify a password against its hash."""
    logger.debug(f"Checking password for provided input length: {len(provided_password)}")
    try:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
    except Exception as e:
        logger.error(f"Password check failed: {str(e)}\n{traceback.format_exc()}")
        return False

def validate_email(email: str) -> bool:
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    result = bool(re.match(email_regex, email))
    logger.debug(f"Email validation for '{email}': {'Valid' if result else 'Invalid'}")
    return result

def validate_username(username: str) -> bool:
    """Validate username (alphanumeric, 3-20 characters)."""
    result = bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))
    logger.debug(f"Username validation for '{username}': {'Valid' if result else 'Invalid'}")
    return result

def validate_password(password: str) -> bool:
    """Validate password (at least 8 characters, includes number and letter)."""
    result = len(password) >= 8 and bool(re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password))
    logger.debug(f"Password validation for input length {len(password)}: {'Valid' if result else 'Invalid'}")
    return result

# Custom 404 error handler
@app.errorhandler(NotFound)
def handle_not_found(error):
    error_msg = f"Endpoint not found: {request.method} {request.path}"
    logger.error(f"{error_msg}\nRequest headers: {dict(request.headers)}\n{traceback.format_exc()}")
    return jsonify({'error': error_msg}), 404

@app.route('/create_user', methods=['POST'])
def create_user():
    """Create a new user in Supabase."""
    logger.debug(f"Received request to /create_user: {request.headers.get('Content-Type')}")
    try:
        data = request.get_json()
        if not data:
            error_msg = 'Invalid JSON payload'
            logger.error(f"create_user failed: {error_msg}\nRequest data: {request.data}")
            return jsonify({'error': error_msg}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        logger.debug(f"create_user: username={username}, email={email}, password_length={len(password) if password else 0}")

        # Input validation
        if not username or not email or not password:
            error_msg = 'Missing username, email, or password'
            logger.error(f"create_user failed: {error_msg}\nRequest data: {data}")
            return jsonify({'error': error_msg}), 400
        if not validate_username(username):
            error_msg = 'Invalid username: must be 3-20 alphanumeric characters'
            logger.error(f"create_user failed: {error_msg}\nUsername: {username}")
            return jsonify({'error': error_msg}), 400
        if not validate_email(email):
            error_msg = 'Invalid email format'
            logger.error(f"create_user failed: {error_msg}\nEmail: {email}")
            return jsonify({'error': error_msg}), 400
        if not validate_password(password):
            error_msg = 'Invalid password: must be at least 8 characters with letters and numbers'
            logger.error(f"create_user failed: {error_msg}\nPassword length: {len(password)}")
            return jsonify({'error': error_msg}), 400

        # Check if username or email already exists
        existing_user = supabase.table('users').select('username, email').or_(f'username.eq.{username},email.eq.{email}').execute()
        logger.debug(f"Checked for existing user: {len(existing_user.data)} found")
        if existing_user.data:
            if any(user['username'] == username for user in existing_user.data):
                error_msg = 'Username already exists'
                logger.error(f"create_user failed: {error_msg}\nUsername: {username}")
                return jsonify({'error': error_msg}), 409
            if any(user['email'] == email for user in existing_user.data):
                error_msg = 'Email already exists'
                logger.error(f"create_user failed: {error_msg}\nEmail: {email}")
                return jsonify({'error': error_msg}), 409

        # Hash password and prepare user data
        password_hash = hash_password(password)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash.decode('utf-8')
        }
        logger.debug(f"Inserting user data: username={username}, email={email}")

        response = supabase.table('users').insert(user_data).execute()

        if response.data:
            logger.info(f"User created: {username}")
            return jsonify({'message': 'User created successfully'}), 201
        else:
            error_msg = f'Failed to create user: {response.error}' if hasattr(response, 'error') else 'Failed to create user'
            logger.error(f"create_user failed: {error_msg}\nResponse: {response}")
            return jsonify({'error': error_msg}), 500

    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        logger.error(f"create_user failed: {error_msg}\nRequest data: {data}\n{traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500

@app.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    """Authenticate a user with username and password."""
    logger.debug(f"Received request to /authenticate_user: {request.headers.get('Content-Type')}")
    try:
        data = request.get_json()
        if not data:
            error_msg = 'Invalid JSON payload'
            logger.error(f"authenticate_user failed: {error_msg}\nRequest data: {request.data}")
            return jsonify({'error': error_msg}), 400

        username = data.get('username')
        password = data.get('password')
        logger.debug(f"authenticate_user: username={username}, password_length={len(password) if password else 0}")

        if not username or not password:
            error_msg = 'Missing username or password'
            logger.error(f"authenticate_user failed: {error_msg}\nRequest data: {data}")
            return jsonify({'error': error_msg}), 400

        response = supabase.table('users').select('id, username, password_hash').eq('username', username).execute()
        logger.debug(f"User query result: {len(response.data)} users found")

        if response.data and len(response.data) > 0:
            user = response.data[0]
            stored_password = user['password_hash'].encode('utf-8')
            if check_password(stored_password, password):
                logger.info(f"User authenticated: {username}")
                return jsonify({
                    'message': 'Authentication successful',
                    'user_id': str(user['id']),
                    'username': user['username']
                }), 200
            else:
                error_msg = 'Invalid password'
                logger.warning(f"authenticate_user failed: {error_msg} for user: {username}")
                return jsonify({'error': error_msg}), 401
        else:
            error_msg = 'User not found'
            logger.warning(f"authenticate_user failed: {error_msg} for username: {username}")
            return jsonify({'error': error_msg}), 404

    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        logger.error(f"authenticate_user failed: {error_msg}\nRequest data: {data}\n{traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500

@app.route('/add_product', methods=['POST'])
def add_product():
    """Add a new product to Supabase with image stored in Storage."""
    try:
        # Get form data
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        rating = request.form.get('rating')

        # Validate inputs
        if not all([name, price, category, rating]):
            return jsonify({'error': 'Missing required fields'}), 400
        try:
            price = float(price)
            rating = float(rating)
        except ValueError:
            return jsonify({'error': 'Price and rating must be numbers'}), 400

        # Get image
        if 'image' not in request.files:
            return jsonify({'error': 'No image file'}), 400
        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        # Secure filename
        filename = secure_filename(image.filename)
        if not filename:
            return jsonify({'error': 'Invalid image filename'}), 400

        # Read image data
        image_data = image.read()
        logger.info(f"Image: {filename}, size: {len(image_data)} bytes")

        # Guess content type (default to image/jpeg)
        content_type = image.content_type or 'image/jpeg'
        if not content_type.startswith('image/'):
            return jsonify({'error': 'File is not an image'}), 400

        # Insert product data without image first to get ID
        product_data = {
            'name': name,
            'price': price,
            'category': category,
            'rating': rating
        }
        logger.info(f"Inserting product: {name}, price={price}, category={category}, rating={rating}")
        response = supabase.table('products').insert(product_data).execute()

        if not response.data:
            error_msg = f'Failed to create product: {response.error}' if hasattr(response, 'error') else 'Failed to create product'
            logger.error(f"add_product failed: {error_msg}\nResponse: {response}")
            return jsonify({'error': error_msg}), 500

        product_id = response.data[0]['id']

        # Upload image to Supabase Storage
        bucket_name = 'product-images'
        image_path = f"product_{product_id}_{filename}"
        logger.debug(f"Uploading image to bucket '{bucket_name}' with path '{image_path}'")
        try:
            upload_response = supabase.storage.from_(bucket_name).upload(
                path=image_path,
                file=image_data,
                file_options={'content-type': content_type}
            )
            logger.info(f"Image uploaded to {image_path}")
        except Exception as e:
            # Rollback product insertion if image upload fails
            supabase.table('products').delete().eq('id', product_id).execute()
            error_msg = f"Failed to upload image: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({'error': error_msg}), 500

        # Update product with image path
        update_response = supabase.table('products').update({'image_path': image_path}).eq('id', product_id).execute()
        if not update_response.data:
            # Rollback image upload and product insertion
            supabase.storage.from_(bucket_name).remove([image_path])
            supabase.table('products').delete().eq('id', product_id).execute()
            error_msg = f'Failed to update product with image path: {response.error}' if hasattr(response, 'error') else 'Failed to update product'
            logger.error(f"add_product failed: {error_msg}\nResponse: {update_response}")
            return jsonify({'error': error_msg}), 500

        logger.info(f"Product added: {name}, ID: {product_id}, Image: {image_path}")
        return jsonify({'message': 'Product added', 'product_id': product_id}), 201

    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        logger.error(f"add_product failed: {error_msg}\n{traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500

@app.route('/fetch_products', methods=['GET'])
def fetch_products():
    """Fetch all products from the Supabase database with image URLs."""
    logger.debug(f"Received request to /fetch_products")
    try:
        response = supabase.table('products').select('*').execute()

        if response.data:
            products = response.data
            logger.debug(f"Fetched {len(products)} products from database")
            bucket_name = 'product-images'
            for product in products:
                if product.get('image_path'):
                    try:
                        # Generate public URL for the image
                        image_url = supabase.storage.from_(bucket_name).get_public_url(product['image_path'])
                        product['image_url'] = image_url
                        logger.debug(f"Generated image URL for product ID {product.get('id')}: {image_url}")
                    except Exception as e:
                        logger.warning(f"Failed to generate image URL for product ID {product.get('id')}: {str(e)}")
                        product['image_url'] = 'https://via.placeholder.com/200'  # Fallback
                    del product['image_path']
                else:
                    product['image_url'] = 'https://via.placeholder.com/200'  # Fallback
                    logger.debug(f"No image path for product ID {product.get('id')}")
            logger.info(f"Fetched {len(products)} products")
            return jsonify(products), 200
        else:
            error_msg = f'Failed to fetch products: {response.error}' if hasattr(response, 'error') else 'Failed to fetch products'
            logger.error(f"fetch_products failed: {error_msg}\nResponse: {response}")
            return jsonify({'error': error_msg}), 500

    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        logger.error(f"fetch_products failed: {error_msg}\n{traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)