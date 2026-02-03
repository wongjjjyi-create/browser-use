#!/usr/bin/env python3
"""
针对公司内部 DeepSeek 模型的测试脚本
使用公司提供的 API 端点和密钥
"""

import os
import sys
import asyncio
import aiohttp

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入 DeepSeek 相关的类
from browser_use import Agent, Browser
from browser_use.llm.deepseek.chat import ChatDeepSeek

async def main():
    """主函数：执行浏览器自动化测试"""
    
    # 配置公司内部 DeepSeek 模型
    llm = ChatDeepSeek(
        model='deepseek-chat',  # 使用标准模型名称
        api_key=os.getenv('DEEPSEEK_API_KEY', 'c18c900019834d6b8da93bfee69cbc31'),
        base_url=os.getenv('DEEPSEEK_BASE_URL', 'http://easyalgo.jd.com/openapi/deepseek'),
        temperature=0.7,
        max_tokens=2000,
        timeout=120.0,
    )

    # 配置浏览器
    browser = Browser(
        headless=False,  # 可视化模式便于调试
        disable_security=True,  # 禁用安全限制
    )

    # 测试 URL
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
            max_actions_per_step=1,
            use_vision=True,
        )
        
        print("🚀 开始使用公司内部 DeepSeek 模型执行浏览器自动化测试...")
        print(f"📡 API 端点: {os.getenv('DEEPSEEK_BASE_URL', 'http://easyalgo.jd.com/openapi/deepseek')}")
        print(f"🤖 模型: deepseek-chat")
        
        result = await agent.run(max_steps=20)
        print(f"✅ 测试完成，结果: {result}")
        
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
        print(f"🔍 错误详情: {type(e).__name__}: {str(e)}")
        raise
    finally:
        # 确保浏览器正确关闭
        await browser.close()

    # 发送 HTTP POST 请求进行后续测试
    print("📡 发送 HTTP 请求进行后续验证...")
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
                        print(f"✅ HTTP 请求成功: {result}")
                    except Exception:
                        result = await response.text()
                        print(f"✅ HTTP 请求成功，响应内容: {result}")
                else:
                    print(f"⚠️ HTTP 请求失败，状态码: {response.status}")
                    text = await response.text()
                    print(f"响应内容: {text}")
        except Exception as e:
            print(f"❌ HTTP 请求异常: {e}")

def validate_config():
    """验证配置"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    base_url = os.getenv('DEEPSEEK_BASE_URL')
    
    print("🔍 验证配置...")
    print(f"   API 密钥: {'✅ 已设置' if api_key else '❌ 未设置'}")
    print(f"   基础 URL: {base_url or 'http://easyalgo.jd.com/openapi/deepseek'}")
    
    if not api_key:
        print("⚠️  请确保设置了 DEEPSEEK_API_KEY 环境变量")
        return False
    
    return True

if __name__ == "__main__":
    print("🤖 使用公司内部 DeepSeek 模型执行浏览器自动化测试")
    print("=" * 60)
    
    # 验证配置
    if not validate_config():
        print("❌ 配置验证失败，请检查环境变量")
        exit(1)
    
    # 运行主程序
    asyncio.run(main())