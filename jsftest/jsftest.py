from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()
# source ~/.venv/bin/activate && python3 jsftest/jsftest.py
async def main():
    llm = ChatBrowserUse(
        browser_config={
            "browser_type": "chrome",
            "user_data_dir": "/Users/wangjingyi32/Library/Application Support/Google/Chrome/Default"
        }
    )

    # 输入要测试的URL
    full_url = (
        "http://test.taishan.jd.com/jsf/protection/tab_limit?interfaceName=com.jd.jsf.service.DemoService&showType=0"
    )
    # 按照步骤在页面执行操作
    task = (
        f"Step 1: Navigate exactly to this URL without any modification:\n{full_url}\n\n"
        "Step 2: 在这个配置页面点击新增\n"
        "Step 3: 接口名输入com.jd.jsf.service.DemoService进行检索，等待数据加载完毕后,可以下拉下拉列表来查找选中,要求必须精确匹配\n"
        "Step 4: 别名填入JSF-COPPER-SIDECAR进行检索,等待数据加载完毕后,可以下拉下拉列表来查找选中,要求必须精确匹配\n"
        "Step 5:方法填入sayHello进行检索,等待数据加载完毕后,可以下拉下拉列表来查找选中,要求必须精确匹配\n"
        "Step 6:其他配置用默认值\n"
        "Step 7: 点击提交\n"
        "Step 8: 点击查询\n"
        "Step 9: 查询到的结果中，选择第一个，将操作的开关打开并提交开启\n"

    )

    agent = Agent(task=task, llm=llm)
    await agent.run()
    
    # 发送HTTP POST请求
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8083/run-test"  # 请替换为实际的API端点
        data = {
            "testcase": "com.jd.jsf.limit.JSFProviderAiLimitTest",
            "testmethod": "test2"
        }
        async with session.post(url, json=data) as response:
            if response.status == 200:
                try:
                    # 尝试解析为JSON
                    result = await response.json()
                    print(f"请求成功: {result}")
                except Exception as e:
                    # 如果不是JSON格式，获取文本内容
                    result = await response.text()
                    print(f"请求成功，但响应不是JSON格式: {result}")
                    print(f"响应内容类型: {response.content_type}")
            else:
                print(f"请求失败，状态码: {response.status}")



if __name__ == "__main__":
    asyncio.run(main())