#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © GuangZhou
"""
光通信产业链知识图谱 + NLP智能查询系统 v2.0
支持自然语言查询 · 动态可视化 · AI智能分析
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from datetime import datetime
import re

# 页面配置
st.set_page_config(
    page_title="光通信产业链AI分析 v2.0",
    page_icon="🔬",
    layout="wide"
)

# 自定义CSS - 现代化风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

    * { font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif; }

    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #f107a3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }

    .sub-title {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.7);
        text-align: center;
        margin-bottom: 2rem;
    }

    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .card:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(0,212,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,212,255,0.15);
    }

    .card-glow {
        background: linear-gradient(135deg, rgba(123,47,247,0.2) 0%, rgba(240,7,163,0.2) 100%);
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 0 30px rgba(0,212,255,0.2);
    }

    .glow-text {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0,212,255,0.5);
    }

    .status-high { color: #ff4757; }
    .status-med { color: #ffa502; }
    .status-low { color: #2ed573; }

    .metric-card {
        background: linear-gradient(135deg, rgba(0,212,255,0.1) 0%, rgba(123,47,247,0.1) 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #fff;
        padding: 0.8rem 1.2rem;
        background: linear-gradient(90deg, rgba(0,212,255,0.2) 0%, transparent 100%);
        border-left: 3px solid #00d4ff;
        border-radius: 0 8px 8px 0;
        margin: 1.5rem 0 1rem 0;
    }

    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .tag-red { background: rgba(255,71,87,0.2); color: #ff4757; border: 1px solid rgba(255,71,87,0.3); }
    .tag-green { background: rgba(46,213,115,0.2); color: #2ed573; border: 1px solid rgba(46,213,115,0.3); }
    .tag-blue { background: rgba(0,212,255,0.2); color: #00d4ff; border: 1px solid rgba(0,212,255,0.3); }
    .tag-purple { background: rgba(123,47,247,0.2); color: #7b2ff7; border: 1px solid rgba(123,47,247,0.3); }
    .tag-yellow { background: rgba(255,165,2,0.2); color: #ffa502; border: 1px solid rgba(255,165,2,0.3); }

    .chat-container {
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
    }

    .chat-message {
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease;
    }

    .chat-user { background: rgba(0,212,255,0.2); border: 1px solid rgba(0,212,255,0.3); }
    .chat-ai { background: rgba(123,47,247,0.2); border: 1px solid rgba(123,47,247,0.3); }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        color: rgba(255,255,255,0.7);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%) !important;
        color: white !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 数据定义 ====================

KNOWLEDGE_GRAPH = {
    "节点": {
        "EML激光器": {"类型": "核心器件", "技术节点": ["10G", "25G", "50G", "100G"], "供应商": ["Lumentum", "II-VI", "三安光电", "武汉敏芯"]},
        "相干DSP": {"类型": "核心器件", "技术节点": ["100G", "400G", "800G"], "供应商": ["Infinera", "Lumentum", "紫光同创"]},
        "硅光芯片": {"类型": "核心器件", "技术节点": ["100G", "200G", "400G", "800G"], "供应商": ["Intel", "Cisco", "中际旭创", "华为海思"]},
        "光模块": {"类型": "成品", "技术节点": ["100G", "200G", "400G", "800G", "1.6T"], "供应商": ["华为", "中际旭创", "光迅科技"]},
        "DCI互联": {"类型": "应用场景", "描述": "数据中心互联", "关键技术": ["相干光通信", "CPO封装"]},
        "AI算力": {"类型": "驱动因素", "描述": "AI大模型训练", "需求": "算力集群互联"},
    },
    "关系": [
        ("EML激光器", "供应", "光模块", "高", "Lumentum占35%市场份额"),
        ("相干DSP", "供应", "光模块", "高", "400G/800G核心芯片"),
        ("硅光芯片", "供应", "光模块", "高", "CPO封装基础"),
        ("AI算力", "驱动", "DCI互联", "极高", "带宽需求爆发"),
        ("DCI互联", "需要", "光模块", "高", "400G-1.6T需求"),
        ("光模块", "依赖", "EML激光器", "极高", "25G/50G EML短缺"),
        ("光模块", "依赖", "相干DSP", "极高", "国产化率不足5%"),
        ("光模块", "依赖", "硅光芯片", "高", "Intel/Cisco主导"),
    ],
    "供应商详情": {
        "Lumentum": {"国家": "美国", "份额": "35%", "产品": ["25G EML", "50G EML"], "状态": "紧张", "产能": "75%"},
        "II-VI Coherent": {"国家": "美国", "份额": "28%", "产品": ["25G EML", "50G EML"], "状态": "紧张", "产能": "70%"},
        "Intel": {"国家": "美国", "份额": "40%", "产品": ["硅光芯片", "CPO"], "状态": "正常", "产能": "90%"},
        "三安光电": {"国家": "中国", "份额": "8%", "产品": ["25G EML"], "状态": "量产", "良率": "72%", "差距": "2年"},
        "中际旭创": {"国家": "中国", "份额": "15%", "产品": ["硅光模块", "400G光模块"], "状态": "量产", "良率": "65%", "差距": "2年"},
        "华为海思": {"国家": "中国", "份额": "20%", "产品": ["光芯片", "400G DSP"], "状态": "受限", "产能": "30%"},
    }
}

SUPPLY_NEWS = [
    {"日期": "2026-05-12", "事件": "Lumentum 50G EML产能紧张", "影响": "交期延长至16周", "级别": "高风险"},
    {"日期": "2026-05-08", "事件": "三安光电25G EML良率提升", "影响": "达75%", "级别": "机会"},
    {"日期": "2026-05-05", "事件": "华为海思扩产受限", "影响": "芯片供应持续紧张", "级别": "关注"},
    {"日期": "2026-04-28", "事件": "中际旭创400G通过海外验证", "影响": "出口市场打开", "级别": "机会"},
    {"日期": "2026-04-20", "事件": "紫光同创DSP研发进展", "影响": "100G DSP进入测试", "级别": "关注"},
    {"日期": "2026-04-15", "事件": "Intel CPO订单爆满", "影响": "优先供应云厂商", "级别": "高风险"},
]

MATRIX_DATA = pd.DataFrame([
    {"产品": "10G EML", "难度": "中", "规模": "50亿", "窗口": "2-3年", "优先级": 5, "标的": "三安光电、光迅科技"},
    {"产品": "25G EML", "难度": "高", "规模": "80亿", "窗口": "2-3年", "优先级": 5, "标的": "三安光电、陕西源杰"},
    {"产品": "50G EML", "难度": "极高", "规模": "120亿", "窗口": "4-5年", "优先级": 4, "标的": "武汉敏芯"},
    {"产品": "400G DSP", "难度": "极高", "规模": "80亿", "窗口": "5-7年", "优先级": 3, "标的": "紫光同创"},
    {"产品": "硅光CPO", "难度": "极高", "规模": "200亿", "窗口": "6-8年", "优先级": 3, "标的": "中际旭创、光子算数"},
    {"产品": "MWDM组件", "难度": "低", "规模": "30亿", "窗口": "1-2年", "优先级": 5, "标的": "光迅科技、博创科技"},
])

PATENTS_DATA = pd.DataFrame([
    {"专利": "共封装光学收发器及光通信系统", "申请人": "Intel", "年份": 2024, "技术": "光电共封装"},
    {"专利": "基于硅光的高速光互连模块", "申请人": "Cisco", "年份": 2024, "技术": "硅光集成"},
    {"专利": "共封装光学接口及方法", "申请人": "华为", "年份": 2023, "技术": "国产CPO"},
    {"专利": "光电子混合集成封装技术", "申请人": "中际旭创", "年份": 2023, "技术": "封装工艺"},
    {"专利": "56GBd光调制器及其制作方法", "申请人": "Lumentum", "年份": 2024, "技术": "高速调制"},
])

MARKET_FORECAST = pd.DataFrame([
    {"年份": 2024, "市场规模(亿美元)": 120, "增速": "18%", "AI驱动占比": "45%"},
    {"年份": 2025, "市场规模(亿美元)": 145, "增速": "21%", "AI驱动占比": "55%"},
    {"年份": 2026, "市场规模(亿美元)": 180, "增速": "24%", "AI驱动占比": "65%"},
    {"年份": 2027, "市场规模(亿美元)": 220, "增速": "22%", "AI驱动占比": "70%"},
])


# ==================== NLP查询引擎 ====================

class NLPQueryEngine:
    """自然语言查询引擎"""

    def __init__(self, kg_data):
        self.kg = kg_data

    def parse_query(self, query):
        """解析自然语言查询"""
        query = query.lower()

        # 意图识别
        intents = {
            "供应链": ["供应", "供应链", "谁在供", "谁提供", "供应商", "缺货"],
            "替代": ["替代", "国产", "国内", "替代品", "替换", "卡脖子"],
            "风险": ["风险", "危机", "紧张", "问题", "风险点"],
            "机会": ["机会", "机会点", "潜力", "增长", "前景"],
            "公司": ["公司", "厂商", "企业", "三安", "华为", "中际"],
            "技术": ["技术", "节点", "速率", "封装", "量产"],
            "专利": ["专利", "知识产权", "发明"],
            "市场": ["市场", "规模", "份额", "增长", "预测"],
        }

        detected_intents = []
        for intent, keywords in intents.items():
            if any(kw in query for kw in keywords):
                detected_intents.append(intent)

        return detected_intents

    def execute_query(self, query):
        """执行查询并返回结果"""
        intents = self.parse_query(query)

        if not intents:
            return self._general_response(query)

        results = []
        for intent in intents:
            if intent == "供应链":
                results.extend(self._query_supply_chain(query))
            elif intent == "替代":
                results.extend(self._query_substitution(query))
            elif intent == "风险":
                results.extend(self._query_risk(query))
            elif intent == "机会":
                results.extend(self._query_opportunity(query))
            elif intent == "公司":
                results.extend(self._query_company(query))
            elif intent == "技术":
                results.extend(self._query_technology(query))
            elif intent == "专利":
                results.extend(self._query_patent(query))
            elif intent == "市场":
                results.extend(self._query_market(query))

        return results if results else self._general_response(query)

    def _query_supply_chain(self, query):
        results = []
        if any(kw in query for kw in ["eml", "激光器", "eML"]):
            results.append({
                "类型": "供应链分析",
                "内容": "**EML激光器供应链情况：**",
                "详情": [
                    "• 全球龙头：Lumentum (美, 35%), II-VI Coherent (美, 28%), 住友电工 (日, 20%)",
                    "• 国内替代：三安光电(量产,良率72%), 武汉敏芯(研发,良率45%)",
                    "• 当前状态：50G EML供应紧张，交期16周",
                    "• 关键缺口：国产50G EML良率不足，量产仍需2-3年"
                ],
                "结论": "短期内高端EML仍依赖进口，国产替代窗口期3-5年"
            })

        if any(kw in query for kw in ["dsp", "相干"]):
            results.append({
                "类型": "供应链分析",
                "内容": "**相干DSP供应链情况：**",
                "详情": [
                    "• 全球龙头：Infinera (美, 30%), Lumentum (美, 25%)",
                    "• 国内替代：紫光同创(研发), 圣邦微(预研)",
                    "• 国产化率：不足5%",
                    "• 关键差距：400G/800G DSP量产需4-5年"
                ],
                "结论": "相干DSP是下一个'卡脖子'环节，战略投资方向"
            })

        return results

    def _query_substitution(self, query):
        results = [{
            "类型": "国产替代分析",
            "内容": "**国产替代进度全景：**",
            "详情": [
                "✅ **已突破**：10G EML(85%), 25G EML(开始), MWDM组件",
                "🔧 **追赶中**：25G EML(65%), 100G光模块(55%), 400G光模块(40%)",
                "📋 **研发中**：50G EML(45%), 400G DSP(30%)",
                "⏳ **规划中**：800G EML, 硅光CPO"
            ],
            "结论": "短期优先10G/25G EML替代，中长期布局50G EML和DSP"
        }]
        return results

    def _query_risk(self, query):
        results = [{
            "类型": "风险分析",
            "内容": "**供应链风险识别：**",
            "详情": [
                "🔴 **高风险**：50G EML、400G DSP、硅光芯片",
                "🟡 **中风险**：25G EML、高速连接器",
                "🟢 **低风险**：CWDM/DWDM组件",
                "⚠️ **受控风险**：华为海思受限（产能30%）"
            ],
            "结论": "高端光芯片是最大风险点，建议建立备选供应链"
        }]
        return results

    def _query_opportunity(self, query):
        results = [{
            "类型": "机会分析",
            "内容": "**国产替代机会点：**",
            "详情": [
                "⭐ **高优先级机会**：",
                "  - 10G/25G EML：三安光电已量产，良率75%，机会窗口2-3年",
                "  - MWDM组件：技术难度低，市场30亿，窗口1-2年",
                "⭐ **中优先级机会**：",
                "  - 50G EML：武汉敏芯研发中，窗口4-5年",
                "  - 400G相干DSP：紫光同创，窗口5-7年",
                "⭐ **战略布局**：硅光CPO，200亿市场，窗口6-8年"
            ],
            "结论": "建议立即启动国产EML供应商验证，3-6个月完成"
        }]
        return results

    def _query_company(self, query):
        results = []
        if "三安" in query:
            results.append({
                "类型": "公司分析",
                "内容": "**三安光电分析：**",
                "详情": [
                    "📊 **基本信息**：成立2000年，厦门，LED龙头转型光通信",
                    "🔬 **技术能力**：氮化镓/砷化镓外延，4/6英寸产线",
                    "📈 **产品进展**：25G EML已量产(良率72%)，50G EML研发中",
                    "💰 **投资建议**：审慎推荐，重点跟踪25G进展，目标价待定"
                ],
                "结论": "三安光电是国产EML替代首选标的"
            })

        if "华为" in query:
            results.append({
                "类型": "公司分析",
                "内容": "**华为/海思分析：**",
                "详情": [
                    "📊 **市场地位**：光模块市场份额20%，国内第一",
                    "⚠️ **受限情况**：芯片扩产受限，产能30%",
                    "🔬 **技术储备**：400G DSP已量产，硅光700nm已验证",
                    "📈 **战略方向**：自研为主，供应链国产化"
                ],
                "结论": "华为受限为国产替代打开空间，关注其他国内厂商"
            })

        return results

    def _query_technology(self, query):
        results = []
        if "cpo" in query.lower():
            results.append({
                "类型": "技术分析",
                "内容": "**CPO（共封装光学）技术：**",
                "详情": [
                    "📊 **技术优势**：功耗降低40%，带宽密度提升5倍",
                    "🏭 **全球布局**：Intel(40%), Cisco(25%), Juniper(15%)",
                    "🇨🇳 **国内进展**：中际旭创已量产，华为海思已验证",
                    "📅 **演进路线**：100G QSFP → 400G QSFP → 800G OSFP → 1.6T CPO"
                ],
                "结论": "CPO是下一代数据中心主流，国内差距2-3年"
            })

        if any(kw in query for kw in ["硅光", "silicon"]):
            results.append({
                "类型": "技术分析",
                "内容": "**硅光技术分析：**",
                "详情": [
                    "📊 **技术优势**：集成度高，成本低，适合CPO封装",
                    "🏭 **全球布局**：Intel主导(40%)，Cisco紧随(25%)",
                    "🇨🇳 **国内进展**：中际旭创65%良率，华为海思70%良率",
                    "⚠️ **差距**：与Intel仍有2年差距，量产经验不足"
                ],
                "结论": "硅光是CPO时代基础，国内正在追赶"
            })

        return results

    def _query_patent(self, query):
        results = [{
            "类型": "专利分析",
            "内容": "**CPO相关核心专利：**",
            "详情": [
                "1. Intel - 共封装光学收发器及光通信系统 (2024)",
                "2. Cisco - 基于硅光的高速光互连模块 (2024)",
                "3. 华为 - 共封装光学接口及方法 (2023)",
                "4. 中际旭创 - 光电子混合集成封装技术 (2023)",
                "5. Lumentum - 56GBd光调制器及其制作方法 (2024)"
            ],
            "结论": "美企主导CPO专利，国内需加强封装工艺专利布局"
        }]
        return results

    def _query_market(self, query):
        results = [{
            "类型": "市场分析",
            "内容": "**光通信市场预测：**",
            "详情": [
                "📈 **市场规模**：2024年120亿美元 → 2027年220亿美元",
                "📊 **CAGR**：21% (2024-2027)",
                "🤖 **AI驱动**：占比从45%提升至70%",
                "🔑 **关键驱动**：GPU集群互联、长距离DCI扩容、能耗优化"
            ],
            "结论": "AI算力需求是市场增长核心动力，CAGR 21%"
        }]
        return results

    def _general_response(self, query):
        return [{
            "类型": "通用分析",
            "内容": "**关于您的问题：**",
            "详情": [
                "我可以从以下维度分析光通信产业链：",
                "• 供应链：查询各类芯片的供应情况",
                "• 国产替代：查看国产化进度和机会",
                "• 风险分析：识别供应链风险点",
                "• 机会挖掘：发现投资机会",
                "• 公司分析：了解特定公司情况",
                "• 技术趋势：分析CPO、硅光等技术",
                "• 专利分析：查看相关专利布局",
                "• 市场预测：了解市场规模增长"
            ],
            "结论": "请尝试更具体的查询，如：'50G EML供应链情况' 或 '三安光电分析'"
        }]


# ==================== 可视化组件 ====================

def create_supply_chain_chart():
    """创建供应链关系图"""
    fig = go.Figure()

    # 节点数据
    nodes = {
        "AI算力": {"x": 0.5, "y": 1, "color": "#ff4757", "size": 30},
        "DCI互联": {"x": 0.5, "y": 0.7, "color": "#ffa502", "size": 25},
        "光模块": {"x": 0.5, "y": 0.4, "color": "#2ed573", "size": 30},
        "EML激光器": {"x": 0.2, "y": 0.2, "color": "#00d4ff", "size": 20},
        "相干DSP": {"x": 0.5, "y": 0.15, "color": "#00d4ff", "size": 20},
        "硅光芯片": {"x": 0.8, "y": 0.2, "color": "#00d4ff", "size": 20},
    }

    # 绘制节点
    for node, attrs in nodes.items():
        fig.add_trace(go.Scatter(
            x=[attrs["x"]],
            y=[attrs["y"]],
            mode='markers+text',
            marker=dict(size=attrs["size"], color=attrs["color"], line=dict(width=2, color='#fff')),
            text=node,
            textposition="top center",
            textfont=dict(color="#fff", size=12),
            hovertemplate=f"{node}<extra></extra>"
        ))

    # 绘制连线
    connections = [
        ("AI算力", "DCI互联"), ("DCI互联", "光模块"),
        ("光模块", "EML激光器"), ("光模块", "相干DSP"), ("光模块", "硅光芯片")
    ]

    for start, end in connections:
        fig.add_trace(go.Scatter(
            x=[nodes[start]["x"], nodes[end]["x"]],
            y=[nodes[start]["y"], nodes[end]["y"]],
            mode='lines',
            line=dict(color='rgba(0,212,255,0.5)', width=3),
            hoverinfo='skip'
        ))

    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, 1.2]),
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


def create_market_chart():
    """创建市场预测图"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=MARKET_FORECAST["年份"],
        y=MARKET_FORECAST["市场规模(亿美元)"],
        name="市场规模",
        marker_color='rgba(0,212,255,0.8)',
        marker_line_color='rgba(0,212,255,1)',
        marker_line_width=2
    ))

    fig.add_trace(go.Scatter(
        x=MARKET_FORECAST["年份"],
        y=MARKET_FORECAST["AI驱动占比"].str.replace('%', '').astype(float),
        name="AI驱动占比",
        mode='lines+markers',
        line=dict(color='#f107a3', width=3),
        marker=dict(size=10, symbol='circle')
    ), secondary_y=True)

    fig.update_layout(
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(gridcolor='rgba(255,255,255,0.1)', tickformat='%')
    )

    return fig


def create_replacement_chart():
    """创建国产替代进度图"""
    categories = ["10G EML", "25G EML", "50G EML", "400G DSP", "硅光CPO"]
    progress = [85, 65, 30, 15, 25]
    colors = ['#2ed573' if p > 60 else '#ffa502' if p > 30 else '#ff4757' for p in progress]

    fig = go.Figure(go.Bar(
        y=categories[::-1],
        x=progress,
        orientation='h',
        marker_color=colors[::-1],
        marker_line_color='#fff',
        marker_line_width=2,
        text=progress,
        textposition='outside',
        textfont=dict(color='#fff')
    ))

    fig.update_layout(
        height=250,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(title='国产化率 (%)', gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=80)
    )

    return fig


def create_risk_heatmap():
    """创建风险热力图"""
    products = ["EML激光器", "相干DSP", "硅光芯片", "光模块"]
    metrics = ["供应风险", "技术差距", "国产化难度", "市场机会"]

    data = [
        [85, 80, 70, 90],  # EML激光器
        [95, 95, 95, 60],  # 相干DSP
        [75, 70, 85, 75],  # 硅光芯片
        [50, 40, 55, 95],  # 光模块
    ]

    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=metrics,
        y=products,
        colorscale='RdYlGn_r',
        showscale=True,
        text=[["85%", "80%", "70%", "90%"],
              ["95%", "95%", "95%", "60%"],
              ["75%", "70%", "85%", "75%"],
              ["50%", "40%", "55%", "95%"]],
        texttemplate="%{text}",
        textfont={"color": "#fff"}
    ))

    fig.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )

    return fig


def create_company_comparison():
    """创建公司对比图"""
    companies = ["Lumentum", "三安光电", "中际旭创", "华为海思"]
    capacity = [75, 72, 65, 30]
    tech_gap = [0, 2, 2, 0]

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Bar(
        x=companies,
        y=capacity,
        name="产能利用率/良率",
        marker_color='rgba(0,212,255,0.8)',
        marker_line_color='rgba(0,212,255,1)',
        marker_line_width=2
    ))

    fig.update_layout(
        height=280,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="百分比 (%)", gridcolor='rgba(255,255,255,0.1)', range=[0, 100])
    )

    return fig


def create_dci_growth():
    """创建DCI增长图"""
    years = [2024, 2025, 2026, 2027, 2028]
    bandwidth = [50, 85, 140, 200, 280]
    compute = [500, 800, 1200, 1800, 2600]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=years, y=bandwidth,
        name="DCI带宽需求 (Pb/s)",
        mode='lines+markers',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=10, symbol='diamond')
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=years, y=compute,
        name="算力需求 (EFLOPS)",
        mode='lines+markers',
        line=dict(color='#f107a3', width=3),
        marker=dict(size=10, symbol='circle')
    ), secondary_y=True)

    fig.update_layout(
        height=280,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="带宽 (Pb/s)", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="算力 (EFLOPS)", gridcolor='rgba(255,255,255,0.1)')
    )

    return fig


# ==================== NLP查询界面 ====================

def render_nlp_query_section(tab_name="main"):
    """渲染NLP查询界面 - 支持多标签页"""
    st.markdown("---")
    st.markdown('<div class="section-header">🔮 NLP智能查询</div>', unsafe_allow_html=True)

    # 初始化查询引擎和聊天历史
    if 'nlp_engine' not in st.session_state:
        st.session_state.nlp_engine = NLPQueryEngine(KNOWLEDGE_GRAPH)

    # 为每个tab维护独立的聊天历史
    chat_key = f"chat_history_{tab_name}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    # 使用基于tab的动态key
    prefix = f"nlp_{tab_name}"

    # 查询输入
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "nlp_query_input",
            value="",
            placeholder="例如：50G EML供应链情况？三安光电分析？国产替代机会？",
            label_visibility="collapsed",
            key=f"{prefix}_text_input"
        )
    with col2:
        search_clicked = st.button("🔍 查询", width="stretch", key=f"{prefix}_search_btn")

    # 示例查询
    st.markdown("**快捷查询：**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("EML供应链", width="stretch", key=f"{prefix}_btn_eml"):
            query = "EML激光器供应链情况"
            search_clicked = True
    with col2:
        if st.button("国产替代", width="stretch", key=f"{prefix}_btn_replace"):
            query = "国产替代进度"
            search_clicked = True
    with col3:
        if st.button("风险分析", width="stretch", key=f"{prefix}_btn_risk"):
            query = "供应链风险"
            search_clicked = True
    with col4:
        if st.button("投资机会", width="stretch", key=f"{prefix}_btn_opp"):
            query = "投资机会"
            search_clicked = True

    # 执行查询
    if query and search_clicked:
        with st.spinner("AI正在分析..."):
            results = st.session_state.nlp_engine.execute_query(query)

            # 添加到对应tab的历史
            chat_history = st.session_state[chat_key]
            chat_history.append({"role": "user", "content": query})

            for result in results:
                chat_history.append({
                    "role": "assistant",
                    "content": result["内容"],
                    "details": result["详情"],
                    "conclusion": result["结论"]
                })

            st.session_state[chat_key] = chat_history

    # 显示聊天历史
    chat_history = st.session_state.get(chat_key, [])
    if chat_history:
        st.markdown("### 对话历史")
        for msg in chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message chat-user">
                    <strong>👤 您：</strong>{msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message chat-ai">
                    <strong>🤖 AI分析：</strong>{msg['content']}
                    <ul>
                """, unsafe_allow_html=True)
                for detail in msg.get("details", []):
                    st.markdown(f"                <li>{detail}</li>", unsafe_allow_html=True)
                st.markdown("            </ul>")
                st.markdown(f"""
                    <div style="background:rgba(0,212,255,0.1);padding:0.5rem;border-radius:8px;margin-top:0.5rem;">
                        <strong>💡 结论：</strong>{msg.get('conclusion', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.button("🗑️ 清空对话", key=f"{prefix}_btn_clear"):
            st.session_state[chat_key] = []
            st.rerun()


# ==================== 场景展示 ====================

def show_overview():
    """概览页面"""
    st.markdown("### 📊 产业全景")

    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("市场规模", "180亿", "24%↑")
    with col2:
        st.metric("CAGR", "21%", "2024-27")
    with col3:
        st.metric("AI驱动", "65%", "↑20%")
    with col4:
        st.metric("国产化率", "45%", "↑8%")

    # 供应链关系图
    st.plotly_chart(create_supply_chain_chart(), use_container_width=True)

    # 市场预测图
    st.plotly_chart(create_market_chart(), use_container_width=True)


def show_cpo_scenario():
    """CPO场景"""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔬 CPO技术架构")
        st.markdown("""
        **技术优势：**
        - 功耗降低 40%
        - 带宽密度提升 5倍
        - 信号延迟减少 50%

        **产业链位置：**
        - 上游：硅光芯片（Intel主导）
        - 中游：CPO模组封装
        - 下游：AI数据中心
        """)
        st.plotly_chart(create_company_comparison())

    with col2:
        st.markdown("#### 📈 市场预测")
        st.plotly_chart(create_dci_growth())

        st.markdown("""
        **技术演进：**
        ```
        2024        2025        2026        2027+
        ──────────────────────────────────────►
        100G QSFP  400G QSFP   800G OSFP   1.6T CPO
        ```

        **核心结论：CPO成为数据中心互联主流**
        """)


def show_supply_analysis():
    """供应链分析场景"""
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_replacement_chart(), use_container_width=True)

    with col2:
        st.plotly_chart(create_risk_heatmap(), use_container_width=True)

    # 供应商详情表格
    st.markdown("#### 🏢 核心供应商对比")
    supplier_df = pd.DataFrame([
        {"供应商": "Lumentum", "国家": "🇺🇸 美国", "份额": "35%", "产品": "25G/50G EML", "状态": "🔴 紧张", "产能": "75%"},
        {"供应商": "II-VI Coherent", "国家": "🇺🇸 美国", "份额": "28%", "产品": "25G/50G EML", "状态": "🔴 紧张", "产能": "70%"},
        {"供应商": "三安光电", "国家": "🇨🇳 中国", "份额": "8%", "产品": "25G EML", "状态": "✅ 量产", "产能": "72%"},
        {"供应商": "华为海思", "国家": "🇨🇳 中国", "份额": "20%", "产品": "光芯片", "状态": "⚠️ 受限", "产能": "30%"},
    ])
    st.dataframe(supplier_df, use_container_width=True, hide_index=True)


def show_replacement_matrix():
    """国产替代矩阵"""
    # 机会矩阵图
    fig = go.Figure()

    # 象限数据
    opportunities = [
        {"产品": "10G/25G EML", "难度": 30, "价值": 80, "size": 25},
        {"产品": "50G EML", "难度": 70, "价值": 85, "size": 22},
        {"产品": "400G DSP", "难度": 90, "价值": 90, "size": 20},
        {"产品": "硅光CPO", "难度": 85, "价值": 95, "size": 28},
        {"产品": "MWDM", "难度": 20, "价值": 50, "size": 18},
    ]

    for opp in opportunities:
        fig.add_trace(go.Scatter(
            x=[opp["难度"]],
            y=[opp["价值"]],
            mode='markers+text',
            marker=dict(size=opp["size"], color='#00d4ff', line=dict(width=2, color='#fff')),
            text=opp["产品"],
            textposition="top center",
            textfont=dict(color="#fff", size=11)
        ))

    fig.update_layout(
        height=350,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(title="技术难度 →", gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        yaxis=dict(title="市场价值 →", gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        shapes=[
            dict(type="rect", x0=0, y0=50, x1=50, y1=100, fillcolor="rgba(46,213,115,0.1)", line=dict(color="rgba(46,213,115,0.3)")),
            dict(type="rect", x0=50, y0=50, x1=100, y1=100, fillcolor="rgba(255,165,2,0.1)", line=dict(color="rgba(255,165,2,0.3)")),
            dict(type="rect", x0=0, y0=0, x1=50, y1=50, fillcolor="rgba(0,212,255,0.1)", line=dict(color="rgba(0,212,255,0.3)")),
            dict(type="rect", x0=50, y0=0, x1=100, y1=50, fillcolor="rgba(255,71,87,0.1)", line=dict(color="rgba(255,71,87,0.3)")),
        ],
        annotations=[
            dict(text="快速机会", x=25, y=75, showarrow=False, font=dict(color="#2ed573")),
            dict(text="战略投资", x=75, y=75, showarrow=False, font=dict(color="#ffa502")),
            dict(text="基础布局", x=25, y=25, showarrow=False, font=dict(color="#00d4ff")),
            dict(text="长期突破", x=75, y=25, showarrow=False, font=dict(color="#ff4757")),
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    # 机会详情表
    st.markdown("#### 📋 机会详情")
    display_df = MATRIX_DATA.copy()
    display_df["优先级"] = display_df["优先级"].apply(lambda x: "⭐" * x)
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def show_patent_analysis():
    """专利分析场景"""
    st.markdown("#### 📑 核心专利布局")

    patent_display = PATENTS_DATA.copy()
    patent_display["技术"] = patent_display["技术"].apply(
        lambda x: f'<span class="tag tag-blue">{x}</span>'
    )
    st.markdown(
        patent_display.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    # 专利趋势图
    patent_trend = pd.DataFrame({
        "年份": [2020, 2021, 2022, 2023, 2024],
        "CPO相关专利": [45, 68, 95, 132, 178]
    })

    fig = px.line(
        patent_trend,
        x="年份",
        y="CPO相关专利",
        markers=True,
        line_shape="spline"
    )
    fig.update_traces(
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=10, symbol='circle', color='#7b2ff7')
    )
    fig.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)


def show_action_plan():
    """行动计划"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card-glow">
            <h3 style="color:#ff4757;text-align:center;">🔥 立即行动</h3>
            <p style="color:rgba(255,255,255,0.7);text-align:center;">0-6个月</p>
            <ul style="color:#fff;">
                <li>启动国产EML验证</li>
                <li>对接三安光电</li>
                <li>建立备选供应链</li>
                <li>签订长期协议</li>
            </ul>
            <p style="color:#00d4ff;text-align:center;font-weight:bold;">目标：3-6月完成验证</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color:#ffa502;text-align:center;">⏰ 中期布局</h3>
            <p style="color:rgba(255,255,255,0.7);text-align:center;">6-18个月</p>
            <ul style="color:#fff;">
                <li>跟踪50G EML进展</li>
                <li>参与国产DSP开发</li>
                <li>预研CPO封装</li>
                <li>建立技术联盟</li>
            </ul>
            <p style="color:#ffa502;text-align:center;font-weight:bold;">目标：18月形成替代</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="color:#2ed573;text-align:center;">🚀 长期战略</h3>
            <p style="color:rgba(255,255,255,0.7);text-align:center;">18个月+</p>
            <ul style="color:#fff;">
                <li>投资国产芯片企业</li>
                <li>参与行业标准制定</li>
                <li>建立完整供应链</li>
                <li>打造竞争优势</li>
            </ul>
            <p style="color:#2ed573;text-align:center;font-weight:bold;">目标：3-5年自主可控</p>
        </div>
        """, unsafe_allow_html=True)


# ==================== 主程序 ====================

def main():
    # 页面标题
    st.markdown('<div class="main-title">🔬 光通信产业链AI分析系统 v2.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">知识图谱 + NLP智能查询 · 从三超到三智 · 企业智能体底层设计</div>', unsafe_allow_html=True)

    # 标签页
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 概览",
        "🔬 CPO技术",
        "📦 供应链分析",
        "💡 国产替代",
        "📑 专利分析",
        "📋 行动计划"
    ])

    with tab1:
        show_overview()
        render_nlp_query_section("overview")

    with tab2:
        show_cpo_scenario()
        st.markdown("---")
        show_action_plan()

    with tab3:
        show_supply_analysis()
        st.markdown("---")
        render_nlp_query_section("supply")

    with tab4:
        show_replacement_matrix()
        st.markdown("---")
        render_nlp_query_section("replacement")

    with tab5:
        show_patent_analysis()
        st.markdown("---")
        render_nlp_query_section("patent")

    with tab6:
        show_action_plan()
        st.markdown("---")
        st.markdown("#### 🎯 关键成功因素")
        st.markdown("""
        | 因素 | 描述 | 优先级 |
        |------|------|--------|
        | 技术突破 | 50G EML良率提升 | ⭐⭐⭐⭐⭐ |
        | 客户验证 | 华为、中际旭创验证通过 | ⭐⭐⭐⭐ |
        | 产能扩张 | 三安光电产能翻倍 | ⭐⭐⭐⭐ |
        | 成本控制 | 国产芯片成本优势 | ⭐⭐⭐ |
        | 政策支持 | 国产化替代政策 | ⭐⭐⭐ |
        """)

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:rgba(255,255,255,0.5);padding:1rem;">
        <small>
            光通信产业链AI分析系统 v2.0 · 从三超到三智<br>
            Powered by Digital Dimension · 数之境科技<br>
            <span style="color:#00d4ff;">🔮 支持NLP自然语言查询</span>
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()