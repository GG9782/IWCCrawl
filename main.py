import os
import time

import excelHandler
import iwencai
from datetime import datetime

if __name__ == "__main__":
    print("working…")

    # Excel文件路径、sheet名称
    file_path = "data.xlsx"
    sheet_name = "成交额前100"

    # 判断是否已有今天的数据
    xlsx_last_date = excelHandler.get_last_cell_in_first_column(file_path, sheet_name)


    # 获取今天的日期
    today = datetime.now().date()

    # 比较日期
    if xlsx_last_date != "date" and xlsx_last_date.date() == today:
        print("data.xlsx中已有今天(" + str(today) + ")的数据，请勿重复抓取数据")
        print("进程将结束")
        time.sleep(5)

    else:
        # 爬取成交额从大到小排名前100 ，同花顺行业
        data = iwencai.crawl_100_volume_of_transaction()

        # 将数据追加到Excel文件并保持格式
        excelHandler.append_data_to_excel_with_format(file_path, sheet_name, data)
        highest = int(iwencai.crawl_250_day_highest())
        lowest = int(iwencai.crawl_250_day_lowest())

        data2 = [{
            'date': today,
            '250日最高(只)': highest,
            '250日最低(只)': lowest,
            '差值': highest - lowest
        }]

        # Excel文件路径、sheet名称
        sheet_name2 = "250日新高&低"

        # 将数据追加到Excel文件并保持格式
        excelHandler.append_data_to_excel_with_format(file_path, sheet_name2, data2)

        # 打开PBI
        file_path = "PBI.pbix"
        if os.path.exists(file_path):
            try:
                # 使用 os.startfile() 打开文件
                os.startfile(file_path)
            except Exception as e:
                print(f"无法打开文件: {e}")
        else:
            print(f"文件不存在: {file_path}")

        print("完成，程序将关闭")
        time.sleep(3)
