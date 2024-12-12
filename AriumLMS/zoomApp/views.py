import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from google.cloud import storage

# Load environment variables
load_dotenv()
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
GCP_CREDENTIALS = os.getenv("GCP_CREDENTIALS")

# Initialize GCP client
storage_client = storage.Client.from_service_account_json(GCP_CREDENTIALS)
bucket = storage_client.bucket(GCP_BUCKET_NAME)

def get_zoom_access_token():
    """Fetch OAuth access token for Zoom."""
    url = "https://zoom.us/oauth/token"
    params = {
        "grant_type": "account_credentials",
        "account_id": ZOOM_ACCOUNT_ID,
    }
    auth = (ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET)
    response = requests.post(url, params=params, auth=auth)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error fetching access token: {response.text}")
        return None

def upload_to_gcp(file_url, file_name):
    """Upload file to GCP bucket."""
    blob = bucket.blob(file_name)
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        blob.upload_from_file(response.raw, content_type="video/mp4")
        print(f"Uploaded {file_name} to GCP bucket.")
    else:
        print(f"Error downloading file: {response.text}")


# @csrf_exempt
# def zoom_webhook(request):
#     print(":::::::::::::zoom webhook in" , request.method)
#     """Handle Zoom webhooks and validation."""
#     if request.method == "GET" and "validationToken" in request.GET:
#         # Respond with the validationToken in plain text
#         validation_token = request.GET["validationToken"]
#         return JsonResponse({"message": validation_token}, safe=False)

#     if request.method == "POST":
#         try:
#             # Parse the incoming JSON data
#             data = json.loads(request.body.decode("utf-8"))
#             print(data)  # For debugging, you can remove this once it's working
            
#             # Handle the URL validation event (this is the first step Zoom performs)
#             if data.get("event") == "endpoint.url_validation":
#                 plain_token = data.get("payload", {}).get("plainToken")
#                 if plain_token:
#                     # Ensure the correct response format
#                     print("result::::",{"plainToken": plain_token})
#                     response = JsonResponse({"plainToken": plain_token})
#                     response['Content-Type'] = 'application/json'
#                     print(":::",response.get('plainToken'))
#                     return response


#                     # return JsonResponse({"plainToken": plain_token})
#                     # response['Content-Type'] = 'application/json'
#                 else:
#                     return JsonResponse({"error": "No plainToken found"}, status=400)

#             # Handle other events (like recording.completed)
#             if data.get("event") == "recording.completed":
#                 recording = data.get("payload", {}).get("object", {})
#                 meeting_name = recording.get("topic", "Untitled Meeting")
#                 # Loop through all recording files
#                 for file in recording.get("recording_files", []):
#                     if file.get("file_type") == "MP4":
#                         file_name = f"{meeting_name}_{file.get('id')}.mp4"
#                         # Call your upload function here
#                         upload_to_gcp(file.get("download_url"), file_name)

#             return JsonResponse({"message": "Webhook received successfully."})  
#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse({"error": "Invalid data"}, status=400)


#     return JsonResponse({"error": "Invalid method"}, status=400)



@csrf_exempt
def zoom_webhook(request):
    print(":::::::::::::zoom webhook in", request.method)
    """Handle Zoom webhooks and validation."""
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode("utf-8"))
            print(data)  # Debugging: Log the incoming data
            
            # Handle the URL validation event
            if data.get("event") == "endpoint.url_validation":
                plain_token = data.get("payload", {}).get("plainToken")
                if plain_token:
                    print("Returning plainToken:", plain_token)
                    
                    # Return the response in the expected format
                    response = JsonResponse({"plainToken": plain_token})
                    response["Content-Type"] = "application/json"
                    return response
                else:
                    return JsonResponse({"error": "plainToken not found"}, status=400)
            
            # Handle other events (e.g., recording.completed)
            if data.get("event") == "recording.completed":
                recording = data.get("payload", {}).get("object", {})
                meeting_name = recording.get("topic", "Untitled Meeting")
                
                # Process recording files
                for file in recording.get("recording_files", []):
                    if file.get("file_type") == "MP4":
                        file_name = f"{meeting_name}_{file.get('id')}.mp4"
                        # Call your upload function here
                        upload_to_gcp(file.get("download_url"), file_name)
            
            return JsonResponse({"message": "Webhook received successfully."})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=400)


