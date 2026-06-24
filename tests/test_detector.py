from pdf_desensitizer.detector import (
    find_chinese_names_in_text,
    find_company_names,
    find_contract_sensitive_terms,
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


def test_finds_contract_amounts_parties_and_account_fields():
    text = """
甲方：北京星河科技有限公司
乙方：上海云杉咨询有限公司
合同金额：人民币壹佰贰拾万元整（￥1,200,000.00元）
纳税人名称：北京星河科技有限公司
纳税人识别号：91110108MA01ABCDE1
办公地址：北京市海淀区知春路88号
电话：010-88886666
手机：13800138000
联系人姓名：陈建国
银行账号：6222 0000 1111 2222 333
"""
    terms = find_contract_sensitive_terms(text)
    assert "北京星河科技有限公司" in terms
    assert "上海云杉咨询有限公司" in terms
    assert "人民币壹佰贰拾万元整" in terms
    assert "￥1,200,000.00元" in terms
    assert "91110108MA01ABCDE1" in terms
    assert "北京市海淀区知春路88号" in terms
    assert "010-88886666" in terms
    assert "13800138000" in terms
    assert "陈建国" in terms
    assert "6222 0000 1111 2222 333" in terms
