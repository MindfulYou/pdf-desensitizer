"""Rule-based sensitive text detection for Chinese PDF text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


SURNAMES = set(
    """
王 李 张 刘 陈 杨 黄 赵 周 吴 徐 孙 马 胡 朱 郭 何 罗 高 林
郑 梁 谢 唐 许 冯 宋 韩 邓 彭 曹 曾 田 萧 潘 袁 蔡 蒋 余 于
杜 叶 程 苏 魏 吕 丁 任 卢 姚 沈 钟 姜 崔 谭 陆 汪 范 金 石
廖 贾 夏 韦 付 方 白 邹 孟 熊 秦 邱 江 尹 薛 闫 段 雷 侯 龙
史 陶 黎 贺 顾 毛 郝 龚 邵 万 钱 严 覃 武 戴 莫 孔 向 汤 温
康 施 文 牛 樊 葛 邢 安 齐 易 乔 伍 庞 颜 倪 庄 聂 章 鲁 岳
翟 殷 詹 申 欧 耿 关 兰 焦 俞 左 柳 甘 祝 包 宁 尚 符 阮 梅
童 凌 毕 单 季 裴 霍 涂 成 谷 曲 娄 盛 纪 舒 柯 管 项 游 饶
刁 祁 连 芦 迟 车 冉 冷 桑 沙 司 卜 邬 尤 滕 匡 吉 鄂 褚 卞
欧阳 司马 诸葛 上官 司徒 东方 独孤 南宫
""".split()
)

NAME_BLACKLIST = {
    "包括", "关于", "对于", "由于", "至于", "作为", "成为", "认为",
    "所以", "可以", "可能", "可是", "可见", "如果", "如何", "为何",
    "任何", "项目", "公司", "方式", "方面", "经济", "经过", "已经",
    "国家", "大家", "专家", "注意", "同意", "任意", "容易", "交易",
    "定义", "说明", "证明", "表明", "根据", "数据", "数字", "部分",
    "全部", "部门", "服务", "任务", "其他", "所有", "特别", "区别",
    "主要", "重要", "必要", "发现", "发展", "发生", "成立", "成功",
    "计划", "规划", "规模", "参加", "参考", "合作", "合同", "合理",
    "提高", "提前", "提供", "进行", "执行", "运行", "管理", "处理",
    "办理", "负责", "承担", "担任", "决定", "解决", "解释", "完成",
    "完善", "完整", "开始", "结束", "结果", "研究", "研发", "开发",
    "生产", "产生", "产品", "实施", "实现", "实际", "规定", "规范",
    "规则", "投资", "投入", "投诉", "支持", "反对", "保证", "整理",
    "调整", "协调", "记录", "记者", "能力", "能够", "功能", "要求",
    "请求", "需求", "问题", "提问", "时间", "时期", "机会", "机构",
}

NAME_SUFFIXES = [
    "先生", "女士", "小姐", "同志", "老师", "教授", "律师", "医生",
    "经理", "总监", "总裁", "董事长", "CEO", "CTO", "CFO", "COO",
    "负责人", "联系人", "经办人", "处长", "局长", "主任", "科长",
    "主席", "书记", "部长", "总", "博士", "硕士", "学士", "工程师",
    "设计师", "咨询师",
]

NAME_PREFIXES = [
    "项目负责人", "技术负责人", "技术顾问", "法务审核", "财务审核",
    "经办人员", "签署代表", "甲方代表", "乙方代表", "丙方代表",
    "甲方", "乙方", "丙方", "客户", "联系人", "负责人", "项目经理",
    "法务", "财务", "销售", "运营", "市场", "人事", "行政", "董事长",
    "总经理", "总监", "经理", "主任", "作者", "编辑", "记者", "发言人",
    "代表", "顾问",
]

SIGNATURE_RE = re.compile(r"(?:签字人|签名|签署人|落款|姓名|署名)[\s：:]*([\u4e00-\u9fff]{2,4})")
NAME_SUFFIX_RE = re.compile("|".join(re.escape(s) for s in sorted(NAME_SUFFIXES, key=len, reverse=True)))
NAME_PREFIX_RE = re.compile(
    r"(?:^|[\s，,。、；;：:\n\r\t（(])("
    + "|".join(re.escape(s) for s in sorted(NAME_PREFIXES, key=len, reverse=True))
    + r")[\s：:]*([\u4e00-\u9fff]{2,4})"
)
LABEL_LIST_RE = re.compile(
    r"(?:"
    + "|".join(re.escape(s) for s in sorted(NAME_PREFIXES, key=len, reverse=True))
    + r")[\s：:]*([\u4e00-\u9fff]{2,4}(?:[、,，]\s*[\u4e00-\u9fff]{2,4})+)"
)
VERB_CONTEXT_RE = re.compile(
    r"(?:由|经|请|让|派|给|向|跟|和|与|同|叫|被|把|将|对)"
    r"([\u4e00-\u9fff]{2,4})"
    r"(?:负责|审批|撰写|草拟|处理|办理|执行|提交|报告|联系|回复|对接|跟进|审核|"
    r"签署|签字|确认|落实|协调|组织|主持|参与|协助)"
)

COMPANY_SUFFIXES = [
    "有限责任公司", "股份有限公司", "集团有限公司", "集团公司",
    "有限公司", "股份公司", "责任公司", "事务所", "集团", "企业",
]
COMPANY_SUFFIX_RE = re.compile("|".join(re.escape(s) for s in sorted(COMPANY_SUFFIXES, key=len, reverse=True)))
COMPANY_LEADING_STOPS = [
    "特此感谢", "感谢", "交由", "委托", "授权", "指定", "指派", "涉及单位",
    "协作方", "供应商", "客户", "甲方", "乙方", "丙方", "与", "和", "及",
    "以及", "给", "向", "由", "的",
]
COMPANY_BLACKLIST_RE = re.compile(
    r"^(?:本|该|此|某|贵|我|各|这|那|子|分|总|母|所有|一切|每个|各个)(?:公司|集团|企业)"
)


@dataclass(frozen=True)
class DetectionResult:
    names: list[str]
    companies: list[str]
    organizations: list[str]
    aliases: list[str]
    locations: list[str]


def is_valid_name_candidate(text: str) -> bool:
    if not text or len(text) < 2 or len(text) > 4:
        return False
    if not all("\u4e00" <= ch <= "\u9fff" for ch in text):
        return False
    if text in NAME_BLACKLIST:
        return False
    if text[:2] in SURNAMES:
        return True
    return text[0] in SURNAMES


def _trim_to_name(text: str) -> str | None:
    for suffix in sorted(NAME_SUFFIXES, key=len, reverse=True):
        if text.endswith(suffix):
            text = text[: -len(suffix)]
            break
    for length in (4, 3, 2):
        value = text[:length]
        if is_valid_name_candidate(value):
            return value
    return None


def _extract_name_before_suffix(text: str, suffix_start: int) -> str | None:
    before = text[max(0, suffix_start - 6):suffix_start]
    before = re.sub(r".*[^\u4e00-\u9fff]", "", before)
    for length in (4, 3, 2):
        value = before[-length:]
        if is_valid_name_candidate(value):
            return value
    return None


def find_chinese_names_in_text(text: str) -> list[str]:
    found: set[str] = set()

    for match in NAME_SUFFIX_RE.finditer(text):
        name = _extract_name_before_suffix(text, match.start())
        if name:
            found.add(name)

    for match in NAME_PREFIX_RE.finditer(text):
        name = _trim_to_name(match.group(2))
        if name:
            found.add(name)

    for match in SIGNATURE_RE.finditer(text):
        name = _trim_to_name(match.group(1))
        if name:
            found.add(name)

    for match in VERB_CONTEXT_RE.finditer(text):
        name = _trim_to_name(match.group(1))
        if name:
            found.add(name)

    for match in LABEL_LIST_RE.finditer(text):
        for part in re.split(r"[、,，]\s*", match.group(1)):
            name = _trim_to_name(part)
            if name:
                found.add(name)

    return sorted(found, key=lambda v: (text.find(v), v))


def _clean_company_candidate(candidate: str) -> str:
    candidate = candidate.strip(" \t\r\n，,。、；;：:（）()「」『』[]【】")
    changed = True
    while changed:
        changed = False
        for stop in sorted(COMPANY_LEADING_STOPS, key=len, reverse=True):
            pos = candidate.rfind(stop)
            if pos >= 0:
                next_value = candidate[pos + len(stop):].strip(" \t\r\n，,。、；;：:（）()")
                if next_value and next_value != candidate:
                    candidate = next_value
                    changed = True
                    break
    return candidate


def find_company_names(text: str) -> list[str]:
    found: set[str] = set()
    for match in COMPANY_SUFFIX_RE.finditer(text):
        suffix_start = match.start()
        suffix = match.group(0)
        prefix = text[max(0, suffix_start - 36):suffix_start]
        prefix = re.split(r"[\n\r\t，,。、；;：:！!？?（）()「」『』\[\]【】]", prefix)[-1]
        candidate = _clean_company_candidate(prefix + suffix)
        if len(candidate) < 4:
            continue
        if not ("\u4e00" <= candidate[0] <= "\u9fff"):
            continue
        if COMPANY_BLACKLIST_RE.match(candidate):
            continue
        if re.match(r"^[\d０１２３４５６７８９]+", candidate):
            continue
        found.add(candidate)

    ordered = sorted(found, key=len, reverse=True)
    final: list[str] = []
    for value in ordered:
        if not any(value != other and value in other for other in ordered):
            final.append(value)
    return sorted(final, key=lambda v: (text.find(v), v))


ORG_SUFFIXES = [
    "委员会", "管理委员会", "人民政府", "政府", "公安局", "税务局", "市场监督管理局",
    "法院", "检察院", "司法局", "财政局", "教育局", "人社局", "民政局", "商务局",
    "大学", "学院", "学校", "中学", "小学", "医院", "银行", "证券", "保险",
    "研究院", "研究所", "设计院", "实验室", "中心", "协会", "商会", "基金会",
    "事务中心", "服务中心", "管理中心", "产业园", "园区", "分行", "支行",
]
ORG_SUFFIX_RE = re.compile("|".join(re.escape(s) for s in sorted(ORG_SUFFIXES, key=len, reverse=True)))
ORG_LEADING_STOPS = COMPANY_LEADING_STOPS + [
    "主办单位", "承办单位", "协办单位", "主管部门", "监管部门", "报送", "提交",
    "发送", "抄送", "致", "至", "来自",
]

LOCATION_NAMES = [
    "北京", "北京市", "上海", "上海市", "天津", "天津市", "重庆", "重庆市",
    "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建",
    "江西", "山东", "河南", "湖北", "湖南", "广东", "海南", "四川", "贵州",
    "云南", "陕西", "甘肃", "青海", "台湾", "内蒙古", "广西", "西藏", "宁夏",
    "新疆", "香港", "澳门",
    "石家庄", "太原", "沈阳", "长春", "哈尔滨", "南京", "杭州", "合肥", "福州",
    "南昌", "济南", "郑州", "武汉", "长沙", "广州", "深圳", "珠海", "佛山",
    "东莞", "中山", "南宁", "海口", "成都", "贵阳", "昆明", "西安", "兰州",
    "西宁", "银川", "乌鲁木齐", "苏州", "无锡", "常州", "宁波", "厦门", "青岛",
    "大连",
]
LOCATION_SUFFIX_RE = re.compile(
    r"[\u4e00-\u9fff]{2,12}(?:省|市|区|县|镇|乡|街道|路|街|大道|园区|新区|开发区|高新区)"
)


def _clean_org_candidate(candidate: str) -> str:
    candidate = candidate.strip(" \t\r\n，,。、；;：:（）()「」『』[]【】")
    changed = True
    while changed:
        changed = False
        for stop in sorted(ORG_LEADING_STOPS, key=len, reverse=True):
            pos = candidate.rfind(stop)
            if pos >= 0:
                next_value = candidate[pos + len(stop):].strip(" \t\r\n，,。、；;：:（）()")
                if next_value and next_value != candidate:
                    candidate = next_value
                    changed = True
                    break
    return candidate


def find_organization_names(text: str) -> list[str]:
    found: set[str] = set()
    for match in ORG_SUFFIX_RE.finditer(text):
        suffix_start = match.start()
        suffix = match.group(0)
        prefix = text[max(0, suffix_start - 36):suffix_start]
        prefix = re.split(r"[\n\r\t，,。、；;：:！!？?（）()「」『』\[\]【】]", prefix)[-1]
        candidate = _clean_org_candidate(prefix + suffix)
        if len(candidate) < 4:
            continue
        if not ("\u4e00" <= candidate[0] <= "\u9fff"):
            continue
        found.add(candidate)
    return sorted(found, key=lambda v: (text.find(v), v))


def derive_aliases(terms: Iterable[str]) -> list[str]:
    aliases: set[str] = set()
    suffixes = sorted(COMPANY_SUFFIXES + ORG_SUFFIXES, key=len, reverse=True)
    location_prefixes = sorted(LOCATION_NAMES, key=len, reverse=True)
    for term in terms:
        base = term
        for suffix in suffixes:
            if base.endswith(suffix):
                base = base[: -len(suffix)]
                break
        for location in location_prefixes:
            if base.startswith(location) and len(base) - len(location) >= 2:
                base = base[len(location):]
                break
        base = base.strip(" \t\r\n，,。、；;：:（）()")
        if 2 <= len(base) <= 12 and all("\u4e00" <= ch <= "\u9fff" for ch in base):
            aliases.add(base)
        if len(base) >= 4:
            short2 = base[:2]
            if all("\u4e00" <= ch <= "\u9fff" for ch in short2):
                aliases.add(short2)
        if len(base) >= 4:
            short = base[:4]
            if all("\u4e00" <= ch <= "\u9fff" for ch in short):
                aliases.add(short)
    return sorted(aliases)


def find_locations(text: str) -> list[str]:
    found = {name for name in LOCATION_NAMES if name in text}
    for match in LOCATION_SUFFIX_RE.finditer(text):
        value = match.group(0)
        if len(value) <= 16:
            found.add(value)
    return sorted(found, key=lambda v: (text.find(v), v))


def find_sensitive_items(text: str) -> DetectionResult:
    names = find_chinese_names_in_text(text)
    companies = find_company_names(text)
    organizations = find_organization_names(text)
    aliases = [value for value in derive_aliases(companies + organizations) if value in text]
    locations = find_locations(text)
    return DetectionResult(
        names=names,
        companies=companies,
        organizations=organizations,
        aliases=aliases,
        locations=locations,
    )
