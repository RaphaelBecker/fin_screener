# This python file contains all candlestick pattern from talib lin

import talib
import numpy as np
import indicators.CandlestickPattern.talib_pattern as pattern

print_flag = 'PATTERN_DETECTION: '


def detect_pattern(data, candlestick_patterns):
    for candlestick_pattern, value in candlestick_patterns.items():
        function_name = pattern.candlestick_patterns_func[value]
        print(print_flag + 'Searching pattern:				' + value + ' ...')
        pattern_function = getattr(talib, function_name)
        data[function_name + '_signal'] = np.nan
        try:
            result = pattern_function(data['open'], data['high'], data['low'], data['close'])
            data[function_name + '_signal'] = result.to_frame().replace(0, np.nan).replace(100, 1)
        except IndexError:
            print(print_flag + 'Error!')
            pass
    return data