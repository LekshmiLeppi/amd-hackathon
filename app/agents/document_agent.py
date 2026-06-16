
from app.services.document_parser import DocumentParser

class DocumentAgent:

    @staticmethod
    def process(path):
        return DocumentParser.parse(path)
