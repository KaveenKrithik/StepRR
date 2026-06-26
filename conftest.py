import sys
import os

# Add booking_service directory to sys.path
booking_service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "booking_service"))
sys.path.insert(0, booking_service_dir)
sys.path.insert(0, os.path.dirname(__file__))