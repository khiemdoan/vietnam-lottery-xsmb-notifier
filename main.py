
__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import asyncio
import sys
from datetime import datetime

import httpx

from messenger import send_message

if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/main/results/xsmb_1_year.csv'
    response = httpx.get(url)
    raw = response.text
    rows = [r for r in raw.split('\n') if len(r) > 0]

    last = rows[-1]
    info = [r for r in last.split(',')]
    date = datetime.strptime(info[0], '%Y-%m-%d').date()
    result = info[1:]

    numbers = [int(r) % 100 for r in result]
    special = numbers[0]

    loto_result = []
    for i in range(10):
        category = sorted([d for d in numbers if d // 10 == i])
        category = [f'{d%10:1d}' for d in category]
        category = ', '.join(category) if len(category) > 0 else '-'
        loto_result.append(category)

    rows = [f'{i}x | {row}' for i, row in enumerate(loto_result)]

    rows.insert(0, f'Số đặc biệt: {special:02d}')
    rows.insert(0, f'Số may mắn ngày: {date:%d-%m-%Y}')
    rows.insert(1, '')
    rows.insert(3, '')
    message = '\n'.join(rows)

    result = asyncio.run(send_message(message))

    sys.exit(int(not result))
