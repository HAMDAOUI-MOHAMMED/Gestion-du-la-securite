# import pandas as pd
# import seaborn as sns #pallete des coleurs
import matplotlib.pyplot as plt #affichage des figure
from pandas import read_csv, crosstab,DataFrame

import os
workpath = os.path.dirname(os.path.abspath(__file__))


columns = (['duration'
,'protocol_type'
,'service'
,'flag'
,'src_bytes'
,'dst_bytes'
,'land'
,'wrong_fragment'
,'urgent'
,'hot'
,'num_failed_logins'
,'logged_in'
,'num_compromised'
,'root_shell'
,'su_attempted'
,'num_root'
,'num_file_creations'
,'num_shells'
,'num_access_files'
,'num_outbound_cmds'
,'is_host_login'
,'is_guest_login'
,'count'
,'srv_count'
,'serror_rate'
,'srv_serror_rate'
,'rerror_rate'
,'srv_rerror_rate'
,'same_srv_rate'
,'diff_srv_rate'
,'srv_diff_host_rate'
,'dst_host_count'
,'dst_host_srv_count'
,'dst_host_same_srv_rate'
,'dst_host_diff_srv_rate'
,'dst_host_same_src_port_rate'
,'dst_host_srv_diff_host_rate'
,'dst_host_serror_rate'
,'dst_host_srv_serror_rate'
,'dst_host_rerror_rate'
,'dst_host_srv_rerror_rate'
,'attack'
,'level'])


def traindata():
    file = open(os.path.join(workpath, "data/KDDTrain+.csv"), 'rb')
    return read_csv(file,header=None, names = columns)


def testdata():
    file = open(os.path.join(workpath, "data/KDDTest+.csv"), 'rb')
    return read_csv(file,header=None, names = columns)


def verification(df):
    d = df[df.duplicated()] # les lignes dupliquer
    Nan = df[df.isna().any(axis=1)] #les cellules null
    msg = [0]*2 
    msg[0] = 'Il y a {} lignes est repete'.format(len(d))
    msg[1] = 'Il y a {} valeurs null'.format(len(Nan))
    return msg


def QualitativeColonnes(df):
    msg=[]
    for col in df.columns:
        if df[col].dtype == 'object':
            nbCat = len(df[col].value_counts())
            msg.append('Colonne : {} a {} categories'.format(col, nbCat))

    return msg    


def DiagCirculaire(df,name):
    ax = crosstab(df.attack, df.protocol_type)
    ax.columns = [''] * len(ax.columns)
    ax.plot(kind='pie',labels=None,subplots=True,figsize=(15,10),title=['ICMP','TCP', 'UDP'])
    # plt.legend(loc='center left',labels=ax.index,bbox_to_anchor=(0.88, 0.5))
    plt.legend(loc='lower right',labels=ax.index,ncol=round(len(ax.index)/5),bbox_to_anchor=(0.88, -0.3))
    plt.figtext(.5,.8,name, fontsize=30, ha='center')

    pathimage = "assets/img/figure/"+name+".svg"
    path = os.path.join(*[workpath.replace("nslKdd",""), "static/",pathimage])
    try:
        os.remove(path)
    except OSError:
        pass
    plt.savefig(path)
    plt.clf()
    plt.close()

    return pathimage

def symboliquecolonne(df):

    Qualitative_col = ['protocol_type','service','flag']

    return df[Qualitative_col]

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
def applyLabelEncoder(df):
    return df.apply(LabelEncoder().fit_transform)

def dummyColonnesHeader(df):
    str = ['Protocol_','service_','flag_']
    protocol_type=sorted(df.protocol_type.unique())
    protocol_list=[str[0] + x for x in protocol_type]
    service=sorted(df.service.unique())
    service_list=[str[1] + x for x in service]
    flag=sorted(df.flag.unique())
    flag_list=[str[2] + x for x in flag]
    return protocol_list + service_list + flag_list


def applyOneHotEncoder(df_LbEn,df_symb):
    enc = OneHotEncoder()
    data_transform = enc.fit_transform(df_LbEn)
    return DataFrame(data_transform.toarray(),columns=dummyColonnesHeader(df_symb))

def equilibrage(diff_list,df):
    for col in diff_list:
        df[col] = 0
    return df

def getcopy(df):
    return df.copy()

def df_jointure(df_old,df_new):
    return df_old.join(df_new)

def suppression(df):
    df.drop('protocol_type', axis=1, inplace=True)
    df.drop('service', axis=1, inplace=True)
    df.drop('flag', axis=1, inplace=True)
    return df

def Attacks(attack):
    Dos = ['neptune','land','pod','smurf','teardrop','back','worm','udpstorm','processtable','apache2']
    Probe = ['ipsweep','satan','nmap','portsweep','mscan','saint']
    R2l = ['ftp_write','guess_passwd','imap','multihop','phf','spy','warezclient','warezmaster','snmpguess','named','xlock','xsnoop','snmpgetattack','httptunnel','sendmail']
    U2r = ['buffer_overflow','loadmodule','perl','rootkit','ps','xterm','sqlattack']
    if attack in Dos:
        atk = 1
    elif attack in Probe:
        atk = 2
    elif attack in R2l:
        atk = 3
    elif attack in U2r:
        atk = 4
    else:
        atk = 0
    return atk

def applayAttack(df):
    df_attack_types = df.attack.apply(Attacks)
    df['attack'] = df_attack_types
    return df


def DiagAttack(df, name):
    ax = df.attack.value_counts()
    ax.plot(kind='pie',labels=None,subplots=True,figsize=(5,8))
    # plt.legend(loc='center left',labels=['Normal','DOS','Probe','R2L','U2R'],bbox_to_anchor=(0.88, 0.5))
    plt.legend(loc='lower right',labels=['Normal','DOS','Probe','R2L','U2R'],ncol=3,bbox_to_anchor=(0.93, -0.1))
    plt.figtext(.5,.8,name,fontsize=10, ha='center')
    pathimage = "assets/img/figure/"+name+".svg"
    path = os.path.join(*[workpath.replace("nslKdd",""), "static/",pathimage])
    try:
        os.remove(path)
    except OSError:
        pass
    plt.savefig(path)
    plt.clf()
    plt.close()


    return pathimage