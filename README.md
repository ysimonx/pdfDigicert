# PDF DigiCert Timestamper

A professional Python tool for applying RFC 3161 compliant timestamps to PDF documents using the DigiCert Timestamp Authority (TSA).

## Overview

This tool allows you to add cryptographic timestamps to PDF files, providing verifiable proof of a document's existence at a specific point in time. The timestamps are applied using the industry-standard RFC 3161 protocol and DigiCert's trusted timestamp service.

## Features

- **RFC 3161 Compliant**: Uses the standard Time-Stamp Protocol
- **DigiCert Integration**: Leverages DigiCert's reliable public TSA service
- **Incremental Updates**: Preserves original PDF structure using incremental writing
- **Professional Error Handling**: Comprehensive exception handling and logging
- **Type Hints**: Full type annotation support for better IDE integration
- **Easy to Use**: Simple API and command-line interface

## Requirements

- Python 3.7+
- pyHanko library

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd pdfDigicert
```

2. Install dependencies:
```bash
pip install pyhanko
```

Or using a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pyhanko
```

## Usage

### Basic Usage

1. Place your PDF file in the project directory and name it `document_a_horodater.pdf`

2. Run the script:
```bash
python test.py
```

3. The timestamped PDF will be saved as `document_horodate.pdf`

### Programmatic Usage

You can also use the `PDFTimestamper` class in your own code:

```python
from pathlib import Path
from test import PDFTimestamper

# Initialize the timestamper
timestamper = PDFTimestamper()

# Timestamp a file
timestamper.timestamp_file(
    input_path=Path('input.pdf'),
    output_path=Path('output.pdf'),
    hash_algorithm='sha256'
)
```

### Using a Custom TSA

If you want to use a different timestamp authority:

```python
timestamper = PDFTimestamper(tsa_url='http://your-tsa-server.com')
```

## Configuration

You can modify the following constants in `test.py`:

- `DEFAULT_TSA_URL`: The URL of the timestamp authority (default: DigiCert)
- `DEFAULT_HASH_ALGORITHM`: Hash algorithm for timestamping (default: sha256)

To change the input/output file paths, modify the `main()` function:

```python
def main():
    input_file = Path('your_input.pdf')
    output_file = Path('your_output.pdf')
    # ...
```

## How It Works

1. **Initialization**: The tool creates an HTTP connection to the DigiCert TSA
2. **Reading**: The input PDF is opened using incremental writing mode
3. **Timestamping**: A timestamp request is sent to DigiCert with a hash of the document
4. **Embedding**: The timestamp token is embedded into the PDF as an invisible signature field
5. **Saving**: The modified PDF is saved with the timestamp embedded

The timestamp includes:
- Exact date and time from DigiCert's trusted time source
- Cryptographic hash of the document
- DigiCert's digital signature
- Certificate chain for verification

## Error Handling

The tool provides clear error messages for common issues:

- **File not found**: If the input PDF doesn't exist
- **Invalid file**: If the input file is not a PDF
- **Network errors**: If the TSA is unreachable
- **Timestamping failures**: If the timestamp cannot be applied

All errors are logged with timestamps and severity levels.

## Logging

The script uses Python's built-in logging module. Logs include:

- Initialization messages
- Processing status
- Success/failure notifications
- Detailed error information

Log level can be adjusted in the code:

```python
logging.basicConfig(level=logging.DEBUG)  # For verbose output
```

## Verification

To verify that a PDF has been properly timestamped, you can:

1. Open the PDF in Adobe Acrobat Reader
2. Go to "Signature Panel" (View > Tools > Certificates)
3. Check the timestamp details including:
   - Timestamp date and time
   - TSA information (DigiCert)
   - Hash algorithm used
   - Certificate chain validity

## Security Notes

- **Trusted TSA**: This tool uses DigiCert's public TSA, a trusted certificate authority
- **No Private Keys**: Timestamping does not require private keys or certificates
- **Integrity**: The timestamp proves document integrity at a specific time
- **Non-repudiation**: Timestamps cannot be backdated or modified

## Limitations

- Requires internet connection to reach the DigiCert TSA
- The free DigiCert TSA may have rate limits
- Timestamps add a small amount of data to the PDF file

## Troubleshooting

### "Connection refused" or "TSA unreachable"
- Check your internet connection
- Verify firewall settings allow HTTP connections
- The DigiCert TSA may be temporarily unavailable

### "Invalid PDF"
- Ensure the input file is a valid PDF
- Check that the file is not corrupted
- Try opening the file in a PDF reader first

### "Permission denied"
- Check file permissions on input/output directories
- Ensure the input file is not open in another program

## License

MIT License - feel free to use and modify as needed.

## Credits

Built with:
- [pyHanko](https://github.com/MatthiasValvekens/pyHanko) - PDF signing and timestamping library
- [DigiCert](https://www.digicert.com/) - Trusted timestamp authority

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Support

For issues related to:
- **This tool**: Open an issue in this repository
- **pyHanko library**: Visit the [pyHanko GitHub](https://github.com/MatthiasValvekens/pyHanko)
- **DigiCert TSA**: Contact [DigiCert support](https://www.digicert.com/support/)

## References

- [RFC 3161 - Time-Stamp Protocol](https://www.rfc-editor.org/rfc/rfc3161)
- [DigiCert TSA Information](https://www.digicert.com/kb/util/utility-test-ssl-connection-to-timestamp-server.htm)
- [PDF Signatures and Timestamps](https://www.adobe.com/devnet-docs/acrobatetk/tools/DigSig/Acrobat_DigSig_Security.pdf)
