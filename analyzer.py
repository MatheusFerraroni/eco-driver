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

    geracoes_txt.pop(0)
    min_geral = float("Infinity")

    ys_min_geral = []
    ys_max_geral = []
    ys_min_geracao = []
    ys_mean = []
    for g in geracoes_txt:
        valores_fuel = []
        for arqs in geracoes[str(g)]:
            f = open("./output/"+arqs,"r")
            dado = ET.fromstring(f.read())
            f.close()

            valores_fuel.append(float(dado[0][0].attrib["fuel_abs"]))

        min_geral = min(min_geral, min(valores_fuel))
        ys_min_geral.append(min_geral)
        ys_max_geral.append(max(valores_fuel))
        ys_min_geracao.append(min(valores_fuel))
        ys_mean.append(mean(valores_fuel))
        # print(g, min_geral, round(max(valores_fuel),1), round(min(valores_fuel),1), round(mean(valores_fuel),1))

    # fig, ax = plt.subplots(figsize=(20,4))
    fig, ax = plt.subplots()
    # ax.set_ylim(0,300)
    # ax.patch.set_facecolor('#87d3e0')
    # ax.set_xlim(-20,1920)
    print(geracoes_txt)
    ax.plot(geracoes_txt, ys_min_geral,label="ys_min_geral")
    ax.plot(geracoes_txt, ys_max_geral,label="ys_max_geral")
    ax.plot(geracoes_txt, ys_min_geracao,label="ys_min_geracao")
    ax.plot(geracoes_txt, ys_mean,label="ys_mean")
    ax.set_title("asd")
    ax.legend()
    ax.set_xlabel('Generation')
    ax.set_ylabel('Fuel Consuption')
    plt.show()



files = os.listdir("./output")

mapas = {
    "0":{"dados":[]},
    "1":{"dados":[]},
    "2":{"dados":[]},
    "3":{"dados":[]},
    "4":{"dados":[]},
    "5":{"dados":[]},
    "6":{"dados":[]},
    "7":{"dados":[]},
    "8":{"dados":[]},
    "9":{"dados":[]},
}

for f in files:
    f2 = f.split(".")

    mapas[f2[0]]["dados"].append(f)





proc(mapas["0"])