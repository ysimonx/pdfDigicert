#!/usr/bin/env python3
"""
PDF Timestamping Tool using DigiCert TSA

This script applies RFC 3161 compliant timestamps to PDF documents using
the DigiCert timestamping service and the pyHanko library.

Author: Your Name
License: MIT
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, timestamps


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFTimestampError(Exception):
    """Custom exception for PDF timestamping errors."""
    pass


class PDFTimestamper:
    """Handles PDF timestamping operations using DigiCert TSA."""

    DEFAULT_TSA_URL = 'http://timestamp.digicert.com'
    DEFAULT_HASH_ALGORITHM = 'sha256'

    def __init__(self, tsa_url: Optional[str] = None):
        """
        Initialize the PDF timestamper.

        Args:
            tsa_url: URL of the RFC 3161 compliant timestamp authority.
                    Defaults to DigiCert's public TSA.
        """
        self.tsa_url = tsa_url or self.DEFAULT_TSA_URL
        logger.info(f"Initializing PDFTimestamper with TSA: {self.tsa_url}")

        try:
            self.timestamper = timestamps.HTTPTimeStamper(self.tsa_url)
            self.pdf_timestamper = signers.PdfTimeStamper(self.timestamper)
        except Exception as e:
            raise PDFTimestampError(f"Failed to initialize timestamper: {e}")

    def timestamp_file(
        self,
        input_path: Path,
        output_path: Path,
        hash_algorithm: str = DEFAULT_HASH_ALGORITHM
    ) -> None:
        """
        Apply a timestamp to a PDF file.

        Args:
            input_path: Path to the input PDF file.
            output_path: Path where the timestamped PDF will be saved.
            hash_algorithm: Hash algorithm to use (default: sha256).

        Raises:
            PDFTimestampError: If timestamping fails.
            FileNotFoundError: If input file doesn't exist.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if not input_path.suffix.lower() == '.pdf':
            raise PDFTimestampError(f"Input file must be a PDF: {input_path}")

        logger.info(f"Processing: {input_path}")
        logger.info(f"Output will be saved to: {output_path}")

        try:
            with open(input_path, 'rb') as inf:
                writer = IncrementalPdfFileWriter(inf)

                # Apply timestamp
                logger.info(f"Applying timestamp using {hash_algorithm} algorithm...")
                output_stream = self.pdf_timestamper.timestamp_pdf(
                    writer,
                    md_algorithm=hash_algorithm
                )

                # Save timestamped PDF
                with open(output_path, 'wb') as outf:
                    outf.write(output_stream.read())

            logger.info(f"Successfully timestamped PDF: {output_path}")

        except Exception as e:
            raise PDFTimestampError(f"Failed to timestamp PDF: {e}")


def main():
    """Main entry point for the script."""

    # Configuration
    input_file = Path('document_a_horodater.pdf')
    output_file = Path('document_horodate.pdf')

    try:
        # Initialize timestamper
        timestamper = PDFTimestamper()

        # Process the PDF
        timestamper.timestamp_file(input_file, output_file)

        print(f"\n✓ Document successfully timestamped!")
        print(f"  Input:  {input_file}")
        print(f"  Output: {output_file}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1

    except PDFTimestampError as e:
        logger.error(f"Timestamping failed: {e}")
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())