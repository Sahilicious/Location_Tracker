import phonenumbers 
from phonenumbers import geocoder, carrier, NumberParseException
from timezonefinder import TimezoneFinder
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Step 1: Get phone number input
number = input("📞 Enter the phone number with country code (eg.+91): ")

try:
    phone_number = phonenumbers.parse(number)

    # Step 2: Basic info
    location = geocoder.description_for_number(phone_number, 'en')
    service_provider = carrier.name_for_number(phone_number, 'en')

    if not location:
        print("❌ Could not detect location from the number.")
    else:
        print(f"📍 Location: {location}")
    
    if not service_provider:
        print("❌ Could not detect carrier.")
    else:
        print(f"📡 SIM/Carrier: {service_provider}")

    # Step 3: Get coordinates
    try:
        time.sleep(1)  # avoid rate-limit
        geolocator = Nominatim(user_agent="BetterPhoneTracker/2.0")
        location_data = geolocator.geocode(f"{location}", timeout=8)

        if location_data:
            lat, lon = location_data.latitude, location_data.longitude
            print(f"🌍 Coordinates: {lat}, {lon}")

            # Step 4: Find timezone
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=lon, lat=lat)
            print(f"🕒 Timezone: {timezone if timezone else 'Unknown'}")

            # Step 5: Create map
            map = folium.Map(location=[lat, lon], zoom_start=8)
            folium.Marker(
                [lat, lon],
                popup=f"{location} ({service_provider})",
                tooltip="Click for more info",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map)

            map.save("phone_location.html")
            print("📁 Map saved as phone_location.html")

        else:
            print("❌ Could not get coordinates for the detected location.")

    except (GeocoderTimedOut, GeocoderServiceError) as geo_err:
        print("🚫 Geocoding error:", geo_err)

except NumberParseException:
    print("⚠ Invalid phone number format. Please include country code like +91xxxxxxxxxx.")
except Exception as e:
    print("🚫 Unexpected error:", e)
