#!/usr/bin/env python3
"""
简化版公司内部 DeepSeek 模型测试脚本
不依赖外部库，直接使用硬编码配置
"""

import os
import sys
import asyncio

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入所需的类
from browser_use.llm.deepseek.chat import ChatDeepSeek
from browser_use.llm.messages import SystemMessage, HumanMessage

# 硬编码配置
API_KEY = 'c18c900019834d6b8da93bfee69cbc31'
BASE_URL = 'http://easyalgo.jd.com/openapi/deepseek'
MODEL = 'deepseek-chat'

async def test_connection():
    """测试与公司内部 DeepSeek 模型的连接"""
    
    print("🔍 开始测试公司内部 DeepSeek 模型连接...")
    print(f"📡 API 端点: {BASE_URL}")
    print(f"🤖 模型: {MODEL}")
    
    # 配置公司内部 DeepSeek 模型
    llm = ChatDeepSeek(
        model=MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.7,
        max_tokens=1000,
        timeout=60.0,
    )
    
    try:
        # 创建测试消息
        messages = [
            SystemMessage(content="你是一个友好的助手，请用中文回复。"),
            HumanMessage(content="你好，请介绍一下你自己。")
        ]
        
        print("🔄 正在发送测试请求...")
        result = await llm.ainvoke(messages)
        
        print("✅ 连接成功!")
        print(f"📝 响应内容: {result.completion}")
        
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {type(e).__name__}: {str(e)}")
        
        # 提供详细的错误信息
        if "404" in str(e):
            print("🔍 错误分析: 404 错误通常表示 API 端点不存在")
            print("💡 建议检查:")
            print("   1. API 基础 URL 是否正确")
            print("   2. 是否需要添加路径后缀，如 /v1 或 /chat/completions")
            print("   3. 公司内部的 API 端点结构")
        elif "401" in str(e) or "403" in str(e):
            print("🔍 错误分析: 认证错误")
            print("💡 建议检查:")
            print("   1. API 密钥是否正确")
            print("   2. 是否有访问权限")
        elif "timeout" in str(e).lower():
            print("🔍 错误分析: 请求超时")
            print("💡 建议检查:")
            print("   1. 网络连接是否正常")
            print("   2. API 服务是否可用")
        else:
            print("🔍 其他错误，请检查网络连接和 API 配置")
        
        return False

if __name__ == "__main__":
    print("🤖 简化版公司内部 DeepSeek 模型连接测试")
    print("=" * 50)
    
    # 运行连接测试
    success = asyncio.run(test_connection())
    
    if success:
        print("\n🎉 恭喜！公司内部 DeepSeek 模型连接正常")
        print("现在可以运行主测试脚本")
    else:
        print("\n❌ 连接测试失败，请根据错误信息排查问题")
        print("可能需要联系公司 IT 部门确认 API 配置")