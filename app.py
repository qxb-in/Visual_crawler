from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from get_screen import capture_webpage_screenshot, capture_webpage_screenshot_async
from image2md import img2md

"""
    首先输入url，将其页面截图完整
    1. 将截图保存为图片
    2. 使用OCR工具将图片中的文字和图片提取出来，并保存为markdown格式的文件
"""

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

@app.post("/crawl_async")
async def crawler_async(request: UrlRequest):
    try :
        url = request.url
        try:
            a = time.time()
            image_path = await capture_webpage_screenshot_async(url)
            b = time.time()
            print("耗时:", b-a)
            
        except Exception as e:
            return "截图获取失败，请检查url是否正确"
        try:
            c = time.time()
            markdown_path = img2md(image_path)
            d = time.time()
            print("耗时:", d-c)
            with open(markdown_path, 'r') as f:
                markdown_content = f.read()
                return markdown_content
        except Exception as e:
            return "解析失败，请检查文件格式是否损坏"

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/crawl")
def crawler(request: UrlRequest):
    try :
        url = request.url
        try:
            a = time.time()
            image_path = capture_webpage_screenshot(url)
            b = time.time()
            print("耗时:", b-a)
            if "Screen_error" in image_path:
                raise HTTPException(status_code=400, detail=image_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail="截图获取失败，请检查url是否正确")
        try:
            c = time.time()
            markdown_path = img2md(image_path)
            d = time.time()
            print("耗时:", d-c)
            with open(markdown_path, 'r') as f:
                markdown_content = f.read()
                return markdown_content
        except Exception as e:
            raise HTTPException(status_code=400, detail="解析失败，请检查文件格式是否损坏")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)