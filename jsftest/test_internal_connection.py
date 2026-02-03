#!/usr/bin/env python3
"""
测试公司内部 DeepSeek 模型连接的脚本
"""

import os
import sys
import asyncio

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use.llm.deepseek.chat import ChatDeepSeek
from browser_use.llm.messages import SystemMessage, UserMessage

async def test_connection():
    """测试与公司内部 DeepSeek 模型的连接"""
    
    print("🔍 开始测试公司内部 DeepSeek 模型连接...")
    
    # 配置公司内部 DeepSeek 模型
    llm = ChatDeepSeek(
        model='DeepSeek-V3',
        api_key= 'c18c900019834d6b8da93bfee69cbc31',
        base_url='http://easyalgo.jd.com/openapi/deepseek/v1',
        temperature=0.7,
        max_tokens=1000,
        timeout=60.0,
    )
  
    
    try:
        # 创建测试消息
        messages = [
            SystemMessage(content="你是一个友好的助手，请用中文回复。"),
            UserMessage(content="你好，请介绍一下你自己。")
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
            print("   2. 公司内部的 API 端点是否需要特殊配置")
            print("   3. 是否需要添加路径后缀，如 /v1 或 /chat/completions")
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
        
        return False

if __name__ == "__main__":
    print("🤖 公司内部 DeepSeek 模型连接测试")
    print("=" * 50)
    
    
    print("\n" + "=" * 50)
    
    # 运行连接测试
    success = asyncio.run(test_connection())
    
    if success:
        print("\n🎉 恭喜！公司内部 DeepSeek 模型连接正常")
        print("现在可以运行主测试脚本: python jsftest/jsftest_internal_deepseek.py")
    else:
        print("\n❌ 连接测试失败，请根据错误信息排查问题")
        print("可能需要联系公司 IT 部门确认 API 配置")