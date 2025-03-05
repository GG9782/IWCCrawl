from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 目标网页的URL
url = 'https://gushitong.baidu.com/top/ab-%E5%85%A8%E9%83%A8-amount-%E6%88%90%E4%BA%A4%E9%A2%9D%E6%A6%9C'

# 设置Chrome选项
options = Options()
options.headless = True  # 无头模式

# 启动Chrome服务
driver = webdriver.Chrome(options=options)

# 打开网页
driver.get(url)

# 等待表格元素加载完成
try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#main > div > div > div > div.wraper > div.list')))
except Exception as e:
    print(f"Failed to load the target element: {e}")
    driver.quit()
    exit(1)
# 无限滚动表，到指定行数
# 初始元素选择器
initial_selector = '#main > div > div > div > div.wraper > div.list > div'

# 初始加载的元素数量
initial_elements = driver.find_elements(By.CSS_SELECTOR, initial_selector)
initial_count = len(initial_elements)

# 目标行数
target_rows = 100

# 当前已加载的行数
current_rows = initial_count

# 循环滚动页面直到加载足够的行数
while current_rows < target_rows:
    # 滚动到底部（或根据需要调整滚动行为）
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 等待新内容加载（可能需要根据页面加载速度调整）
    time.sleep(2)  # 这里假设每次滚动后需要2秒来加载新内容

    # 再次查找元素
    elements = driver.find_elements(By.CSS_SELECTOR, initial_selector)
    new_count = len(elements)

    # 检查是否加载了新内容
    if new_count == current_rows:
        # 如果数量没有增加，可能意味着已经加载了所有可用内容
        break

    # 更新当前行数
    current_rows = new_count

# 提取数据
data = []
for i in range(min(current_rows, target_rows)):
    try:
        element = driver.find_elements(By.CSS_SELECTOR, initial_selector)[i]

        # 提取名称
        name = element.find_element(By.CSS_SELECTOR, 'div.table-left > div > div > div > div.name.c-color').text.strip()

        # 提取代码
        code = element.find_element(By.CSS_SELECTOR,
                                    'div.table-left > div > div > div > div.marking.c-color-gray > span').text.strip()

        # 提取最新价
        latest_price = element.find_element(By.CSS_SELECTOR, 'div.table-right > div:nth-child(1) > div').text.strip()

        # 提取涨跌幅
        rise_fall = element.find_element(By.CSS_SELECTOR,
                                         'div.table-right > div:nth-child(2) > div > span').text.strip()

        # 提取总市值
        total_market_value = element.find_element(By.CSS_SELECTOR,
                                                  'div.table-right > div:nth-child(3) > div > span').text.strip()

        # 提取成交量
        volume = element.find_element(By.CSS_SELECTOR, 'div.table-right > div:nth-child(4) > div').text.strip()

        # 提取成交额
        turnover = element.find_element(By.CSS_SELECTOR, 'div.table-right > div:nth-child(5) > div').text.strip()

        # 提取换手率
        turnover_rate = element.find_element(By.CSS_SELECTOR, 'div.table-right > div:nth-child(6) > div').text.strip()

        # 提取振幅
        amplitude = element.find_element(By.CSS_SELECTOR, 'div.table-right > div:nth-child(7) > div').text.strip()

        # 存储数据
        data.append({
            "名称": name,
            "代码": code,
            "最新价": latest_price,
            "涨跌幅": rise_fall,
            "总市值": total_market_value,
            "成交量": volume,
            "成交额": turnover,
            "换手率": turnover_rate,
            "振幅": amplitude
        })
    except Exception as e:
        print(f"Error extracting data from list item {i + 1}: {e}")

# 关闭浏览器
driver.quit()

# 打印提取的数据
for item in data:
    print(item)
