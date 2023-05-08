#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[ ]:


# preprocessing
with open(r'C:\Users\hwx756\Downloads/Cinematographie_des_Holocaust.pickle', 'rb') as handle:
    b = pickle.load(handle)
print(len(b))

unique_cols = {'ID:', 'Produktionsjahr:', 'ODat:','O-Titel:','D-Titel:','A-Titel:', 'Produktionsland:','Pro:','ProdStabDar:', 
               'OCredits:','Länge/Dauer:', 'Regie:','UAng:',  'Kopie:', 'ZAng:', 'Video:',     
               'Auff/TV:', 'Anm:', 'Abstract:',  'Inhalt:', 'Gattung:',   'Format:',  'Filmo:','Biblio:','Sonstiges:'}
df = pd.DataFrame(columns=unique_cols)
for dct in b:
    df = df.append(dct,ignore_index=True)

df.drop_duplicates(subset=['ID:'],inplace=True)
len(df)

df1.to_csv(r'C:\Users\hwx756\Downloads/Cinematographie_des_Holocaust_standard_engl.tsv', sep='\t', index=False)


# In[ ]:


def standardise_dates(cell):
    out = str(cell).split('-')[0] # return the first in any potential date range (usually series are counted by start date)
    if "??" in out or out.isalpha():
        return 0 # for results like '19??' or "DE" which are useless
    if "/" in out:
        return int(out.split('/')[0])
    else:
        out = out.replace(' ', '').replace('(?)', '')
        if len(out) == 4:
            return int(out.replace('?', '0')) # replace questionmarks with 0
        else: return int(out.replace('?', '')[:4])
        
        
def standardise_countrycodes(cell):
    if not isinstance(cell, str) or cell.isnumeric():
        return 'unknown'
    else:
        val = re.sub('P9 /|\[P9\]|/ P9|[ ]', '', cell).strip()
        if '?' in val and val != 'IL?' or val == '':
            return 'unknown'
        else: 
            val = val.replace('?', '')
            val = '/'.join(sorted(val.split('/'))).strip() # split and sort alphabetically, so we have consistent counting
            return val

def standardise_length_duration(cell):
    l = None
    d = None
    if isinstance(cell, str):
        vals = cell.split('/')
        for item in vals:
            if 'm' in item:
                l = item.replace(' ', '')
            elif '\'' in item:
                d = item.replace(' ', '').replace('\'\'', '').replace('\'', ':')
                if d.endswith(':'):
                    d += '00'
    return l, d

def standardise_genre(cell):
    if not isinstance(cell, str):
        return 'unknown'
    map_dict = {'TV-Dokumentation': 'Dokumentarfilm', 'TV-Film':'Spielfilm',
       'Spielfilm / Dokumentarfilm':'unknown', 'Spielfim':'Spielfilm',
       'Filmsketch mit Live-Auftritten':'TV-Show', 'Wochenschau':'Archiv',
       'Dokumentarfilm / Kompilationsfilm': 'Dokumentarfilm',
       'Kurz-Dokumentarfilm / Filmmaterial':'Archiv',
       'Dokumentarfilm mit Spielszenen':'Dokumentarfilm', 'Video':'Archiv',
       'Dokumentarfilm / Filmmaterial':'Archiv', 'Newsreel':'Archiv',
       'Kurz-Dokumentarfilm / Amateurfilm':'Archiv',
       'Kurz-Dokumentarfilm mit Spielszenen':'Dokumentarfilm', 'TV-Spielfilm':'Spielfilm',
       'Puppen-Animationsfilm': 'Animationsfilm', 'Amateurfilm / Dokumentarfilm':'Archiv',
       'Amateurfilm / Kurz-Dokumentarfilm':'Archiv',
       'Kurz-Dokumentarfilm / home movie': "Archiv", 'TV-Spiel':'Spielfilm', 'Dokumentation':'Dokumentarfilm',
       'Amateurfilm':'Archiv', 'Dokumentarfilm / Amateurfilm':'Archiv',
       'Kurz-Dokumentarfilm /  Wochenschau':'Archiv', 'Filmmaterial':'Archiv',
       'Spielfilm / Projekt':'Spielfilm', 
       'Kurz-Dokumentarfilm / Amateurfilmmaterial':'Archiv',
       'TV-Dokumentarfilm mit Spielszenen':"Dokumentarfilm", 'Neewsreel':'Archiv', 'TV-Newsreel':'Archiv',
       'Episodenfilm':'Spielfilm', 'TV-Drama':'Spielfilm', 'Kurz-Dokumentarfilm / Episodenfilm': 'Dokumentarfilm',
       'TV- Serie':'TV-Serie', 'TV- Dokumentation': 'Dokumentarfilm', 'Dokumentarspiel': 'Dokudrama',
       'TV-Tagesschau':'Archiv', 'dokumentarfilm':'Dokumentarfilm', 'TV-Dokumentarfilm': 'Dokumentarfilm',
       'Dokumentarfilm mit Spielszenen\t\tDokumentarfilm mit Spielszenen':'Dokumentarfilm',
       'Fernsehspiel':'Spielfilm', "105'":'unknown', 'Kurz-Dokumentarfilm':'Dokumentarfilm', 
        'Kurzfilm': 'Spielfilm','Kurz-Spielfilm':'Spielfilm', 'Kurz-Animationsfilm':'Animationsfilm',
        'Experimentalfilm':'Spielfilm'}
    if cell in map_dict.keys():
        return map_dict.get(cell)
    else: return cell
df1['standardised_genre'] = df1.genre.apply(standardise_genre)
df1['standardised_genre'].unique()


# In[ ]:


# let's drop and rename columns
df1.drop(labels=['ZAng:', 'Auff/TV:' , 'UAng:'],axis=1, inplace=True)
dct = {'Filmo:': 'film_records', 'Produktionsland:':'production_country', 'O-Titel:':'original_title', 
       'Kopie:':'copy', 'Länge/Dauer:':'length/duration',
       'D-Titel:':'german_title', 'ODat:':'original_date', 'Gattung:':'genre', 'ID:': 'ID', 
       'Format:':'format','Regie:':'director',
       'A-Titel:':'other_title', 'Anm:':'notes', 'Inhalt:':'content', 'Produktionsjahr:':'date', 'Pro:':'producer',
       'ProdStabDar:' :'further_production_info', 'OCredits:':'credits', 'Sonstiges:':'other', 'Biblio:':'biblio',
       'Video:': 'video', 'Abstract:': 'abstract'}
df1.rename(columns=dct, inplace=True)
df1


# In[ ]:


df1['length'], df1['duration'] = zip(*df1['length/duration'].map(standardise_length_duration))

df1.drop(labels=['length/duration'],axis=1, inplace=True)
dct = {'length': 'physical_length_meters'}
df1.rename(columns=dct, inplace=True)

df1 = pd.read_csv(r'C:\Users\hwx756\Downloads/Cinematographie_des_Holocaust_standard_engl.tsv', sep='\t')

ar = df1.production_country.unique()
for e in ar:
    print('before ',e)
    print('after ' , re.sub('P9 /|\[P9\]|/ P9|[ ]', '', str(e)).strip(), '\n')

bars = df1.groupby('production_country').size().reset_index()
# df1.loc[(df1.production_country == bars.production_country) & df1.]

docs = df1[(df1.standardised_genre == 'Dokumentarfilm')]
len(docs)


# In[ ]:


def rep(cell):
    if isinstance(cell, str):
#         return int(re.sub(':[0-9][0-9]', '', str(cell)).replace('(Teil2)', '').replace('121oder123', '121'))
        vals = cell.split(':')[0].replace('(Teil2)', '').replace('121oder123', '121')\
                .replace('3Teile,jederTeil44', '132').replace('(ZweiVersionen)40', '40')\
                .replace('(VierTeileà60', '240').replace('30(Beitrag3);21(Beitrag4);1', '51')\
                .replace('ca.60', '')
#         print(vals)
        vals = vals.split('(')[0]
        vals = vals.split(',')[0]
        vals = vals.split('’')[0]
        if vals: return int(vals)
        else: return 0
    else: return 0
df1['duration_rounddown_min'] = df1.duration.apply(rep)


# In[ ]:





# In[ ]:


df1.to_csv(r'C:\Users\hwx756\Downloads/Cinematographie_des_Holocaust_standard_engl.tsv', sep='\t', index=False)


# In[ ]:




