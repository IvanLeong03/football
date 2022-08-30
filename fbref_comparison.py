import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from bs4 import BeautifulSoup
from googlesearch import search



url = 'https://www.google.com/search?q=fbref+'



def plot_comparison_graphs(df, str1, str2):
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(12,8))
    fig.suptitle("Comparison of percentiles taken from FBREF")
    
    #graph 1: npg - sca
    part1 = df.iloc[:7]
    metricnames = part1['metric']
    player1 = part1.iloc[:,1]
    player2 = part1.iloc[:,2]
    X = np.arange(len(metricnames))
    barwidth = 0.3
    
    ax1.bar(X - barwidth/2, player1, color='g', width=barwidth, label=str1)
    ax1.bar(X + barwidth/2, player2, color='r', width=barwidth, label=str2)
    ax1.set_ylabel('Percentile')
    ax1.set_xticks(X, metricnames)
    ax1.legend()

    #graph 2: passes att - prog pass rec
    part2 = df.iloc[7:14]
    metricnames = part2['metric']
    player1 = part2.iloc[:,1]
    player2 = part2.iloc[:,2]
    X = np.arange(len(metricnames))
    ax2.bar(X - barwidth/2, player1, color='g', width=barwidth, label=str1)
    ax2.bar(X + barwidth/2, player2, color='r', width=barwidth, label=str2)
    ax2.set_ylabel('Percentile')
    ax2.set_xticks(X, metricnames, fontsize=7)
    ax2.legend()

    #graph 3: pressures - aerials won
    part3 = df.iloc[14:]
    metricnames = part3['metric']
    player1 = part3.iloc[:,1]
    player2 = part3.iloc[:,2]
    X = np.arange(len(metricnames))
    ax3.bar(X - barwidth/2, player1, color='g', width=barwidth, label=str1)
    ax3.bar(X + barwidth/2, player2, color='r', width=barwidth, label=str2)
    ax3.set_ylabel('Percentile')
    ax3.set_xticks(X, metricnames)
    ax3.legend()
    
    
    filename = str1+"_"+str2+".png"
    plt.savefig(filename)
    plt.show()
    

def get_player_percentiles(link):
    url = link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    name = [element.text for element in soup.find_all("span")]
    name = name[7]
    
    metric_names = []
    percentile_values = []
    
    for row in soup.find_all('table')[0].tbody.find_all('tr'):
        contents = row.find_all('th')[0].contents
        metric_names.append(contents)
        
    clean_metric_names = []
    for item in metric_names:
        item = str(item).strip("[']")
        clean_metric_names.append(item)
        
    for row in soup.find_all('table')[0].tbody.find_all('tr'):
        contents = row.find_all('td')[1].contents
        percentile_values.append(contents)

    clean_percentiles = []
    splitat_r = 65
    splitat_l = 67

    for item in percentile_values:
        item = str(item).strip('[]')
        left, right = item[:splitat_l], item[splitat_r:]
        clean_percentiles.append(left)
    
    clean_overall_x = []
    
    for item in clean_percentiles:
        item = str(item).strip('[]')
        left, right = item[:splitat_l], item[splitat_r:]
        clean_overall_x.append(right)
    
    final_percentiles = []
    
    for item in clean_overall_x:
        item = item.replace("<","")
        final_percentiles.append(item)
    
    
    metric_names_no_blanks = []
    percentiles_no_blanks = []
    
    
    
    for i in range(7):
        metric_names_no_blanks.append(clean_metric_names[i])
        percentiles_no_blanks.append(final_percentiles[i])
        
    for j in range(8,15):
        metric_names_no_blanks.append(clean_metric_names[j])
        percentiles_no_blanks.append(final_percentiles[j])
    
    for k in range(16,22):
        metric_names_no_blanks.append(clean_metric_names[k])
        percentiles_no_blanks.append(final_percentiles[k])


    
    
    df = pd.DataFrame({'metric':metric_names_no_blanks,
                       name: percentiles_no_blanks})
    df[name] = df[name].astype(int)
        

    return df

def search_tester(kw1):
    query = kw1 + " fbref"
    for j in search(query, num_results=1, lang="en"):
        link = j   
    return link


if __name__== "__main__":
    p1 = input("Enter name of player 1: ")
    p2 = input("Enter name of player 2: ")
    #get_comparison_graph(p1, p2)
    link1 = search_tester(p1)
    link2 = search_tester(p2)
    df1 = get_player_percentiles(link1)
    df2 = get_player_percentiles(link2)

    df2noaxis = df2.iloc[:, 1]
    combined = pd.concat([df1, df2noaxis],axis=1)
    plot_comparison_graphs(combined, p1, p2)