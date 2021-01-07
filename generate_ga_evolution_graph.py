import json






def main():
    f = open("./results/20_200_True_0.1.json")
    dat = f.read()
    f.close()

    dat = json.loads(dat)
    
    for i in range(len(dat['historic'])):
        gen = dat['historic'][i]
        print(i, gen['max'])



if __name__ == '__main__':
    main()