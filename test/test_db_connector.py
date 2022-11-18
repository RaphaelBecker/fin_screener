import datetime
import unittest
import pandas_datareader as pdr
import data.db_connector as db_connector

ticker = 'FB'
pair = 'USD'
timeframe = '1d'


class TestDbConnector(unittest.TestCase):

    def test_get_dow_ticker_list(self):
        dow_ticker_list = db_connector.get_dow_ticker_list()
        print(dow_ticker_list)

    def test_get_smp500_ticker_list(self):
        smp500_ticker_list = db_connector.get_smp500_ticker_list()
        print(smp500_ticker_list)

    def test_get_nasdaq_ticker_list(self):
        nasdaq_ticker_list = db_connector.get_nasdaq_ticker_list()
        print(nasdaq_ticker_list)

    def test_get_others_ticker_list(self):
        others_ticker_list = db_connector.get_others_ticker_list()
        print(others_ticker_list)

    def test_fundamental_quote(self):
        """
        <class 'pandas.core.frame.DataFrame'> Transposed:
                           attribute                        value
        0              1y Target Est                       177.61
        1              52 Week Range              129.04 - 182.94
        2                        Ask                149.73 x 1400
        3                Avg. Volume                   88992084.0
        4          Beta (5Y Monthly)                         1.25
        5                        Bid                 149.72 x 900
        6                Day's Range              147.43 - 150.28
        7                  EPS (TTM)                         6.11
        8              Earnings Date  Jan 25, 2023 - Jan 30, 2023
        9           Ex-Dividend Date                 Nov 04, 2022
        10  Forward Dividend & Yield                 0.92 (0.61%)
        11                Market Cap                       2.387T
        12                      Open                       148.97
        13            PE Ratio (TTM)                        24.56
        14            Previous Close                        149.7
        15               Quote Price                   150.059998
        16                    Volume                   50512311.0

        """
        fundamental_quote = db_connector.get_fundamental_quote("aapl")
        print("\nType: ")
        print(type(fundamental_quote))
        print("\nDataframe ")
        print(fundamental_quote)
        print(f"\nprint single value 'Avg. Volume': {fundamental_quote['Avg. Volume'][0]}")

    def test_get_fundamental_stats(self):
        """
        <class 'pandas.core.frame.DataFrame'> Transposed:
                                   0      1
        0      Market Cap (intraday)  2.38T
        1           Enterprise Value  2.45T
        2               Trailing P/E  24.50
        3                Forward P/E  24.33
        4  PEG Ratio (5 yr expected)   2.90
        5          Price/Sales (ttm)   6.20
        6           Price/Book (mrq)  47.00
        7   Enterprise Value/Revenue   6.22
        8    Enterprise Value/EBITDA  18.43
        """
        fundamental_stats_valuation = db_connector.get_fundamental_stats_valuation("aapl")
        print("\nType: ")
        print(type(fundamental_stats_valuation))
        print("\nDataframe ")
        print(fundamental_stats_valuation)
        print(f"\nprint single value 'Market Cap (intraday)': {fundamental_stats_valuation['Market Cap (intraday)'][0]}")

    def test_get_ticker_info(self):
        """
        <class 'pandas.core.frame.DataFrame'> Transposed:
        zip                             95014
        sector                          Technology
        fullTimeEmployees               164000
        longBusinessSummary             Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. In addition, the company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. Further, it provides AppleCare support and cloud services store services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. Additionally, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.
        city                            Cupertino
        phone                           408 996 1010
        state                           CA
        country                         United States
        companyOfficers                 []
        website                         https://www.apple.com
        maxAge                          1
        address1                        One Apple Park Way
        industry                        Consumer Electronics
        ebitdaMargins                   0.33105
        profitMargins                   0.2531
        grossMargins                    0.4331
        operatingCashflow               122151002112
        revenueGrowth                   0.081
        operatingMargins                0.30289
        ebitda                          130541002752
        targetLowPrice                  122
        recommendationKey               buy
        grossProfits                    170782000000
        freeCashflow                    90215251968
        targetMedianPrice               178.5
        currentPrice                    148.28
        earningsGrowth                  0.048
        currentRatio                    0.879
        returnOnAssets                  0.21214
        numberOfAnalystOpinions         40
        targetMeanPrice                 177.61
        debtToEquity                    261.446
        returnOnEquity                  1.75459
        targetHighPrice                 214
        totalCash                       48304001024
        totalDebt                       132480000000
        totalRevenue                    394328014848
        totalCashPerShare               3.036
        financialCurrency               USD
        revenuePerShare                 24.317
        quickRatio                      0.709
        recommendationMean              1.9
        exchange                        NMS
        shortName                       Apple Inc.
        longName                        Apple Inc.
        exchangeTimezoneName            America/New_York
        exchangeTimezoneShortName       EST
        isEsgPopulated                  False
        gmtOffSetMilliseconds           -18000000
        quoteType                       EQUITY
        symbol                          AAPL
        messageBoardId                  finmb_24937
        market                          us_market
        annualHoldingsTurnover          None
        enterpriseToRevenue             6.253
        beta3Year                       None
        enterpriseToEbitda              18.888
        52WeekChange                    -0.018013
        morningStarRiskRating           None
        forwardEps                      6.81
        revenueQuarterlyGrowth          None
        sharesOutstanding               15908100096
        fundInceptionDate               None
        annualReportExpenseRatio        None
        totalAssets                     None
        bookValue                       3.178
        sharesShort                     103178670
        sharesPercentSharesOut          0.0065
        fundFamily                      None
        lastFiscalYearEnd               1663977600
        heldPercentInstitutions         0.60247
        netIncomeToCommon               99802996736
        trailingEps                     6.11
        lastDividendValue               0.23
        SandP52WeekChange               -0.158193
        priceToBook                     46.658276
        heldPercentInsiders             0.00073
        nextFiscalYearEnd               1727136000
        yield                           None
        mostRecentQuarter               1663977600
        shortRatio                      1.14
        sharesShortPreviousMonthDate    1664496000
        floatShares                     15891414476
        beta                            1.246644
        enterpriseValue                 2465621344256
        priceHint                       2
        threeYearAverageReturn          None
        lastSplitDate                   1598832000
        lastSplitFactor                 4:1
        legalType                       None
        lastDividendDate                1667520000
        morningStarOverallRating        None
        earningsQuarterlyGrowth         0.008
        priceToSalesTrailing12Months    5.981956
        dateShortInterest               1667174400
        pegRatio                        2.69
        ytdReturn                       None
        forwardPE                       21.773863
        lastCapGain                     None
        shortPercentOfFloat             0.0065
        sharesShortPriorMonth           103251184
        impliedSharesOutstanding        0
        category                        None
        fiveYearAverageReturn           None
        previousClose                   149.7
        regularMarketOpen               148.97
        twoHundredDayAverage            155.57056
        trailingAnnualDividendYield     0.006012
        payoutRatio                     0.1473
        volume24Hr                      None
        regularMarketDayHigh            150.28
        navPrice                        None
        averageDailyVolume10Day         94688660
        regularMarketPreviousClose      149.7
        fiftyDayAverage                 147.513
        trailingAnnualDividendRate      0.9
        open                            148.97
        toCurrency                      None
        averageVolume10days             94688660
        expireDate                      None
        algorithm                       None
        dividendRate                    0.92
        exDividendDate                  1667520000
        circulatingSupply               None
        startDate                       None
        regularMarketDayLow             147.43
        currency                        USD
        trailingPE                      24.268412
        regularMarketVolume             73374114
        lastMarket                      None
        maxSupply                       None
        openInterest                    None
        marketCap                       2358852976640
        volumeAllCurrencies             None
        strikePrice                     None
        averageVolume                   89292351
        dayLow                          147.43
        ask                             0
        askSize                         1300
        volume                          73374114
        fiftyTwoWeekHigh                182.94
        fromCurrency                    None
        fiveYearAvgDividendYield        1
        fiftyTwoWeekLow                 129.04
        bid                             0
        tradeable                       False
        dividendYield                   0.0061
        bidSize                         1300
        dayHigh                         150.28
        coinMarketCapLink               None
        regularMarketPrice              148.28
        preMarketPrice                  149.74
        logo_url                        https://logo.clearbit.com/apple.com
        trailingPegRatio                2.8961

        """
        ticker_info = db_connector.get_ticker_info("CTVA")
        print(type(ticker_info))
        print(ticker_info.to_string())
        print(ticker_info)
        print(f"Single ticker 'netIncomeToCommon' value: {ticker_info['netIncomeToCommon'][0]}")

    # other tests

    def test_basics(self):
        df_ticker = db_connector.download_ticker_df(ticker, pair, timeframe)
        print(df_ticker)
        print(db_connector.root_dir0)

    def test_add_hlocv_table(self):
        db_connector.add_hlocv_table(ticker, pair, timeframe)

    def test_snapshot(self):
        ticker_list = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT']
        db_connector.snapshot(ticker_list)

    def test_view_all_tickers(self):
        ticker_list = db_connector.view_all_tickers()
        print(ticker_list)
        print('')

    def test_get_hlocv_from_db(self):
        ticker_dict_list = db_connector.view_all_tickers()
        for ticker_dict in ticker_dict_list:
            df_ticker = db_connector.get_hlocv_from_db(ticker_dict['ticker'], ticker_dict['pair'],
                                                       ticker_dict['timeframe'], ticker_dict['market'])
            print(df_ticker)


