import pandas as pd
import os
import EmailScraping as mailscrap

def main():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    for i in range(7, len(csv_files)):

        df = pd.read_csv(csv_files[i])
        list = df['Source url'].to_list()

        with open('urls.txt','w', encoding='utf-8') as file:
            file.write('\n'.join(list))

        mailscrap.scrap(csv_files[i][:-4])

if __name__=='__main__':
    main()
