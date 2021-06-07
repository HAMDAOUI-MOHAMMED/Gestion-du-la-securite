from django.shortcuts import render
from . import preprocessing as prs

# Create your views here.
def kdd99(request):
    traindata = prs.traindata()
    testdata = prs.testdata()
    vrftraindata = prs.verification(traindata)
    vrftestdata = prs.verification(testdata)
    shaptrdata = testdata.shape
    shaptsdata = testdata.shape
    qctrdata=prs.QualitativeColonnes(traindata)
    qctsdata=prs.QualitativeColonnes(testdata)
    imgtrdata = prs.DiagCirculaire(traindata,"training kdd-99 data")
    imgtsdata = prs.DiagCirculaire(testdata,"testing kdd-99 data")
    trsymbcl=prs.symboliquecolonne(traindata)
    tssymbcl=prs.symboliquecolonne(testdata)
    df_train_LbEn = prs.applyLabelEncoder(trsymbcl)
    df_test_LbEn = prs.applyLabelEncoder(tssymbcl)
    df_train_OneEnc = prs.applyOneHotEncoder(df_train_LbEn,trsymbcl)
    df_test_OneEnc = prs.applyOneHotEncoder(df_test_LbEn,tssymbcl)
    col_train_OneEnc = df_train_OneEnc.columns.tolist()
    col_test_OneEnc = df_test_OneEnc.columns.tolist()
    diff_list = set(col_train_OneEnc).difference(set(col_test_OneEnc))
    df_test_OneEnc_copy=prs.getcopy(df_test_OneEnc)
    df_test_OneEnc_copy =prs.equilibrage(diff_list,df_test_OneEnc_copy)
    df_train_new=prs.df_jointure(traindata,df_train_OneEnc)
    df_test_new=prs.df_jointure(testdata,df_test_OneEnc_copy)
    df_train_new_copy=prs.getcopy(df_train_new)
    df_test_new_copy=prs.getcopy(df_test_new)
    df_train_new_final=prs.suppression(df_train_new_copy)
    df_test_new_final=prs.suppression(df_test_new_copy)
    df_Attack_train_update=prs.applayAttack(prs.getcopy(df_train_new_final))
    df_Attack_test_update=prs.applayAttack(prs.getcopy(df_test_new_final))
    imgtrattack = prs.DiagAttack(df_Attack_train_update,"training attack kdd-99 data")
    imgtsattack = prs.DiagAttack(df_Attack_test_update,"testing attack kdd-99 data")

    context = {
        'traindata':traindata.head(10).to_html(classes="table table-sm table-hover text-center"),
        'testdata':testdata.head(10).to_html(classes="table table-sm table-hover text-center"),
        'vrftraindata':vrftraindata,
        'vrftestdata':vrftestdata,
        'shaptrdata':shaptrdata,
        'shaptsdata':shaptsdata,
        'qctrdata':qctrdata,
        'qctsdata':qctsdata,
        'imgtrdata':imgtrdata,
        'imgtsdata':imgtsdata,
        'trsymbcl':trsymbcl.head(10).to_html(classes="table table-sm table-hover text-center"),
        'tssymbcl':tssymbcl.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_train_LbEn':df_train_LbEn.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_test_LbEn':df_test_LbEn.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_train_OneEnc':df_train_OneEnc.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_test_OneEnc':df_test_OneEnc.head(10).to_html(classes="table table-sm table-hover text-center"),
        'dftrOneEnc':df_train_OneEnc.shape,
        'dftsOneEnc':df_test_OneEnc.shape,
        'diff_list':diff_list,
        'df_test_OneEnc_copy':df_test_OneEnc_copy.head(10).to_html(classes="table table-sm table-hover text-center"),
        'dftsOneEnc_copy':df_test_OneEnc_copy.shape,
        'df_train_new':df_train_new.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_test_new':df_test_new.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_train_new_shape':df_train_new.shape,
        'df_test_new_shape':df_test_new.shape,
        'df_train_new_final':df_train_new_final.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_test_new_final':df_test_new_final.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_train_new_final_shape':df_train_new_final.shape,
        'df_test_new_final_shape':df_test_new_final.shape,
        'df_Attack_train_update':df_Attack_train_update.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_Attack_test_update':df_Attack_test_update.head(10).to_html(classes="table table-sm table-hover text-center"),
        'df_Attack_train_update_shape':df_Attack_train_update.shape,
        'df_Attack_test_update_shape':df_Attack_test_update.shape,
        'imgtrattack':imgtrattack,
        'imgtsattack':imgtsattack,

        

    }
    return render(request, 'kdd99/kdd99.html',context)