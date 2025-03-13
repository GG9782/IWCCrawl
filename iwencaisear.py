from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawl_100_volume_of_transaction(input_date):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.headless = True  # 无头模式

    # 禁用自动化控制标志
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # 创建一个新的Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    # 打开目标网页
    url = 'https://www.iwencai.com/unifiedwap/home/index'
    # 成交额从大到小排名前100 ，同花顺行业
    driver.get(url)

    try:

        # 模拟搜索框搜索，等待搜索框变为可交互
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#searchInput'))
        )
        search_box.send_keys(str(input_date).split()[0] +'成交额从大到小排名前100 ，同花顺行业')

        # 点击搜索
        # 定位可点击的<div>元素（使用CSS选择器作为示例）
        clickable_div = driver.find_element(By.CSS_SELECTOR, '#searchInputWrap > div.search-input-outer > div > div.input-base.search-input-box > div.input-base-tools > div > div.num-search > div.search-icon.search-active')
        # 点击<div>元素
        clickable_div.click()

        # 模拟下拉选择修改每页行数
        # 等待下拉选择框加载完成（根据实际情况调整等待条件）
        wait = WebDriverWait(driver, 10)  # 10秒超时
        drop_down = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.drop-down-box span')))

        # 点击下拉选择框以展开选项
        drop_down.click()

        # 等待选项加载完成（根据实际情况，可能需要调整等待时间或条件）
        # 这里假设选项是立即可见的，或者通过其他方式定位选项（如通过文本内容）
        options = driver.find_elements(By.CSS_SELECTOR, '.drop-down-box ul li')

        # 遍历选项，找到“显示100条/页”并点击
        for option in options:
            if option.text == '显示100条/页':
                option.click()
                break

        # 等待表格元素加载完成
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '#iwc-table-container > div.iwc-table-content.isTwoLine > div.iwc-table-scroll > div.iwc-table-body.scroll-style2.big-mark > table > tbody > tr:nth-child(100)'))
        )

        table = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '#iwc-table-container > div.iwc-table-content.isTwoLine > div.iwc-table-scroll > div.iwc-table-body.scroll-style2.big-mark > table > tbody'))
        )

    except Exception as e:
        print(f"Failed to load the target element: {e}")
        driver.quit()
        exit(1)

    # 获取所有行
    rows = table.find_elements(By.CSS_SELECTOR, 'tr')

    # 遍历每一行并提取数据
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        data.append({
            'date': input_date,

            '序号': cols[0].text.strip(),
            '代码': int(cols[2].text.strip()),
            '简称': str(cols[3].text.strip()),
            '现价(元)': cols[4].text.strip(),
            '涨跌幅(%)': cols[5].text.strip(),

            '成交额排名': cols[6].text.strip(),
            '所属概念': cols[7].text.strip(),
            '成交量(股)': cols[8].text.strip(),
            '最新DDE大单净额(元)': cols[9].text.strip(),
            '总股本(元)': cols[10].text.strip(),
            '市盈率(pe)': cols[11].text.strip(),
            '成交额(元)': cols[12].text.strip(),

            '所属同花行业': cols[13],
            '所属同花行业': cols[13].text.strip().split("-")[0],
            '所属同花行业2阶': cols[13].text.strip().split("-")[1],
            '所属同花行业3阶': cols[13].text.strip().split("-")[2]
        })

    # 关闭浏览器
    driver.quit()

    # 返回提取的数据
    return data


def crawl_250_day_highest(input_date):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.headless = True  # 无头模式

    # 禁用自动化控制标志
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # 创建一个新的Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    # 打开目标网页
    # 收盘价创250日新高个股行业
    # 打开目标网页
    url = 'https://www.iwencai.com/unifiedwap/home/index'

    driver.get(url)

    try:
        # 模拟搜索框搜索，等待搜索框变为可交互
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#searchInput'))
        )
        search_box.send_keys(str(input_date).split()[0] + '收盘价创250日新高个股行业')

        # 点击搜索
        # 定位可点击的<div>元素（使用CSS选择器作为示例）
        clickable_div = driver.find_element(By.CSS_SELECTOR,
                                            '#searchInputWrap > div.search-input-outer > div > div.input-base.search-input-box > div.input-base-tools > div > div.num-search > div.search-icon.search-active')
        # 点击<div>元素
        clickable_div.click()

        # 等待表格元素加载完成
        wait = WebDriverWait(driver, 20)

        highest_count = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '#xuan-top-con > div.xuangu-tool > div > div.table-count.xuangu-count-line > div > span.ui-f24.ui-fb.red_text.ui-pl8'))
        )

    except Exception as e:
        print(f"Failed to load the target element: {e}")
        driver.quit()
        exit(1)

    res = highest_count.text.strip()

    # 关闭浏览器
    driver.quit()

    # 返回提取的数据
    return res


def crawl_250_day_lowest(input_date):
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.headless = True  # 无头模式

    # 禁用自动化控制标志
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # 创建一个新的Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    # 打开目标网页
    # 打开目标网页
    url = 'https://www.iwencai.com/unifiedwap/home/index'

    driver.get(url)

    try:
        # 模拟搜索框搜索，等待搜索框变为可交互
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#searchInput'))
        )
        search_box.send_keys(str(input_date).split()[0] + '收盘价创250日新低个股行业')

        # 点击搜索
        # 定位可点击的<div>元素（使用CSS选择器作为示例）
        clickable_div = driver.find_element(By.CSS_SELECTOR,
                                            '#searchInputWrap > div.search-input-outer > div > div.input-base.search-input-box > div.input-base-tools > div > div.num-search > div.search-icon.search-active')
        # 点击<div>元素
        clickable_div.click()

        # 等待表格元素加载完成
        wait = WebDriverWait(driver, 20)

        lowest_count = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '#xuan-top-con > div.xuangu-tool > div > div.table-count.xuangu-count-line > div > span.ui-f24.ui-fb.red_text.ui-pl8'))
        )

    except Exception as e:
        print(f"Failed to load the target element: {e}")
        driver.quit()
        exit(1)

    res = lowest_count.text.strip()

    # 关闭浏览器
    driver.quit()

    # 返回提取的数据
    return res