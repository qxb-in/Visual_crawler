import torch
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument
from transformers import AutoProcessor, AutoModelForVision2Seq
from pathlib import Path
from transformers.image_utils import load_image


DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# Initialize processor and model
processor = AutoProcessor.from_pretrained("model/SmolDocling-256M-preview")
model = AutoModelForVision2Seq.from_pretrained(
    "model/SmolDocling-256M-preview",
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2" if DEVICE == "cuda:0" else "eager",
).to(DEVICE)


def inference(image_path, output_path):
    # Create input messages
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Convert this page to docling."}
            ]
        },
    ]

    # Load imagespip 
    image = load_image(image_path)

    # Prepare inputs
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    # Generate outputs
    generated_ids = model.generate(**inputs, max_new_tokens=8192)
    print("正在转换Doc")
    prompt_length = inputs.input_ids.shape[1]
    trimmed_generated_ids = generated_ids[:, prompt_length:]
    doctags = processor.batch_decode(
        trimmed_generated_ids,
        skip_special_tokens=False,
    )[0].lstrip()

    # Populate document
    doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
    # print(doctags)
    # create a docling document
    doc = DoclingDocument(name="Document")
    doc.load_from_doctags(doctags_doc)

    # export as any format
    # HTML
    # Path("Out/").mkdir(parents=True, exist_ok=True)
    # output_path_html = Path("Out/") / "example.html"
    # doc.save_as_html(output_path_html)
    # MD

    with open(output_path, "w") as f:
        f.write(doc.export_to_markdown())



inference("data/image/paper.png", "data/markdown/paper.md")


inference("data/image/paper2.png", "data/markdown/paper2.md")