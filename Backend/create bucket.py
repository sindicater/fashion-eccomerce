import os
import logging
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://kvejotrlwtxkzhgxtwre.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2ZWpvdHJsd3R4a3poZ3h0d3JlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxMDg3MDAsImV4cCI6MjA2MTY4NDcwMH0.LakaN0T-7EFF5bt6uD_mgn1es4Nu-l3TnY6HsnXI8vk')

BUCKET_NAME = 'product-images'

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    raise

def create_bucket():
    """Create the product-images bucket in Supabase storage."""
    try:
        # Check if bucket already exists
        buckets = supabase.storage.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]
        if BUCKET_NAME in bucket_names:
            logger.info(f"Bucket '{BUCKET_NAME}' already exists.")
            return

        # Create bucket with public access
        response = supabase.storage.create_bucket(BUCKET_NAME, options={'public': True})
        if response.status_code == 200 or response.status_code == 201:
            logger.info(f"Successfully created bucket '{BUCKET_NAME}'.")
        else:
            logger.error(f"Failed to create bucket '{BUCKET_NAME}': {response.content}")
            raise Exception(f"Failed to create bucket: {response.content}")

    except Exception as e:
        logger.error(f"Error creating bucket '{BUCKET_NAME}': {str(e)}")
        if 'Unauthorized' in str(e) or 'Permission' in str(e):
            logger.error("The Supabase key lacks permission to create buckets. Use a service_role key.")
        raise

if __name__ == "__main__":
    create_bucket()