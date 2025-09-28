from openai import OpenAI
import base64
import hashlib

def md5_encode(input_string):
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    
    # 更新哈希对象的内容
    md5_hash.update(input_string.encode('utf-8'))
    
    # 获取哈希值的十六进制表示
    encoded_string = md5_hash.hexdigest()
    
    return encoded_string

# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

prompt = """
    ##任务
    提取网页图片中的重点文字内容，按阅读顺序和版面格式组合成新文本。
    ##输出
    - 只含主要内容，不含导航栏、页脚、广告等无关信息。
    - 不包含额外信息，仅提取图片中的文字内容。
"""

def use_qwen2_5_vl_7b(image_path):
    client = OpenAI(base_url="", api_key="EMPTY")
    # 使用Qwen2.5-VL-7B模型
    base64_image = encode_image(image_path)
    # 图文多模态调用示例
    response = client.chat.completions.create(
        model="Qwen2.5-VL-7B-Instruct",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ]}
        ],
        max_tokens=32678
    )

    return response.choices[0].message.content

def use_qwen2_5_vl_3b(image_path):
    base64_image = encode_image(image_path)
    client = OpenAI(base_url="", api_key="EMPTY")
    # 图文多模态调用示例
    response = client.chat.completions.create(
        model="Qwen2.5-VL-3B-Instruct",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ]}
        ],
        max_tokens=32678
    )
    return response.choices[0].message.content
