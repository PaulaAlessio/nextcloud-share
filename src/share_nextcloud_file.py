import subprocess
import requests
import argparse
from requests.auth import HTTPBasicAuth


def get_credentials(service_name, enc_credentials_file):
  # Use openssl to decrypt the credentials file
  result = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-d", "-pbkdf2", "-in", enc_credentials_file],
    stdout=subprocess.PIPE,
    text=True  # Ensure the result is handled as text
  )

  # Decrypted content
  decrypted_content = result.stdout.strip()

  # Parse the decrypted content and find the entry for the given service
  for line in decrypted_content.splitlines():
    service, username, password = line.split(':')
    if service == service_name:
      return username, password

  # If the service is not found, return None
  return None, None


class NextcloudClient:
  def __init__(self, username, password, base_url):
    """Initialize with credentials and base URL."""
    self.username = username
    self.password = password
    self.base_url = base_url
    self.auth = HTTPBasicAuth(username, password)

  def share_file(self, path, share_type=3, permissions=1):
    """
        Share a file and return the response. By default, shareType=3 (public link),
        and permissions=1 (read-only).
        """
    url = f"{self.base_url}/ocs/v2.php/apps/files_sharing/api/v1/shares"
    headers = {"OCS-APIRequest": "true"}
    data = {
      "path": path,
      "shareType": share_type,
      "permissions": permissions
    }
    response = requests.post(url, headers=headers, data=data, auth=self.auth)

    if response.status_code == 200:
      return response.text  # You can modify to parse the XML/JSON
    else:
      print(response.text)
      raise Exception(f"Failed to share file. Status code: {response.status_code}")

  @staticmethod
  def get_share_url(share_response):
    """
        Extract the share URL from the response. Assumes XML parsing.
        """
    import xml.etree.ElementTree as ET

    # Parse the XML response
    root = ET.fromstring(share_response)
    # Find the URL tag
    url_element = root.find(".//url")
    if url_element is not None:
      return url_element.text
    else:
      raise Exception("Share URL not found in response")


def parse_args():
  # Create an ArgumentParser object with a  help message
  parser = argparse.ArgumentParser(
    description="This program shares a file on Nextcloud using the Nextcloud API."
  )

  # Add the mandatory -p / --path argument with custom help text
  parser.add_argument(
    "-p", "--path",
    required=True,
    help="Path to the file in the Nextcloud structure that you want to make shareable"
  )

  # Add the mandatory -e --credentials-enctyoe with help text
  parser.add_argument(
    "-e", "--credentials-encfile",
    required=True,
    help="Path to the encripted file containing the credentials."
  )

  # Parse the arguments
  args = parser.parse_args()

  return args


def main():
  # Parse command line arguments
  args = parse_args()

  file_path = args.path
  print(f"The file path provided is: {file_path}")

  enc_credentials = args.credentials_encfile
  print(f"The path to the file that contains the encripted credentials: {enc_credentials}")

  # Initialize Nextcloud client with credentials and base URL
  service_name = "nextcloud"
  username, password = get_credentials(service_name, enc_credentials)

  if username and password:
    print(f"Credentials for {service_name} were correctly retrieved")
  else:
    print(f"Service {service_name} not found.")
  client = NextcloudClient(username, password, "https://cloud.educa.madrid.org")

  try:
    # Share the file
    response = client.share_file(file_path)
    print("File shared successfully!")

    # Extract and print the share URL
    share_url = client.get_share_url(response)
    print(f"Share URL: {share_url}")
  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  main()
