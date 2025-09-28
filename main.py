from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
import json
from pathlib import Path

artifacts_path = "/data2/qinxb/ai_crawler/model/docling_models"

pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)
pipeline_options.ocr_options.lang = ["chi_sim"]  
pipeline_options.ocr_options.force_full_page_ocr = True
doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

source = "/data2/qinxb/ai_crawler/data/image/baidu.jpeg"

result = doc_converter.convert(source)

with open("result.md", "w") as f:
    f.write(result.document.export_to_markdown())

with open("result.json", "w") as f:
    json.dump(result.document.export_to_dict(), f, indent=2, ensure_ascii=False)
