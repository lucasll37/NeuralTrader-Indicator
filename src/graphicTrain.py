from variable import stepsFoward, stepsShow, symbol, stepsShow
import os
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TKAgg')


def graphicTrain(frameCurrent,
                 RScore,
                 prediction,
                 indLucas,
                 priceTrader,
                 CoefAng,
                 delta,
                 stopLoss,
                 takeProfit,
                 std,
                 outdir,
                 action,
                 y):

    timeTotal = frameCurrent.index

    fig, axlist = mpf.plot(frameCurrent.iloc[-stepsShow:, :],
                           type='candle',  # ohlc, candle, line
                           returnfig=True,
                           volume=True,
                           show_nontrading=True,
                           datetime_format="%b %d, %H:%M",
                           xrotation=0,
                           figscale=2.0,
                           figratio=(3, 2),
                           figsize=(15, 10),
                           title="NeuralTrader - Training",
                           axtitle='{} ({} UTC+3)'.format(symbol,
                                                          frameCurrent.index[-stepsFoward]),
                           style='classic',  # binance, classic, yahoo
                           panel_ratios=(6, 1),
                           ylabel='Price',
                           ylabel_lower='Ticket\nVolume',
                           tight_layout=False)

    axlist[0].plot(timeTotal[-stepsFoward:],
                   y.reshape(stepsFoward,),
                   linewidth=2.0,
                   label='tg(Θ): {:.3f}'.format(CoefAng),
                   c='#ff0000')

    axlist[0].plot(timeTotal[-stepsShow:],
                   np.ones((stepsShow,), dtype=float) * priceTrader,
                   linewidth=0.5,
                   c='#808080',
                   label='Ind. Lucas: {:.3f}'.format(indLucas),
                   ls=':')

    axlist[0].plot(timeTotal[-stepsFoward:],
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
                   label='Delta: {:.1f} pip(s)'.format(np.abs(delta) * 10000),
                   ls=':')

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
                              title='Metrics',
                              borderpad=0.5,
                              labelspacing=0.5)

    nameGraphic = '{}.png'.format(
        frameCurrent.index[-1].strftime('%Y-%m-%d %Hh%Mm%Ss'))
    fullname = os.path.join(outdir, nameGraphic)

    plt.savefig(fullname)
    plt.close(fig)
