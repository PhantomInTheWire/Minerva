from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

pdf_converter = None

async def init_converter():
    global pdf_converter
    print("Initializing PDFConverter...")
    pdf_converter = PdfConverter(artifact_dict=create_model_dict())

def get_converter():
    return pdf_converter

