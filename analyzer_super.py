import os
import json
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np
from statistics import *

def proc(arquivos):
    geracoes = {}
    geracoes_txt = []
    for a in arquivos["dados"]:
        geracao = a.split(".")[2].split("_")[1]
        idd = a.split(".")[2].split("_")[2]
        try:
            geracoes[geracao].append(a)
        except:
            geracoes[geracao] = [a]
            geracoes_txt.append(int(geracao))

    geracoes_txt.sort()

    # geracoes_txt.pop(0)
    min_geral = float("Infinity")

    ys_min_geral = []
    ys_max_geral = []
    ys_min_geracao = []
    ys_mean = []
    for g in geracoes_txt:
        valores_fuel = []
        for arqs in geracoes[str(g)]:
            dado = None
            try:
                f = open("./output/"+arqs,"r")
                dado = f.read()
                f.close()
                dado = dado.split("\n")
                if dado[-1]=="":
                    dado.pop()
                dado.pop()
                dado.append("</tripinfos>")
                dado = "\n".join(dado)
                f = open("./output/"+arqs,"w")
                f.write(dado)
                f.close()
                f = open("./output/"+arqs,"r")
                dado = f.read()
                dado = ET.fromstring(dado)
                f.close()
            except Exception as e:
                print(arqs)
                print(e)
                print(dado)
                # raise
                continue

            valores_fuel.append(float(dado[0][0].attrib["fuel_abs"]))

        min_geral = min(min_geral, min(valores_fuel))
        #print(g,min_geral)
        ys_min_geral.append(min_geral)
        ys_max_geral.append(max(valores_fuel))
        ys_min_geracao.append(min(valores_fuel))
        ys_mean.append(mean(valores_fuel))
        # print(g, min_geral, round(max(valores_fuel),1), round(min(valores_fuel),1), round(mean(valores_fuel),1))

    # fig, ax = plt.subplots(figsize=(20,4))

    namePlot = 'total_fuel_consuption_Evolution_during_generations'
    fig, ax = plt.subplots()
    # ax.set_ylim(0,300)
    # ax.patch.set_facecolor('#87d3e0')
    # ax.set_xlim(-20,1920)
    ax.plot(geracoes_txt, ys_min_geral,label="Best Solution")
    ax.plot(geracoes_txt, ys_max_geral,label="Worst Generation")
    ax.plot(geracoes_txt, ys_min_geracao,label="Best Generation")
    ax.plot(geracoes_txt, ys_mean,label="Mean Generation")
    #ax.set_title("Evolution during generations")
    ax.legend(numpoints=1, loc="upper right", ncol=2, fontsize='medium')
    ax.set_xlabel('Generations')
    ax.set_ylabel('Total Fuel Consuption (ml/s)')    
    ax.grid(True, which="both", ls="-", linewidth=0.2, color='0.10', zorder=0)
    #plt.yscale('log')
    fig.savefig('plots/'+namePlot+'.png', bbox_inches='tight')
    #fig.savefig('plots/'+namePlot+'.pdf', bbox_inches='tight')
    plt.close(fig)
    #plt.show()

files = os.listdir("./output/")

mapas = {
    "super":{"dados":[]}
}

for f in files:
    f2 = f.split(".")

    mapas[f2[0]]["dados"].append(f)

proc(mapas["super"])