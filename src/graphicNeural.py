from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from variable import *
import matplotlib
matplotlib.use('TKAgg')


def graphicNeural(rates_frame,
                  prediction,
                  CoefAng,
                  delta,
                  RScore,
                  indLucas,
                  std,
                  y,
                  priceTrader,
                  action,
                  takeProfit,
                  stopLoss,
                  ):

    stepsTotal = stepsBack + stepsFoward
    fowardTime = pd.date_range(
        start=rates_frame.index[-1], periods=stepsFoward, freq='5T')
    timeTotal = pd.date_range(
        start=rates_frame.index[0], periods=stepsTotal, freq='5T')
    fig, axlist = mpf.plot(rates_frame.iloc[-stepsShow+stepsFoward:, :],
                           type='candle',  # ohlc, candle, line
                           returnfig=True,
                           volume=True,
                           show_nontrading=True,
                           datetime_format="%b %d, %H:%M",
                           xrotation=0,
                           figscale=2.0,
                           figratio=(3, 2),
                           figsize=(15, 10),
                           title="NeuralTrader",
                           axtitle='{} ({} UTC-3)'.format(symbol,
                                                          rates_frame.index[-1] - timedelta(hours=6)),
                           style='classic',  # binance, classic, yahoo
                           panel_ratios=(6, 1),
                           ylabel='Price',
                           ylabel_lower='Ticket\nVolume',
                           tight_layout=False)

    axlist[0].plot(fowardTime,
                   y.reshape(stepsFoward,),
                   linewidth=2.0,
                   label='tg(Θ): {:.3f}'.format(CoefAng),
                   c='#000000')

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * priceTrader,
                   linewidth=0.5,
                   c='#808080',
                   label='Delta: {:.1f} pip(s)'.format(np.abs(delta) * 10000),
                   ls=':')

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * priceTrader,
                   linewidth=0.5,
                   c='#808080',
                   label='Ind. Lucas: {:.3f}'.format(indLucas),
                   ls=':')

    axlist[0].plot(fowardTime,
                   prediction.reshape(stepsFoward,),
                   linewidth=1.0,
                   c='#808080',
                   ls='--',
                   label='RScore: {:.3f}'.format(RScore))

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * takeProfit,
                   linewidth=2.0,
                   c='#000000',
                   ls='--',
                   label='Take Profit: {:.5f}'.format(takeProfit))

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * stopLoss,
                   linewidth=2.0,
                   c='#000000',
                   label='Stop Loss: {:.5f}'.format(stopLoss),
                   ls='--')

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * priceTrader,
                   linewidth=0.5,
                   c='#808080',
                   label='Std. Deviation: {:.1f} pip(s)'.format(std * 10000),
                   ls=':')

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * priceTrader,
                   linewidth=0.5,
                   c='#808080',
                   label='Action: {}'.format(action),
                   ls=':')

    legend = axlist[0].legend(loc='upper left',
                              shadow=True,
                              fontsize='medium',
                              numpoints=1,
                              framealpha=0.9,
                              facecolor='#fff',
                              title='METRICS',
                              borderpad=0.5,
                              labelspacing=0.5)

    plt.savefig('./graphics/NeuralTrader/{}.png'.format(
        rates_frame.index[-1].strftime('%Y-%m-%d %Hh%Mm%Ss')))
    plt.close(fig)
