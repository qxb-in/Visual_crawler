import os

from magic_pdf.data.data_reader_writer import FileBasedDataWriter
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.data.read_api import read_local_images

def get_filename(file_path: str) -> str:
    filename_with_extension = os.path.basename(file_path)  # 获取文件名（含扩展名）
    filename, _ = os.path.splitext(filename_with_extension)
    
    return filename

def img2md(image_path):

    image_dir = get_filename(image_path)
    output_dir = f"tmp/markdown/{image_dir}"
    
    os.makedirs(output_dir, exist_ok=True)

    image_writer, md_writer = FileBasedDataWriter(output_dir), FileBasedDataWriter(
        output_dir
    )

    ds = read_local_images(image_path)[0]
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    ds.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(
        md_writer, f"{image_name}.md", image_dir
    )
    return f"{output_dir}/{image_name}.md"
