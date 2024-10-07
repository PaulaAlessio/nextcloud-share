# Nextcloud File Sharing Script

This Python script enables you to share a file in a Nextcloud instance via the Nextcloud API. The script makes use of encrypted credentials stored locally and performs the sharing operation, returning a shareable URL for the file.

## Features

- Use the Nextcloud API to share files via a public link.
- Credentials are securely stored in an encrypted file.
- The script returns the shareable URL after successfully sharing a file.

## Requirements

- Python 3.x
- Required Python libraries: `requests`

## Installation

### Unix-based Systems (Linux, macOS)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/nextcloud-file-share-script.git
   cd nextcloud-file-share-script
   ```

2. **Set up a virtual environment (recommended):**

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    ```

3. Install dependencies:

   ```bash
    pip install -r requirements.txt
   ```

4. Set up your encrypted credentials file:

   ```bash
    echo "nextcloud:your-username:your-password" > creds.txt
    openssl enc -aes-256-cbc -salt -pbkdf2 -in creds.txt -out creds.enc
    rm creds.txt  # Ensure you remove the plaintext credentials after encryption.
```

### Windows

1. **Clone the repository**: Open Command Prompt or PowerShell and run:

   ```bash
   git clone https://github.com/your-repo/nextcloud-file-share-script.git
   cd nextcloud-file-share-script
   ```

2. **Set up a virtual** environment (recommended):

   ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Set up your encrypted credentials file: Run the following in PowerShell:

   ```bash
   echo "nextcloud:your-username:your-password" > creds.txt
   openssl enc -aes-256-cbc -salt -pbkdf2 -in creds.txt -out creds.enc
   Remove-Item creds.txt  # Remove the plaintext credentials after encryption.
   ```
## Usage

### Command Line Arguments:
- `-p, --path` (Required): The path to the file you want to make shareable in your Nextcloud file structure.
- `-e, --credentials-encfile` (Required): Path to the encrypted file containing your credentials.
- `-h, --help`: Display help information.

### Example Usage:

To share a file and get a public URL:

```bash
python3 share_nextcloud_file.py -p "/path/to/file/in/nextcloud" -e "creds.enc"
```

This will output something like:

```bash
The file path provided is: /Documents/test.txt
The path to the file that contains the encrypted credentials: creds.enc
Credentials for nextcloud were correctly retrieved
File shared successfully!
Share URL: https://cloud.educa.madrid.org/s/EXAMPLE_URL
```

## Encrypting the Credentials File

You can store your Nextcloud credentials (`service-name:username:password`) 
in an encrypted file using openssl. Here's the command to create 
an encrypted file `creds.enc` from `creds.txt`:

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in creds.txt -out creds.enc
```

Make sure that `creds.txt` contains the following format:


```makefile
service-name:your-username:your-password
```

Once encrypted, you can remove creds.txt to keep your credentials secure.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

