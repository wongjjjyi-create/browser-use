#!/usr/bin/env python3
"""
优化后的DeepSeek模型调用脚本
用于浏览器自动化测试，使用DeepSeek大模型
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# 导入DeepSeek相关的类
from browser_use import Agent, Browser
from browser_use.llm.deepseek.chat import ChatDeepSeek

# 加载环境变量
load_dotenv()

async def main():
    """主函数：执行浏览器自动化测试"""
    
    # 配置DeepSeek模型
    # 支持多种DeepSeek模型：deepseek-chat, deepseek-coder等
    llm = ChatDeepSeek(
        model='DeepSeek-V3',  # 或 'deepseek-coder' 用于编码任务
        api_key=os.getenv('DEEPSEEK_API_KEY'),  # 从环境变量获取API密钥
        base_url=os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),  # 支持自定义端点
        temperature=0.7,  # 控制创造性
        max_tokens=2000,  # 最大token数
        timeout=120.0,  # 超时时间
    )

    # 配置浏览器
    browser = Browser(
        headless=False,  # 可视化模式便于调试
        disable_security=True,  # 禁用安全限制
    )

    # 测试URL
    full_url = (
        "http://test.taishan.jd.com/jsf/protection/tab_limit?interfaceName=com.jd.jsf.service.DemoService&showType=0"
    )

    # 定义任务步骤
    task = (
        f"Step 1: Navigate exactly to this URL without any modification:\n{full_url}\n\n"
        "Step 2: 在这个配置页面点击新增\n"
        "Step 3: 接口名输入com.jd.jsf.service.DemoService进行检索并选中，别名填入JSF-COPPER-SIDECAR进行检索并选中，方法填入sayHello进行检索并选中，其他配置用默认值\n"
        "Step 4: 点击提交\n"
        "Step 5: 点击查询\n"
        "Step 6: 查询到的结果中，选择第一个，将操作的开关打开并提交开启\n"
    )

    try:
        # 创建并运行智能体
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            max_actions_per_step=1,  # 每步最多执行一个动作
            use_vision=True,  # 启用视觉能力
        )
        
        print("🚀 开始执行浏览器自动化测试...")
        result = await agent.run(max_steps=20)
        print(f"✅ 测试完成，结果: {result}")
        
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
        raise
    finally:
        # 确保浏览器正确关闭
        await browser.close()

    # 发送HTTP POST请求进行后续测试
    print("📡 发送HTTP请求进行后续验证...")
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8083/run-test"
        data = {
            "testcase": "com.jd.jsf.limit.JSFProviderAiLimitTest",
            "testmethod": "test2"
        }
        
        try:
            async with session.post(url, json=data, timeout=30) as response:
                if response.status == 200:
                    try:
                        result = await response.json()
                        print(f"✅ HTTP请求成功: {result}")
                    except Exception:
                        result = await response.text()
                        print(f"✅ HTTP请求成功，响应内容: {result}")
                else:
                    print(f"⚠️ HTTP请求失败，状态码: {response.status}")
                    text = await response.text()
                    print(f"响应内容: {text}")
        except Exception as e:
            print(f"❌ HTTP请求异常: {e}")

if __name__ == "__main__":
    # 检查必要的API密钥
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("⚠️  请设置 DEEPSEEK_API_KEY 环境变量")
        print("   示例: export DEEPSEEK_API_KEY='your-api-key'")
        exit(1)
    
    print("🤖 使用DeepSeek模型执行浏览器自动化测试")
    asyncio.run(main())