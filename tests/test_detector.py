from pdf_desensitizer.detector import (
    find_chinese_names_in_text,
    find_company_names,
    find_sensitive_items,
)


def test_finds_role_label_names():
    text = "项目负责人：陈建国\n技术顾问：刘洋"
    assert "陈建国" in find_chinese_names_in_text(text)
    assert "刘洋" in find_chinese_names_in_text(text)


def test_finds_name_list_after_label():
    text = "法务审核：周明华、吴小红"
    names = find_chinese_names_in_text(text)
    assert "周明华" in names
    assert "吴小红" in names


def test_finds_verb_context_names():
    text = "本协议由马超草拟，经黄磊先生审批。"
    names = find_chinese_names_in_text(text)
    assert "马超" in names
    assert "黄磊" in names
    assert "黄磊先生" not in names


def test_company_detection_does_not_include_context_prefix():
    text = "特此感谢万科企业股份有限公司与小米科技有限责任公司的技术支持。"
    companies = find_company_names(text)
    assert "万科企业股份有限公司" in companies
    assert "小米科技有限责任公司" in companies
    assert "特此感谢万科企业股份有限公司" not in companies


def test_finds_organizations_aliases_and_locations():
    text = "深圳市南山区人民政府与北京大学、招商银行深圳分行和华为技术有限公司合作。华为在深圳落地。"
    result = find_sensitive_items(text)
    assert "深圳市南山区人民政府" in result.organizations
    assert "北京大学" in result.organizations
    assert "招商银行深圳分行" in result.organizations
    assert "华为技术有限公司" in result.companies
    assert "华为" in result.aliases
    assert "深圳" in result.locations
