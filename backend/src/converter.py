from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from .error import FileProcessingError

pdf_converter = None

async def init_converter():
    """
    Asynchronously initializes the global PDF converter instance.
    
    Raises:
        FileProcessingError: If initialization of the PDF converter fails.
    """
    global pdf_converter
    try:
        print("Initializing PDFConverter...")
        pdf_converter = PdfConverter(artifact_dict=create_model_dict())
    except Exception as e:
        raise FileProcessingError(f"Failed to initialize PDF converter: {str(e)}")

def get_converter():
    """
    Retrieves the initialized PDF converter instance.
    
    Raises:
        FileProcessingError: If the PDF converter has not been initialized.
        
    Returns:
        The initialized PDF converter instance.
    """
    if pdf_converter is None:
        raise FileProcessingError("PDF converter is not initialized")
    return pdf_converter
