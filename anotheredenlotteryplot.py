import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from opencc import OpenCC
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

urllist = ['https://api-ap.another-eden.games/asset/lottery_notice/view/f0a49c23fa558a79bafe852e7bd21877?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/7afe777d0db5b4ff6e4af815bfa581af?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/97a81dc5583274dfa58de59e1ec1634d?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/3b50ed8f46da90b471f59f4a1ad48d46?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/1220f766e2263ac4ca23fd583e120bd7?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/654947868f926a8537602606a603291b?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/8024bbdd75f283beaa61b0916ba45478?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/9f96c44b1225fb243321da7d3a3c58c3?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/b43ce2a77226709200bd158baeab4bc3?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/dabdd4a6e65a0aed1d21c00a3e6d0ec7?language=tw','https://api-ap.another-eden.games/asset/lottery_notice/view/adbbf669bf4b88a6a16c0156c700dccb?language=tw']
titlelist = []
dflist = []

font = FontProperties(fname='/system/fonts/NotoSansCJK-Regular.ttc',size=7)


def main():
    response = OpenCC('t2s').convert(requests.get(url).text)
    soup = bs(response, 'html.parser')
    table = soup.find('table')
    title = ''
    for i in soup.h2.stripped_strings:
        if title == '':
            title = repr(i).replace('\'','').replace('\\u3000',' ')
        else:
            title = title+' '+repr(i).replace('\'','')
    print(title)
    dataframe = pd.read_html(str(table),index_col='人物')[0]
    dataframe.replace(r"\(.*\)","",regex=True,inplace=True)
    for i in dataframe:
        for j in dataframe.index.tolist():
            if str(dataframe[i][j]).endswith('%'):
                dataframe[i][j] = float(dataframe[i][j].strip('%'))/100
    dataframe.fillna(0,inplace=True)

    if len(urllist) > 1:
        titlelist.append(title)
        dflist.append(dataframe)

#   dataframecount = pd.DataFrame({'count':[dataframe['★★★'].sum(),dataframe['★★★★'].sum(),dataframe['★★★★★'].sum()]},index=['★★★','★★★★','★★★★★'])

    print(dataframe)

    plt.figure(figsize=(50,50))

    plt.suptitle(title,FontProperties=font)

    pie = plt.subplot(2,2,1)

    pieend = 0
    pieradius = 1

    for i in dataframe:
        plt.pie(dataframe[i].loc[dataframe[i] > 0],labels=dataframe[i].loc[dataframe[i] > 0].index,startangle=pieend,radius=pieradius)
        plt.pie([dataframe[i].sum()],labels=[i+' '+str(dataframe[i].sum())],startangle=pieend,radius=pieradius-0.5,labeldistance=0.3)
        pieend = dataframe[i].sum()*360+pieend
        pieradius = pieradius + 0.1

#    plt.pie(dataframe['★★★'].loc[dataframe['★★★'] > 0],labels=dataframe['★★★'].loc[dataframe['★★★'] > 0].index)
##plt.legend(dataframe['★★★'].loc[dataframe['★★★'] > 0].index,prop=font,loc='center right',bbox_to_anchor=[1.1,0.5])
#    pie3end = dataframe['★★★'].sum()*360
#    plt.pie(dataframe['★★★★'].loc[dataframe['★★★★'] > 0],labels=dataframe['★★★★'].loc[dataframe['★★★★'] > 0].index,startangle=pie3end,radius=1.1)
#    pie4end = (dataframe['★★★'].sum()+dataframe['★★★★'].sum())*360
#    plt.pie(dataframe['★★★★★'].loc[dataframe['★★★★★'] > 0],labels=dataframe['★★★★★'].loc[dataframe['★★★★★'] > 0].index,startangle=pie4end,radius=1.2)
#    plt.pie([dataframe['★★★'].sum()],labels=['★★★ '+str(dataframe['★★★'].sum())],radius=0.5,labeldistance=0.3)
#    plt.pie([dataframe['★★★★'].sum()],labels=['★★★★ '+str(dataframe['★★★★'].sum())],radius=0.6,labeldistance=0.3,startangle=pie3end)
#    plt.pie([dataframe['★★★★★'].sum()],labels=['★★★★★ '+str(dataframe['★★★★★'].sum())],radius=0.7,labeldistance=0.3,startangle=pie4end)
    for i in pie.texts:
        i.set_fontproperties(font)

    bar = plt.subplot(2,2,3)
    bottom = (0,0,0)
    for i in dataframe.index:
        plt.bar(list(dataframe),dataframe.loc[dataframe.index == i].values[0],bottom=bottom,label=i)
        bottom = dataframe.loc[dataframe.index == i].values[0]+bottom
    plt.legend(prop=font,loc='upper left',bbox_to_anchor=(-0.11,1))
    for i in bar.get_xticklabels():
        i.set_fontproperties(font)
    for i in bar.get_yticklabels():
        i.set_fontproperties(font)

    for i in range(len(list(dataframe))):
        plt.text(i,dataframe[list(dataframe)[i]].sum()*1.01,dataframe[list(dataframe)[i]].sum(),ha='center',FontProperties=font)

    pie2 = plt.subplot(2,2,2)
    plt.pie(dataframe.sum(axis=1),labels=dataframe.index)
    for i in pie2.texts:
        i.set_fontproperties(font)

    bar2 = plt.subplot(2,2,4)
    bottom2 = [0]*len(dataframe.index)
    for i in dataframe:
        plt.bar(dataframe.index,dataframe[i],bottom=bottom2,label=i)
        bottom2 = dataframe[i]+bottom2
    plt.legend(prop=font)
    for i in bar2.get_xticklabels():
        i.set_fontproperties(font)
    for i in bar2.get_yticklabels():
        i.set_fontproperties(font)

    for i in range(len(list(dataframe.index))):
        plt.text(i,float(dataframe.loc[dataframe.index == list(dataframe.index)[i]].sum(axis=1))*1.01,float(dataframe.loc[dataframe.index == list(dataframe.index)[i]].sum(axis=1)),ha='center',FontProperties=font)

    plt.savefig('/storage/emulated/0/ADM/'+title+'.svg')
    plt.close()


for url in urllist:
    main()

if len(urllist) > 1:
    plt.figure(figsize=(50,50))

    total = plt.subplot(2,2,1)

    for i in range(len(urllist)):
        plt.bar([x-(len(urllist)/2-i)*0.8/len(urllist) for x in range(len(list(dflist[i])))],dflist[i].sum(),width=0.8/len(urllist),label=titlelist[i])
    plt.xticks(range(len(list(dflist[0]))),list(dflist[0]))
    plt.legend(prop=font)
    for i in total.get_xticklabels():
        i.set_fontproperties(font)
    for i in total.get_yticklabels():
        i.set_fontproperties(font)

    for i in range(len(list(dflist[0]))):
        total = plt.subplot(2,2,2+i)
        plt.title(list(dflist[0])[i],FontProperties=font)
        plt.bar(titlelist,[x[list(dflist[0])[i]].sum() for x in dflist])
        for j in total.get_xticklabels():
            j.set_fontproperties(font)
        for j in total.get_yticklabels():
            j.set_fontproperties(font)

        for j in range(len(urllist)):
            plt.text(j,dflist[j][list(dflist[0])[i]].sum()*1.01,dflist[j][list(dflist[0])[i]].sum(),ha='center',FontProperties=font)

    plt.savefig('/storage/emulated/0/ADM/total.svg')
    plt.close()
