from playwright.async_api import async_playwright
from utils import use_qwen2_5_vl_3b, use_qwen2_5_vl_7b, md5_encode
import asyncio

"""
爬取网页截图，并使用模型提取内容
可能修改参数，例如：
- 修改模型名称："qwen2_5_vl_7b" 和 "qwen2_5_vl_3b"
- 修改网页超时时间: timeout，默认为10s
"""

timeout = 10000

class CrawlerAsync:

    def __init__(self, model_name):
        self.model_name = model_name

    async def capture_webpage_screenshot(self, url, type='png'):
        """
        使用 Playwright 截取网页完整页面截图
        参数：
        - url: 要访问的网页地址
        - type: 图片格式，可以是 png 或 jpeg
        """
        name = md5_encode(url)
        screenshot_path = None  # 用于记录截图路径

        async with async_playwright() as p:
            
            retry_count = 0
            while retry_count < 3:
                # 启动浏览器（默认使用 Chromium，可改为 firefox 或 webkit）
                browser = await p.chromium.launch()
                # 处理弹窗拦截
                page = await browser.new_page(ignore_https_errors=True, java_script_enabled=True)
                # 控制页面大小
                # page.set_viewport_size({"width": 1920, "height": 1080})
                print(f"正在尝试访问 {url} ，重试次数：{retry_count+1}")
                try:
                    # 导航到目标网页（设置超时 30 秒）
                    await page.goto(url, timeout=timeout)
                    if type=="png":
                            # 截取完整页面截图（包含滚动区域）
                        await page.screenshot(
                            path=f"tmp/image/{name}.png",
                            full_page=True,    # 截取完整页面
                            type=type,       # 图片格式（也支持 jpeg）
                            timeout=15000      # 截图操作超时时间
                        )
                        
                        print(f"截图已保存为 tmp/image/{name}.png")
                        screenshot_path = f"tmp/image/{name}.png"

                    elif type=="jpeg":

                        # 截取完整页面截图（包含滚动区域）
                        await page.screenshot(
                            path=f"tmp/image/{name}.jpeg",
                            full_page=True,    # 截取完整页面
                            type=type,       # 图片格式（也支持 jpeg）
                            quality=90,        # 图片质量（仅对 jpeg 有效）
                            timeout=timeout     # 截图操作超时时间
                        )
                        
                        print(f"截图已保存为 tmp/image/{name}.jpeg")
                        screenshot_path = f"tmp/image/{name}.jpeg"
                    break
                except Exception as e:
                    print(f"操作失败：{str(e)}")
                    retry_count += 1
                finally:
                    # 确保关闭浏览器
                    await browser.close()

            return screenshot_path

    async def crawl(self, url):
        # 获取截图path
        image_path = await self.capture_webpage_screenshot(url)

        if image_path:
            if self.model_name == "qwen2_5_vl_3b":
                content = use_qwen2_5_vl_3b(image_path)
                return content
            elif self.model_name == "qwen2_5_vl_7b":
                content = use_qwen2_5_vl_7b(image_path)
                return content
        else:
            return 'ERROR：网页截图失败'

if __name__ == "__main__":

    crawl = CrawlerAsync(model_name="qwen2_5_vl_7b")
    asyncio.run(crawl.crawl("https://baijiahao.baidu.com/s?id=1827624450705506865&wfr=spider&for=pc"))
