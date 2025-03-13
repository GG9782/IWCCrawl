import os
import time

import excelHandler

import iwencaisear
from datetime import datetime


if __name__ == "__main__":
    str_date = input("输入需要查找的日期后回车，格式'y-m-d'，如'2025-1-15'，如果要查今天可以直接回车")
    input_date = datetime.now().date() if str_date == "" else datetime.strptime(str_date, "%Y-%m-%d")
    print("working…")

    # Excel文件路径、sheet名称
    file_path = "data.xlsx"
    sheet_name = "成交额前100"

    # 判断是否已有对应日期的数据
    xlsx_date = excelHandler.get_first_column_values_as_set(file_path, sheet_name)

    # 比较日期
    if input_date in xlsx_date:
        print("data.xlsx中已有(" + str(input_date) + ")的数据，请勿重复抓取数据")
        print("进程将结束")
        time.sleep(5)

    else:
        # 爬取成交额从大到小排名前100 ，同花顺行业
        data = iwencaisear.crawl_100_volume_of_transaction(input_date)

        # 将数据追加到Excel文件并保持格式
        excelHandler.append_data_to_excel_with_format(file_path, sheet_name, data)
        highest = int(iwencaisear.crawl_250_day_highest(input_date))
        lowest = int(iwencaisear.crawl_250_day_lowest(input_date))

        data2 = [{
            'date': input_date,
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
