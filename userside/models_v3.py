# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class TblAbondoh(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    datestat = models.DateField(null=True, db_column='DATESTAT', blank=True) # Field name made lowercase.
    doh = models.FloatField(null=True, db_column='DOH', blank=True) # Field name made lowercase.
    users = models.IntegerField(null=True, db_column='USERS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_abondoh'

class TblActivtable(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    datestat = models.DateTimeField(null=True, db_column='DATESTAT', blank=True) # Field name made lowercase.
    count = models.IntegerField(null=True, db_column='COUNT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_activtable'

class TblAdrCity(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    districtcode = models.IntegerField(null=True, db_column='DISTRICTCODE', blank=True) # Field name made lowercase.
    provincecode = models.IntegerField(null=True, db_column='PROVINCECODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_adr_city'

class TblAdrDistrict(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    provincecode = models.IntegerField(null=True, db_column='PROVINCECODE', blank=True) # Field name made lowercase.
    maincity = models.IntegerField(null=True, db_column='MAINCITY', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_adr_district'

class TblAdrProvince(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    maincity = models.IntegerField(null=True, db_column='MAINCITY', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_adr_province'

class TblAttach(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    kat = models.CharField(max_length=60, db_column='KAT', blank=True) # Field name made lowercase.
    code1 = models.IntegerField(null=True, db_column='CODE1', blank=True) # Field name made lowercase.
    code2 = models.IntegerField(null=True, db_column='CODE2', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=600, db_column='FILEPATH', blank=True) # Field name made lowercase.
    realname = models.CharField(max_length=600, db_column='REALNAME', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=600, db_column='OPIS', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_attach'

class TblAttr(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    attrcode = models.IntegerField(null=True, db_column='ATTRCODE', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    valuestr = models.CharField(max_length=765, db_column='VALUESTR', blank=True) # Field name made lowercase.
    valueint = models.IntegerField(null=True, db_column='VALUEINT', blank=True) # Field name made lowercase.
    valuedate = models.DateField(null=True, db_column='VALUEDATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_attr'

class TblBase(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    codeti = models.CharField(max_length=108, db_column='CODETI', blank=True) # Field name made lowercase.
    groupn = models.CharField(max_length=114, db_column='GROUPN', blank=True) # Field name made lowercase.
    groupr = models.IntegerField(null=True, db_column='GROUPR', blank=True) # Field name made lowercase.
    isreg = models.IntegerField(null=True, db_column='ISREG', blank=True) # Field name made lowercase.
    logname = models.CharField(max_length=60, db_column='LOGNAME', blank=True) # Field name made lowercase.
    dognumber = models.CharField(max_length=60, db_column='DOGNUMBER', blank=True) # Field name made lowercase.
    datedog2 = models.CharField(max_length=30, db_column='DATEDOG2', blank=True) # Field name made lowercase.
    fio = models.CharField(max_length=765, db_column='FIO', blank=True) # Field name made lowercase.
    pass_field = models.CharField(max_length=150, db_column='PASS', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    housec = models.IntegerField(null=True, db_column='HOUSEC', blank=True) # Field name made lowercase.
    podezd = models.IntegerField(null=True, db_column='PODEZD', blank=True) # Field name made lowercase.
    floor = models.IntegerField(null=True, db_column='FLOOR', blank=True) # Field name made lowercase.
    apart = models.IntegerField(null=True, db_column='APART', blank=True) # Field name made lowercase.
    apart_b = models.CharField(max_length=96, db_column='APART_B', default='', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=300, db_column='EMAIL', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=765, db_column='TEL', blank=True) # Field name made lowercase.
    telmob = models.CharField(max_length=765, db_column='TELMOB', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    dop2 = models.TextField(db_column='DOP2', blank=True) # Field name made lowercase.
    scet = models.FloatField(null=True, db_column='SCET', blank=True) # Field name made lowercase.
    balans = models.FloatField(null=True, db_column='BALANS', blank=True) # Field name made lowercase.
    kredit = models.FloatField(null=True, db_column='KREDIT', blank=True) # Field name made lowercase.
    inkredit = models.IntegerField(null=True, db_column='INKREDIT', blank=True) # Field name made lowercase.
    skidka = models.IntegerField(null=True, db_column='SKIDKA', blank=True) # Field name made lowercase.
    dateplus = models.DateField(null=True, db_column='DATEPLUS', auto_now_add=True, blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', auto_now_add=True, blank=True) # Field name made lowercase.
    lastping = models.DateTimeField(null=True, db_column='LASTPING', auto_now_add=True, blank=True) # Field name made lowercase.
    workstatus = models.IntegerField(null=True, db_column='WORKSTATUS', default=2, blank=True) # Field name made lowercase.
    rxtraf = models.CharField(max_length=45, db_column='RXTRAF', blank=True) # Field name made lowercase.
    txtraf = models.CharField(max_length=45, db_column='TXTRAF', blank=True) # Field name made lowercase.
    dateinnet = models.DateField(null=True, db_column='DATEINNET', blank=True) # Field name made lowercase.
    lastlogontime = models.DateTimeField(null=True, db_column='LASTLOGONTIME', blank=True) # Field name made lowercase.
    lastlogofftime = models.DateTimeField(null=True, db_column='LASTLOGOFFTIME', blank=True) # Field name made lowercase.
    logonhisip = models.BigIntegerField(null=True, db_column='LOGONHISIP', blank=True) # Field name made lowercase.
    agent_ver = models.CharField(max_length=33, db_column='AGENT_VER', blank=True) # Field name made lowercase.
    agent_lastvisit = models.DateTimeField(null=True, db_column='AGENT_LASTVISIT', blank=True) # Field name made lowercase.
    agent_data = models.TextField(db_column='AGENT_DATA', blank=True) # Field name made lowercase.
    userlang = models.CharField(max_length=33, db_column='USERLANG', blank=True) # Field name made lowercase.
    isvip = models.IntegerField(null=True, db_column='ISVIP', blank=True) # Field name made lowercase.
    lastvisit = models.DateTimeField(null=True, db_column='LASTVISIT', blank=True) # Field name made lowercase.
    logonip = models.FloatField(null=True, db_column='LOGONIP', blank=True) # Field name made lowercase.
    dateakciya = models.DateField(null=True, db_column='DATEAKCIYA', blank=True) # Field name made lowercase.
    metr = models.IntegerField(null=True, db_column='METR', default=0, blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', auto_now_add=True, blank=True) # Field name made lowercase.
    datecorrect = models.DateTimeField(null=True, db_column='DATECORRECT', auto_now_add=True, blank=True) # Field name made lowercase.
    housecode = models.CharField(max_length=30, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    billcode = models.IntegerField(null=True, db_column='BILLCODE', blank=True) # Field name made lowercase.
    notinbilling = models.IntegerField(null=True, db_column='NOTINBILLING', blank=True) # Field name made lowercase.
    datepaid = models.DateField(null=True, db_column='DATEPAID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base'

class TblBaseBilling(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    billcode = models.IntegerField(null=True, db_column='BILLCODE', blank=True) # Field name made lowercase.
    workstatus = models.IntegerField(null=True, db_column='WORKSTATUS', blank=True) # Field name made lowercase.
    datepaid = models.DateField(null=True, db_column='DATEPAID', blank=True) # Field name made lowercase.
    groupn = models.CharField(max_length=114, db_column='GROUPN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base_billing'

class TblBaseDopdata(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datacode = models.IntegerField(null=True, db_column='DATACODE', blank=True) # Field name made lowercase.
    valuestr = models.CharField(max_length=765, db_column='VALUESTR', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base_dopdata'

class TblBaseMark(models.Model):
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    markcode = models.IntegerField(null=True, db_column='MARKCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base_mark'

class TblBaseOld(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    fio = models.CharField(max_length=300, db_column='FIO', blank=True) # Field name made lowercase.
    housec = models.IntegerField(null=True, db_column='HOUSEC', blank=True) # Field name made lowercase.
    apart = models.IntegerField(null=True, db_column='APART', blank=True) # Field name made lowercase.
    apart_b = models.CharField(max_length=15, db_column='APART_B', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    balans = models.FloatField(null=True, db_column='BALANS', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    dateinnet = models.DateField(null=True, db_column='DATEINNET', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=765, db_column='TEL', blank=True) # Field name made lowercase.
    telmob = models.CharField(max_length=765, db_column='TELMOB', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base_old'

class TblBasesist(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=600, db_column='DOP', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_basesist'

class TblBilhist(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    oper = models.IntegerField(null=True, db_column='OPER', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    doing = models.CharField(max_length=765, db_column='DOING', blank=True) # Field name made lowercase.
    pko = models.IntegerField(null=True, db_column='PKO', blank=True) # Field name made lowercase.
    oldbalans = models.FloatField(null=True, db_column='OLDBALANS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_bilhist'

class TblBlagPaid(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    blagcode = models.IntegerField(null=True, db_column='BLAGCODE', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_blag_paid'

class TblBuhOper(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    scet1 = models.BigIntegerField(null=True, db_column='SCET1', blank=True) # Field name made lowercase.
    scet2 = models.BigIntegerField(null=True, db_column='SCET2', blank=True) # Field name made lowercase.
    tovarcode = models.IntegerField(null=True, db_column='TOVARCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    kolvo = models.FloatField(null=True, db_column='KOLVO', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    operaprove = models.IntegerField(null=True, db_column='OPERAPROVE', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=765, db_column='DOP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_buh_oper'

class TblBuhOst(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    scet = models.BigIntegerField(null=True, db_column='SCET', blank=True) # Field name made lowercase.
    tovarcode = models.IntegerField(null=True, db_column='TOVARCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    kolvo = models.FloatField(null=True, db_column='KOLVO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_buh_ost'

class TblBuhPromise(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datestop = models.DateTimeField(null=True, db_column='DATESTOP', blank=True) # Field name made lowercase.
    isact = models.IntegerField(null=True, db_column='ISACT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_buh_promise'

class TblCards(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    series = models.IntegerField(null=True, db_column='SERIES', blank=True) # Field name made lowercase.
    cardno = models.IntegerField(null=True, db_column='CARDNO', blank=True) # Field name made lowercase.
    pin = models.CharField(max_length=765, db_column='PIN', blank=True) # Field name made lowercase.
    nominal = models.IntegerField(null=True, db_column='NOMINAL', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    dateact = models.DateTimeField(null=True, db_column='DATEACT', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_cards'

class TblCeleb(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    datestart = models.DateField(null=True, db_column='DATESTART', blank=True) # Field name made lowercase.
    datestop = models.DateField(null=True, db_column='DATESTOP', blank=True) # Field name made lowercase.
    active = models.IntegerField(null=True, db_column='ACTIVE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_celeb'

class TblConf(models.Model):
    param = models.CharField(max_length=150, db_column='PARAM', blank=True) # Field name made lowercase.
    valuestr = models.CharField(max_length=765, db_column='VALUESTR', blank=True) # Field name made lowercase.
    valuedate = models.DateTimeField(null=True, db_column='VALUEDATE', blank=True) # Field name made lowercase.
    valueint = models.IntegerField(null=True, db_column='VALUEINT', blank=True) # Field name made lowercase.
    valuememo = models.TextField(db_column='VALUEMEMO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf'

class TblConfAttr(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    katcode = models.IntegerField(null=True, db_column='KATCODE', blank=True) # Field name made lowercase.
    pos = models.IntegerField(null=True, db_column='POS', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    isactive = models.IntegerField(null=True, db_column='ISACTIVE', blank=True) # Field name made lowercase.
    fsize = models.IntegerField(null=True, db_column='FSIZE', blank=True) # Field name made lowercase.
    fmaxsize = models.IntegerField(null=True, db_column='FMAXSIZE', blank=True) # Field name made lowercase.
    ftyper = models.IntegerField(null=True, db_column='FTYPER', blank=True) # Field name made lowercase.
    subkatcode = models.IntegerField(null=True, db_column='SUBKATCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_attr'

class TblConfBasedopdata(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    lenfield = models.IntegerField(null=True, db_column='LENFIELD', blank=True) # Field name made lowercase.
    maxlenfield = models.IntegerField(null=True, db_column='MAXLENFIELD', blank=True) # Field name made lowercase.
    position = models.IntegerField(null=True, db_column='POSITION', blank=True) # Field name made lowercase.
    inuser = models.IntegerField(null=True, db_column='INUSER', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_basedopdata'

class TblConfBilling(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    billcode = models.IntegerField(null=True, db_column='BILLCODE', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    istraf = models.IntegerField(null=True, db_column='ISTRAF', blank=True) # Field name made lowercase.
    isupdfio = models.IntegerField(null=True, db_column='ISUPDFIO', blank=True) # Field name made lowercase.
    isupdtel = models.IntegerField(null=True, db_column='ISUPDTEL', blank=True) # Field name made lowercase.
    isupdadr = models.IntegerField(null=True, db_column='ISUPDADR', blank=True) # Field name made lowercase.
    isupdmac = models.IntegerField(null=True, db_column='ISUPDMAC', blank=True) # Field name made lowercase.
    ismt = models.IntegerField(null=True, db_column='ISMT', blank=True) # Field name made lowercase.
    lastupdate = models.DateTimeField(null=True, db_column='LASTUPDATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_billing'

class TblConfBillingRegion(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    billcode = models.IntegerField(null=True, db_column='BILLCODE', blank=True) # Field name made lowercase.
    regioncode = models.IntegerField(null=True, db_column='REGIONCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_billing_region'

class TblConfBlag(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    pict = models.CharField(max_length=765, db_column='PICT', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    inmain = models.IntegerField(null=True, db_column='INMAIN', blank=True) # Field name made lowercase.
    isactive = models.IntegerField(null=True, db_column='ISACTIVE', blank=True) # Field name made lowercase.
    ishideusers = models.IntegerField(null=True, db_column='ISHIDEUSERS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_blag'

class TblConfBuhSs(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    isbuh = models.IntegerField(null=True, db_column='ISBUH', blank=True) # Field name made lowercase.
    issklad = models.IntegerField(null=True, db_column='ISSKLAD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_buh_ss'

class TblConfContr(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    isbuh = models.IntegerField(null=True, db_column='ISBUH', blank=True) # Field name made lowercase.
    issklad = models.IntegerField(null=True, db_column='ISSKLAD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_contr'

class TblConfCronTyper(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    param1 = models.CharField(max_length=765, db_column='PARAM1', blank=True) # Field name made lowercase.
    param2 = models.CharField(max_length=765, db_column='PARAM2', blank=True) # Field name made lowercase.
    param3 = models.CharField(max_length=765, db_column='PARAM3', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_cron_typer'

class TblConfDoppaid(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    isenabled = models.IntegerField(null=True, db_column='ISENABLED', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_doppaid'

class TblConfEquip(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    firma = models.CharField(max_length=765, db_column='FIRMA', blank=True) # Field name made lowercase.
    model = models.CharField(max_length=765, db_column='MODEL', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    fn = models.CharField(max_length=765, db_column='FN', blank=True) # Field name made lowercase.
    param1 = models.IntegerField(null=True, db_column='PARAM1', blank=True) # Field name made lowercase.
    param2 = models.IntegerField(null=True, db_column='PARAM2', blank=True) # Field name made lowercase.
    oid_reset = models.CharField(max_length=765, db_column='OID_RESET', blank=True) # Field name made lowercase.
    oid_reset_2 = models.IntegerField(null=True, db_column='OID_RESET_2', blank=True) # Field name made lowercase.
    fdpcommand = models.IntegerField(null=True, db_column='FDPCOMMAND', blank=True) # Field name made lowercase.
    oid_proshivka = models.CharField(max_length=765, db_column='OID_PROSHIVKA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_equip'

class TblConfGroupZ(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    groupcode1 = models.CharField(max_length=765, db_column='GROUPCODE1', blank=True) # Field name made lowercase.
    groupcode2 = models.CharField(max_length=765, db_column='GROUPCODE2', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_group_z'

class TblConfJournal(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    timedo = models.FloatField(null=True, db_column='TIMEDO', blank=True) # Field name made lowercase.
    color_fon = models.CharField(max_length=18, db_column='COLOR_FON', blank=True) # Field name made lowercase.
    color_text = models.CharField(max_length=18, db_column='COLOR_TEXT', blank=True) # Field name made lowercase.
    color_link = models.CharField(max_length=18, db_column='COLOR_LINK', blank=True) # Field name made lowercase.
    pict = models.CharField(max_length=765, db_column='PICT', blank=True) # Field name made lowercase.
    deadline = models.IntegerField(null=True, db_column='DEADLINE', blank=True) # Field name made lowercase.
    deadline_info = models.IntegerField(null=True, db_column='DEADLINE_INFO', blank=True) # Field name made lowercase.
    maingroup = models.IntegerField(null=True, db_column='MAINGROUP', blank=True) # Field name made lowercase.
    ispricemult = models.IntegerField(null=True, db_column='ISPRICEMULT', blank=True) # Field name made lowercase.
    ispriceproizv = models.IntegerField(null=True, db_column='ISPRICEPROIZV', blank=True) # Field name made lowercase.
    r_read = models.TextField(db_column='R_READ', blank=True) # Field name made lowercase.
    r_do = models.TextField(db_column='R_DO', blank=True) # Field name made lowercase.
    r_write = models.TextField(db_column='R_WRITE', blank=True) # Field name made lowercase.
    sel_list = models.CharField(max_length=765, db_column='SEL_LIST', blank=True) # Field name made lowercase.
    def_pers = models.TextField(db_column='DEF_PERS', blank=True) # Field name made lowercase.
    def_loop = models.TextField(db_column='DEF_LOOP', blank=True) # Field name made lowercase.
    doc_sh = models.IntegerField(null=True, db_column='DOC_SH', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_journal'

class TblConfJournalAnswer(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_journal_answer'

class TblConfJournalGroup(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_journal_group'

class TblConfJournalStatus(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    pict = models.CharField(max_length=765, db_column='PICT', blank=True) # Field name made lowercase.
    isact = models.IntegerField(null=True, db_column='ISACT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_journal_status'

class TblConfLoyalityGroup(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    groupcode = models.CharField(max_length=765, db_column='GROUPCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_loyality_group'

class TblConfLoyalityNet(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    startdate = models.IntegerField(null=True, db_column='STARTDATE', blank=True) # Field name made lowercase.
    finishdate = models.IntegerField(null=True, db_column='FINISHDATE', blank=True) # Field name made lowercase.
    skidka = models.IntegerField(null=True, db_column='SKIDKA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_loyality_net'

class TblConfMac(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    mac = models.CharField(max_length=18, db_column='MAC', blank=True) # Field name made lowercase.
    proizv = models.CharField(max_length=765, db_column='PROIZV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_mac'

class TblConfMark(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    pict = models.CharField(max_length=765, db_column='PICT', blank=True) # Field name made lowercase.
    color = models.CharField(max_length=18, db_column='COLOR', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_mark'

class TblConfOpticaCol(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    colnazv = models.CharField(max_length=765, db_column='COLNAZV', blank=True) # Field name made lowercase.
    colcol = models.CharField(max_length=765, db_column='COLCOL', blank=True) # Field name made lowercase.
    coltype = models.IntegerField(null=True, db_column='COLTYPE', blank=True) # Field name made lowercase.
    markcol = models.IntegerField(null=True, db_column='MARKCOL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_optica_col'

class TblConfRealip(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    userip1 = models.FloatField(null=True, db_column='USERIP1', blank=True) # Field name made lowercase.
    userip2 = models.FloatField(null=True, db_column='USERIP2', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_realip'

class TblConfRightsKat(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    position = models.IntegerField(null=True, db_column='POSITION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_rights_kat'

class TblConfRightsProfile(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_rights_profile'

class TblConfRightsProfileInc(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    profilecode = models.IntegerField(null=True, db_column='PROFILECODE', blank=True) # Field name made lowercase.
    rightcode = models.IntegerField(null=True, db_column='RIGHTCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_rights_profile_inc'

class TblConfRightsSubkat(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    katcode = models.IntegerField(null=True, db_column='KATCODE', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_rights_subkat'

class TblConfRouter(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    routerip = models.CharField(max_length=45, db_column='ROUTERIP', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    rport = models.IntegerField(null=True, db_column='RPORT', blank=True) # Field name made lowercase.
    ruser = models.CharField(max_length=765, db_column='RUSER', blank=True) # Field name made lowercase.
    rpass = models.CharField(max_length=765, db_column='RPASS', blank=True) # Field name made lowercase.
    statusconn = models.IntegerField(null=True, db_column='STATUSCONN', blank=True) # Field name made lowercase.
    ispiring = models.IntegerField(null=True, db_column='ISPIRING', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_router'

class TblConfRouterDiapazon(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    routercode = models.IntegerField(null=True, db_column='ROUTERCODE', blank=True) # Field name made lowercase.
    userip1 = models.FloatField(null=True, db_column='USERIP1', blank=True) # Field name made lowercase.
    userip2 = models.FloatField(null=True, db_column='USERIP2', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    outint = models.CharField(max_length=765, db_column='OUTINT', blank=True) # Field name made lowercase.
    inint = models.CharField(max_length=765, db_column='ININT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_router_diapazon'

class TblConfRouterGroup(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    routercode = models.IntegerField(null=True, db_column='ROUTERCODE', blank=True) # Field name made lowercase.
    groupcode = models.CharField(max_length=114, db_column='GROUPCODE', blank=True) # Field name made lowercase.
    userip = models.CharField(max_length=45, db_column='USERIP', blank=True) # Field name made lowercase.
    whiteint = models.CharField(max_length=765, db_column='WHITEINT', blank=True) # Field name made lowercase.
    grayint = models.CharField(max_length=765, db_column='GRAYINT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_router_group'

class TblConfShtraf(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_shtraf'

class TblConfSwitchPass(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    basecode = models.IntegerField(null=True, db_column='BASECODE', blank=True) # Field name made lowercase.
    com_login = models.CharField(max_length=765, db_column='COM_LOGIN', blank=True) # Field name made lowercase.
    com_pass = models.CharField(max_length=765, db_column='COM_PASS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_switch_pass'

class TblConfTt(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_tt'

class TblConfTurbo(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    hourtime = models.IntegerField(null=True, db_column='HOURTIME', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    price = models.FloatField(null=True, db_column='PRICE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_turbo'

class TblConfVols(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    proizv = models.CharField(max_length=765, db_column='PROIZV', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    kn = models.IntegerField(null=True, db_column='KN', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    portcolor = models.TextField(db_column='PORTCOLOR', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_vols'

class TblConfZvit(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    katcode = models.IntegerField(null=True, db_column='KATCODE', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    param = models.TextField(db_column='PARAM', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_conf_zvit'

class TblCoord(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    mapcode = models.IntegerField(null=True, db_column='MAPCODE', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    coord = models.TextField(db_column='COORD', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_coord'

class TblCron(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    st_day = models.CharField(max_length=150, db_column='ST_DAY', blank=True) # Field name made lowercase.
    st_hour = models.CharField(max_length=150, db_column='ST_HOUR', blank=True) # Field name made lowercase.
    st_minute = models.CharField(max_length=150, db_column='ST_MINUTE', blank=True) # Field name made lowercase.
    typercode = models.IntegerField(null=True, db_column='TYPERCODE', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    lastuse = models.DateTimeField(null=True, db_column='LASTUSE', blank=True) # Field name made lowercase.
    param1 = models.CharField(max_length=765, db_column='PARAM1', blank=True) # Field name made lowercase.
    param2 = models.CharField(max_length=765, db_column='PARAM2', blank=True) # Field name made lowercase.
    iswork = models.IntegerField(null=True, db_column='ISWORK', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    lastdeliv = models.TextField(db_column='LASTDELIV', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'tbl_cron'

class TblCrossPersRegion(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    regioncode = models.IntegerField(null=True, db_column='REGIONCODE', blank=True) # Field name made lowercase.
    ismain = models.IntegerField(null=True, db_column='ISMAIN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_cross_pers_region'

class TblDocs(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    isenabled = models.IntegerField(null=True, db_column='ISENABLED', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_docs'

class TblDoppaid(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    paidcode = models.IntegerField(null=True, db_column='PAIDCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_doppaid'

class TblGlobalPort(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    equipcode = models.IntegerField(null=True, db_column='EQUIPCODE', blank=True) # Field name made lowercase.
    storona = models.IntegerField(null=True, db_column='STORONA', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    typer2 = models.IntegerField(null=True, db_column='TYPER2', blank=True) # Field name made lowercase.
    equipcode2 = models.IntegerField(null=True, db_column='EQUIPCODE2', blank=True) # Field name made lowercase.
    storona2 = models.IntegerField(null=True, db_column='STORONA2', blank=True) # Field name made lowercase.
    port2 = models.IntegerField(null=True, db_column='PORT2', blank=True) # Field name made lowercase.
    dopdata = models.CharField(max_length=765, db_column='DOPDATA', blank=True) # Field name made lowercase.
    x1 = models.IntegerField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.IntegerField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    coord = models.CharField(max_length=765, db_column='COORD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_global_port'

class TblGroup(models.Model):
    code = models.CharField(max_length=114, primary_key=True, db_column='CODE', blank=True) # Field name made lowercase.
    groupname = models.CharField(max_length=150, db_column='GROUPNAME',default=0, blank=True) # Field name made lowercase.
    price = models.FloatField(null=True, db_column='PRICE',default=0, blank=True) # Field name made lowercase.
    trafex = models.IntegerField(null=True, db_column='TRAFEX', default=0, blank=True) # Field name made lowercase.
    users = models.IntegerField(null=True, db_column='USERS', default=0, blank=True) # Field name made lowercase.
    trafbuh = models.IntegerField(null=True, db_column='TRAFBUH', default=0, blank=True) # Field name made lowercase.
    abon = models.FloatField(null=True, db_column='ABON', default=0, blank=True) # Field name made lowercase.
    abonday = models.IntegerField(null=True, db_column='ABONDAY', blank=True) # Field name made lowercase.
    trafrx1 = models.CharField(max_length=150, db_column='TRAFRX1', blank=True) # Field name made lowercase.
    traftx1 = models.CharField(max_length=150, db_column='TRAFTX1', blank=True) # Field name made lowercase.
    trafrx2 = models.CharField(max_length=150, db_column='TRAFRX2', blank=True) # Field name made lowercase.
    traftx2 = models.CharField(max_length=150, db_column='TRAFTX2', blank=True) # Field name made lowercase.
    rxkbps = models.CharField(max_length=150, db_column='RXKBPS', blank=True) # Field name made lowercase.
    txkbps = models.CharField(max_length=150, db_column='TXKBPS', blank=True) # Field name made lowercase.
    foruser = models.IntegerField(null=True, db_column='FORUSER', blank=True) # Field name made lowercase.
    rulewhite = models.CharField(max_length=765, db_column='RULEWHITE', blank=True) # Field name made lowercase.
    rulegray = models.CharField(max_length=765, db_column='RULEGRAY', blank=True) # Field name made lowercase.
    hidename = models.CharField(max_length=765, db_column='HIDENAME', blank=True) # Field name made lowercase.
    priznak = models.IntegerField(null=True, db_column='PRIZNAK', default=0, blank=True) # Field name made lowercase.
    akciya_day = models.IntegerField(null=True, db_column='AKCIYA_DAY', default=0, blank=True) # Field name made lowercase.
    akciya_many = models.IntegerField(null=True, db_column='AKCIYA_MANY', default=0, blank=True) # Field name made lowercase.
    notsms = models.IntegerField(null=True, db_column='NOTSMS', default=1, blank=True) # Field name made lowercase.
    isturbo = models.IntegerField(null=True, db_column='ISTURBO', default=0, blank=True) # Field name made lowercase.
    speedtx = models.IntegerField(null=True, db_column='SPEEDTX', default=0, blank=True) # Field name made lowercase.
    speedrx = models.IntegerField(null=True, db_column='SPEEDRX', default=0, blank=True) # Field name made lowercase.
    dogroup = models.IntegerField(null=True, db_column='DOGROUP', blank=True) # Field name made lowercase.
    billcode = models.IntegerField(null=True, db_column='BILLCODE', default=1, blank=True) # Field name made lowercase.
    notinbilling = models.IntegerField(null=True, db_column='NOTINBILLING', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_group'



class TblGroza(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    switchcode = models.IntegerField(null=True, db_column='SWITCHCODE', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_groza'

class TblHouse(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    streetcode = models.IntegerField(null=True, db_column='STREETCODE', blank=True) # Field name made lowercase.
    house = models.IntegerField(null=True, db_column='HOUSE', blank=True) # Field name made lowercase.
    house_b = models.CharField(max_length=765, db_column='HOUSE_B', blank=True) # Field name made lowercase.
    map = models.IntegerField(null=True, db_column='MAP', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    podezd = models.IntegerField(null=True, db_column='PODEZD', blank=True) # Field name made lowercase.
    floor = models.IntegerField(null=True, db_column='FLOOR', blank=True) # Field name made lowercase.
    vihod = models.CharField(max_length=150, db_column='VIHOD', blank=True) # Field name made lowercase.
    kluch = models.CharField(max_length=750, db_column='KLUCH', blank=True) # Field name made lowercase.
    workdop = models.CharField(max_length=765, db_column='WORKDOP', blank=True) # Field name made lowercase.
    workdop_date = models.DateTimeField(null=True, db_column='WORKDOP_DATE', blank=True) # Field name made lowercase.
    ismark = models.IntegerField(null=True, db_column='ISMARK', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    apartc = models.IntegerField(null=True, db_column='APARTC', blank=True) # Field name made lowercase.
    notused = models.IntegerField(null=True, db_column='NOTUSED', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    customnazv = models.CharField(max_length=765, db_column='CUSTOMNAZV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_house'

class TblIp(models.Model):
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    userip = models.FloatField(primary_key=True, db_column='USERIP', blank=True) # Field name made lowercase.
    mac = models.CharField(max_length=51, db_column='MAC', blank=True) # Field name made lowercase.
    isupd = models.IntegerField(null=True, db_column='ISUPD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_ip'

class TblIpReserv(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    userip = models.FloatField(null=True, db_column='USERIP', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_ip_reserv'

class TblIpnet(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    userip = models.FloatField(null=True, db_column='USERIP', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    ipstart = models.FloatField(null=True, db_column='IPSTART', blank=True) # Field name made lowercase.
    ipstop = models.FloatField(null=True, db_column='IPSTOP', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_ipnet'

class TblJek(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    adr = models.CharField(max_length=600, db_column='ADR', blank=True) # Field name made lowercase.
    dirfio = models.CharField(max_length=600, db_column='DIRFIO', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=600, db_column='TEL', blank=True) # Field name made lowercase.
    dognumber = models.CharField(max_length=765, db_column='DOGNUMBER', blank=True) # Field name made lowercase.
    dogdata = models.DateField(null=True, db_column='DOGDATA', blank=True) # Field name made lowercase.
    rekv = models.TextField(db_column='REKV', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_jek'

class TblJekHouse(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    jekcode = models.IntegerField(null=True, db_column='JEKCODE', blank=True) # Field name made lowercase.
    housecode = models.IntegerField(null=True, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_jek_house'

class TblJekOplata(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    jekcode = models.IntegerField(null=True, db_column='JEKCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    datedo = models.DateField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    datetoopl = models.DateField(null=True, db_column='DATETOOPL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_jek_oplata'

class TblJournal(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    housecode = models.IntegerField(null=True, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    datefinish = models.DateTimeField(null=True, db_column='DATEFINISH', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    newklient = models.CharField(max_length=750, db_column='NEWKLIENT', blank=True) # Field name made lowercase.
    fromaprove = models.CharField(max_length=45, db_column='FROMAPROVE', blank=True) # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    priority = models.IntegerField(null=True, db_column='PRIORITY', blank=True) # Field name made lowercase.
    apart = models.IntegerField(null=True, db_column='APART', blank=True) # Field name made lowercase.
    parentcode = models.IntegerField(null=True, db_column='PARENTCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_journal'

class TblJournalComments(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    journalcode = models.IntegerField(null=True, db_column='JOURNALCODE', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_journal_comments'

class TblJournalDoing(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    journalcode = models.IntegerField(null=True, db_column='JOURNALCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_journal_doing'

class TblJournalStaff(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    journalcode = models.IntegerField(null=True, db_column='JOURNALCODE', blank=True) # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    ispodrazd = models.IntegerField(null=True, db_column='ISPODRAZD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_journal_staff'

class TblJournalStatus(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    journalcode = models.IntegerField(null=True, db_column='JOURNALCODE', blank=True) # Field name made lowercase.
    statuscode = models.IntegerField(null=True, db_column='STATUSCODE', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_journal_status'

class TblJur(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_jur'

class TblKeys(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    housecode = models.IntegerField(null=True, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=150, db_column='NAZV', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=750, db_column='DOP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_keys'

class TblKeyshist(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    keycode = models.IntegerField(null=True, db_column='KEYCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    keyfrom = models.IntegerField(null=True, db_column='KEYFROM', blank=True) # Field name made lowercase.
    keyto = models.IntegerField(null=True, db_column='KEYTO', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=750, db_column='DOP', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_keyshist'

class TblLinks(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    kat = models.IntegerField(null=True, db_column='KAT', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    links = models.TextField(db_column='LINKS', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    popular = models.IntegerField(null=True, db_column='POPULAR', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_links'

class TblMacHistory(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datestop = models.DateTimeField(null=True, db_column='DATESTOP', blank=True) # Field name made lowercase.
    userip = models.FloatField(null=True, db_column='USERIP', blank=True) # Field name made lowercase.
    mac = models.CharField(max_length=48, db_column='MAC', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_mac_history'

class TblMap(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    codenumber = models.IntegerField(null=True, db_column='CODENUMBER', blank=True) # Field name made lowercase.
    filepath = models.CharField(max_length=600, db_column='FILEPATH', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=600, db_column='OPIS', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    typemap = models.IntegerField(null=True, db_column='TYPEMAP', blank=True) # Field name made lowercase.
    geo_x = models.FloatField(null=True, db_column='GEO_X', blank=True) # Field name made lowercase.
    geo_y = models.FloatField(null=True, db_column='GEO_Y', blank=True) # Field name made lowercase.
    geo_scale = models.IntegerField(null=True, db_column='GEO_SCALE', blank=True) # Field name made lowercase.
    regioncode = models.IntegerField(null=True, db_column='REGIONCODE', blank=True) # Field name made lowercase.
    maptypeshow = models.IntegerField(null=True, db_column='MAPTYPESHOW', blank=True) # Field name made lowercase.
    city = models.CharField(max_length=765, db_column='CITY', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_map'

class TblMed(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    uzelcode1 = models.IntegerField(null=True, db_column='UZELCODE1', blank=True) # Field name made lowercase.
    uzelcode2 = models.IntegerField(null=True, db_column='UZELCODE2', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    medlen = models.IntegerField(null=True, db_column='MEDLEN', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_med'

class TblMedHouse(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    linecode = models.IntegerField(null=True, db_column='LINECODE', blank=True) # Field name made lowercase.
    position = models.IntegerField(null=True, db_column='POSITION', blank=True) # Field name made lowercase.
    x1 = models.FloatField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.FloatField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    mapcode = models.IntegerField(null=True, db_column='MAPCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_med_house'

class TblMedic(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    skladcode = models.IntegerField(null=True, db_column='SKLADCODE', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    x1 = models.IntegerField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.IntegerField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_medic'

class TblMemo(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    razdel = models.IntegerField(null=True, db_column='RAZDEL', blank=True) # Field name made lowercase.
    info1 = models.TextField(db_column='INFO1', blank=True) # Field name made lowercase.
    info2 = models.TextField(db_column='INFO2', blank=True) # Field name made lowercase.
    info3 = models.TextField(db_column='INFO3', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    whoadd = models.IntegerField(null=True, db_column='WHOADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_memo'

class TblMemotype(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    razdelname = models.CharField(max_length=750, db_column='RAZDELNAME', blank=True) # Field name made lowercase.
    pole1 = models.CharField(max_length=150, db_column='POLE1', blank=True) # Field name made lowercase.
    pole2 = models.CharField(max_length=150, db_column='POLE2', blank=True) # Field name made lowercase.
    pole3 = models.CharField(max_length=150, db_column='POLE3', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_memotype'

class TblOper(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    oper = models.CharField(max_length=150, db_column='OPER', blank=True) # Field name made lowercase.
    pass_field = models.CharField(max_length=150, db_column='PASS', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    fio = models.CharField(max_length=150, db_column='FIO', blank=True) # Field name made lowercase.
    dolgnost = models.CharField(max_length=150, db_column='DOLGNOST', blank=True) # Field name made lowercase.
    locked = models.IntegerField(null=True, db_column='LOCKED', blank=True) # Field name made lowercase.
    lastmsg = models.DateTimeField(null=True, db_column='LASTMSG', blank=True) # Field name made lowercase.
    profilecode = models.IntegerField(null=True, db_column='PROFILECODE', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=765, db_column='EMAIL', blank=True) # Field name made lowercase.
    issign = models.IntegerField(null=True, db_column='ISSIGN', blank=True) # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    lastip = models.TextField(db_column='LASTIP', blank=True) # Field name made lowercase.
    regioncur = models.IntegerField(null=True, db_column='REGIONCUR', blank=True) # Field name made lowercase.
    cashe = models.TextField(db_column='CASHE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_oper'

class TblOperDo(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    objectcode = models.IntegerField(null=True, db_column='OBJECTCODE', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    typerdo = models.IntegerField(null=True, db_column='TYPERDO', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_oper_do'

class TblOperIp(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    userip = models.CharField(max_length=45, db_column='USERIP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_oper_ip'

class TblOperMsg(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    answercode = models.IntegerField(null=True, db_column='ANSWERCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    operfrom = models.IntegerField(null=True, db_column='OPERFROM', blank=True) # Field name made lowercase.
    operto = models.TextField(db_column='OPERTO', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    dateview = models.TextField(db_column='DATEVIEW', blank=True) # Field name made lowercase.
    hidemsg = models.TextField(db_column='HIDEMSG', blank=True) # Field name made lowercase.
    delmsg = models.TextField(db_column='DELMSG', blank=True) # Field name made lowercase.
    isedit = models.IntegerField(null=True, db_column='ISEDIT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_oper_msg'

class TblOperRegion(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    regioncode = models.IntegerField(null=True, db_column='REGIONCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_oper_region'

class TblOperhist(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    dateoper = models.DateTimeField(null=True, db_column='DATEOPER', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    par1 = models.CharField(max_length=150, db_column='PAR1', blank=True) # Field name made lowercase.
    par2 = models.CharField(max_length=150, db_column='PAR2', blank=True) # Field name made lowercase.
    val_new = models.CharField(max_length=600, db_column='VAL_NEW', blank=True) # Field name made lowercase.
    val_old = models.CharField(max_length=600, db_column='VAL_OLD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_operhist'

class TblOperhisttype(models.Model):
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_operhisttype'

class TblOptica(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    uzelcode1 = models.IntegerField(null=True, db_column='UZELCODE1', blank=True) # Field name made lowercase.
    uzelcode2 = models.IntegerField(null=True, db_column='UZELCODE2', blank=True) # Field name made lowercase.
    opticalen = models.IntegerField(null=True, db_column='OPTICALEN', blank=True) # Field name made lowercase.
    uzel1pos = models.IntegerField(null=True, db_column='UZEL1POS', blank=True) # Field name made lowercase.
    uzel2pos = models.IntegerField(null=True, db_column='UZEL2POS', blank=True) # Field name made lowercase.
    uzel1rotat = models.IntegerField(null=True, db_column='UZEL1ROTAT', blank=True) # Field name made lowercase.
    uzel2rotat = models.IntegerField(null=True, db_column='UZEL2ROTAT', blank=True) # Field name made lowercase.
    opticalen2 = models.IntegerField(null=True, db_column='OPTICALEN2', blank=True) # Field name made lowercase.
    pg = models.TextField(db_column='PG', blank=True) # Field name made lowercase.
    cabletype = models.CharField(max_length=765, db_column='CABLETYPE', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    cablecode = models.IntegerField(null=True, db_column='CABLECODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica'

class TblOpticaBon(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    rotation = models.IntegerField(null=True, db_column='ROTATION', blank=True) # Field name made lowercase.
    x1 = models.IntegerField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.IntegerField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    pg = models.TextField(db_column='PG', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_bon'

class TblOpticaBonPort(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    boncode = models.IntegerField(null=True, db_column='BONCODE', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    devcode = models.IntegerField(null=True, db_column='DEVCODE', blank=True) # Field name made lowercase.
    devport = models.IntegerField(null=True, db_column='DEVPORT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_bon_port'

class TblOpticaHouse(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    volscode = models.IntegerField(null=True, db_column='VOLSCODE', blank=True) # Field name made lowercase.
    position = models.IntegerField(null=True, db_column='POSITION', blank=True) # Field name made lowercase.
    x1 = models.FloatField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.FloatField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    mapcode = models.IntegerField(null=True, db_column='MAPCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_house'

class TblOpticaMag(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_mag'

class TblOpticaMagInc(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    magcode = models.IntegerField(null=True, db_column='MAGCODE', blank=True) # Field name made lowercase.
    volscode = models.IntegerField(null=True, db_column='VOLSCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_mag_inc'

class TblOpticaSplit(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    port1 = models.IntegerField(null=True, db_column='PORT1', blank=True) # Field name made lowercase.
    port2 = models.IntegerField(null=True, db_column='PORT2', blank=True) # Field name made lowercase.
    rotation = models.IntegerField(null=True, db_column='ROTATION', blank=True) # Field name made lowercase.
    x1 = models.IntegerField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.IntegerField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    pg = models.TextField(db_column='PG', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_split'

class TblOpticaVol(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    opticacode = models.IntegerField(null=True, db_column='OPTICACODE', blank=True) # Field name made lowercase.
    volno = models.IntegerField(null=True, db_column='VOLNO', blank=True) # Field name made lowercase.
    volmod = models.IntegerField(null=True, db_column='VOLMOD', blank=True) # Field name made lowercase.
    volcol = models.IntegerField(null=True, db_column='VOLCOL', blank=True) # Field name made lowercase.
    position = models.IntegerField(null=True, db_column='POSITION', blank=True) # Field name made lowercase.
    zatuh = models.FloatField(null=True, db_column='ZATUH', blank=True) # Field name made lowercase.
    mark1 = models.CharField(max_length=765, db_column='MARK1', blank=True) # Field name made lowercase.
    mark2 = models.CharField(max_length=765, db_column='MARK2', blank=True) # Field name made lowercase.
    position2 = models.IntegerField(null=True, db_column='POSITION2', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_optica_vol'

class TblOsmpPaid(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    provcode = models.IntegerField(null=True, db_column='PROVCODE', blank=True) # Field name made lowercase.
    summa = models.IntegerField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    numberstr = models.CharField(max_length=765, db_column='NUMBERSTR', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    paidnumber = models.IntegerField(null=True, db_column='PAIDNUMBER', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_osmp_paid'

class TblOsmpProv(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    katnazv = models.CharField(max_length=765, db_column='KATNAZV', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    pict = models.CharField(max_length=765, db_column='PICT', blank=True) # Field name made lowercase.
    osmpcode = models.IntegerField(null=True, db_column='OSMPCODE', blank=True) # Field name made lowercase.
    valuelen = models.IntegerField(null=True, db_column='VALUELEN', blank=True) # Field name made lowercase.
    valueopis = models.CharField(max_length=765, db_column='VALUEOPIS', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    minpay = models.IntegerField(null=True, db_column='MINPAY', blank=True) # Field name made lowercase.
    maxpay = models.IntegerField(null=True, db_column='MAXPAY', blank=True) # Field name made lowercase.
    kommin = models.IntegerField(null=True, db_column='KOMMIN', blank=True) # Field name made lowercase.
    komproc = models.IntegerField(null=True, db_column='KOMPROC', blank=True) # Field name made lowercase.
    isactive = models.IntegerField(null=True, db_column='ISACTIVE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_osmp_prov'

class TblOtkl(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    whoadd = models.IntegerField(null=True, db_column='WHOADD', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    dateotkl = models.DateTimeField(null=True, db_column='DATEOTKL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_otkl'

class TblPelengLog(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    pelengcode = models.IntegerField(null=True, db_column='PELENGCODE', blank=True) # Field name made lowercase.
    datestart = models.DateTimeField(null=True, db_column='DATESTART', blank=True) # Field name made lowercase.
    devcode = models.IntegerField(null=True, db_column='DEVCODE', blank=True) # Field name made lowercase.
    isdo = models.IntegerField(null=True, db_column='ISDO', blank=True) # Field name made lowercase.
    allmac = models.IntegerField(null=True, db_column='ALLMAC', blank=True) # Field name made lowercase.
    unkmac = models.IntegerField(null=True, db_column='UNKMAC', blank=True) # Field name made lowercase.
    devtype = models.IntegerField(null=True, db_column='DEVTYPE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_peleng_log'

class TblPelengMac(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    devcode = models.IntegerField(null=True, db_column='DEVCODE', blank=True) # Field name made lowercase.
    devstack = models.IntegerField(null=True, db_column='DEVSTACK', blank=True) # Field name made lowercase.
    devport = models.IntegerField(null=True, db_column='DEVPORT', blank=True) # Field name made lowercase.
    mac = models.CharField(max_length=36, db_column='MAC', blank=True) # Field name made lowercase.
    datefirst = models.DateTimeField(null=True, db_column='DATEFIRST', blank=True) # Field name made lowercase.
    datelast = models.DateTimeField(null=True, db_column='DATELAST', blank=True) # Field name made lowercase.
    inbase = models.IntegerField(null=True, db_column='INBASE', blank=True) # Field name made lowercase.
    devtype = models.IntegerField(null=True, db_column='DEVTYPE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_peleng_mac'

class TblPers(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    fio = models.CharField(max_length=600, db_column='FIO', blank=True) # Field name made lowercase.
    dolg = models.CharField(max_length=150, db_column='DOLG', blank=True) # Field name made lowercase.
    datein = models.DateField(null=True, db_column='DATEIN', blank=True) # Field name made lowercase.
    dateout = models.DateField(null=True, db_column='DATEOUT', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    iswork = models.IntegerField(null=True, db_column='ISWORK', blank=True) # Field name made lowercase.
    mainphone = models.IntegerField(null=True, db_column='MAINPHONE', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    smsuvedom = models.IntegerField(null=True, db_column='SMSUVEDOM', blank=True) # Field name made lowercase.
    mainmail = models.IntegerField(null=True, db_column='MAINMAIL', blank=True) # Field name made lowercase.
    mailuvedom = models.IntegerField(null=True, db_column='MAILUVEDOM', blank=True) # Field name made lowercase.
    mailuvedom2 = models.IntegerField(null=True, db_column='MAILUVEDOM2', blank=True) # Field name made lowercase.
    fioshort = models.CharField(max_length=765, db_column='FIOSHORT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_pers'

class TblPersDolg(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    otdelcode = models.IntegerField(null=True, db_column='OTDELCODE', blank=True) # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    dolg = models.CharField(max_length=765, db_column='DOLG', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    dateout = models.DateField(null=True, db_column='DATEOUT', blank=True) # Field name made lowercase.
    iswork = models.IntegerField(null=True, db_column='ISWORK', blank=True) # Field name made lowercase.
    ismain = models.IntegerField(null=True, db_column='ISMAIN', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_pers_dolg'

class TblPersOtdel(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    parentcode = models.IntegerField(null=True, db_column='PARENTCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_pers_otdel'

class TblPerstabel(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    datework = models.DateField(null=True, db_column='DATEWORK', blank=True) # Field name made lowercase.
    hour = models.IntegerField(null=True, db_column='HOUR', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_perstabel'

class TblPingtable(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    datestat = models.DateTimeField(null=True, db_column='DATESTAT', blank=True) # Field name made lowercase.
    count = models.IntegerField(null=True, db_column='COUNT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_pingtable'

class TblPortLearn(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    devcode = models.IntegerField(null=True, db_column='DEVCODE', blank=True) # Field name made lowercase.
    portcode = models.IntegerField(null=True, db_column='PORTCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_port_learn'

class TblPostav(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    adr = models.CharField(max_length=600, db_column='ADR', blank=True) # Field name made lowercase.
    okpo = models.CharField(max_length=36, db_column='OKPO', blank=True) # Field name made lowercase.
    inn = models.CharField(max_length=60, db_column='INN', blank=True) # Field name made lowercase.
    svid = models.CharField(max_length=120, db_column='SVID', blank=True) # Field name made lowercase.
    bank = models.CharField(max_length=600, db_column='BANK', blank=True) # Field name made lowercase.
    mfo = models.CharField(max_length=24, db_column='MFO', blank=True) # Field name made lowercase.
    scet = models.CharField(max_length=48, db_column='SCET', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=60, db_column='TEL', blank=True) # Field name made lowercase.
    tel2 = models.CharField(max_length=60, db_column='TEL2', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=60, db_column='FAX', blank=True) # Field name made lowercase.
    dird = models.CharField(max_length=90, db_column='DIRD', blank=True) # Field name made lowercase.
    dirfio = models.CharField(max_length=450, db_column='DIRFIO', blank=True) # Field name made lowercase.
    gbuhd = models.CharField(max_length=90, db_column='GBUHD', blank=True) # Field name made lowercase.
    gbuhfio = models.CharField(max_length=450, db_column='GBUHFIO', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=600, db_column='EMAIL', blank=True) # Field name made lowercase.
    icq = models.CharField(max_length=150, db_column='ICQ', blank=True) # Field name made lowercase.
    site = models.CharField(max_length=765, db_column='SITE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_postav'

class TblPunkt(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    adr = models.CharField(max_length=600, db_column='ADR', blank=True) # Field name made lowercase.
    grafik = models.CharField(max_length=600, db_column='GRAFIK', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=600, db_column='OPIS', blank=True) # Field name made lowercase.
    photo = models.CharField(max_length=600, db_column='PHOTO', blank=True) # Field name made lowercase.
    active = models.IntegerField(null=True, db_column='ACTIVE', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_punkt'

class TblRegion(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    maincode = models.IntegerField(null=True, db_column='MAINCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_region'

class TblRekl(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=600, db_column='OPIS', blank=True) # Field name made lowercase.
    param = models.CharField(max_length=600, db_column='PARAM', blank=True) # Field name made lowercase.
    param2 = models.CharField(max_length=600, db_column='PARAM2', blank=True) # Field name made lowercase.
    datestart = models.DateField(null=True, db_column='DATESTART', blank=True) # Field name made lowercase.
    datestop = models.DateField(null=True, db_column='DATESTOP', blank=True) # Field name made lowercase.
    result_0 = models.IntegerField(null=True, db_column='RESULT_0', blank=True) # Field name made lowercase.
    result_7 = models.IntegerField(null=True, db_column='RESULT_7', blank=True) # Field name made lowercase.
    result_14 = models.IntegerField(null=True, db_column='RESULT_14', blank=True) # Field name made lowercase.
    result_30 = models.IntegerField(null=True, db_column='RESULT_30', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_rekl'

class TblShtraf(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    perscode = models.IntegerField(null=True, db_column='PERSCODE', blank=True) # Field name made lowercase.
    shtrafcode = models.IntegerField(null=True, db_column='SHTRAFCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=765, db_column='DOP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_shtraf'

class TblSign(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    code1 = models.IntegerField(null=True, db_column='CODE1', blank=True) # Field name made lowercase.
    code2 = models.IntegerField(null=True, db_column='CODE2', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    stoped = models.IntegerField(null=True, db_column='STOPED', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_sign'

class TblSms(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=60, db_column='TEL', blank=True) # Field name made lowercase.
    smstext = models.TextField(db_column='SMSTEXT', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    datesend = models.DateTimeField(null=True, db_column='DATESEND', blank=True) # Field name made lowercase.
    smsprov = models.IntegerField(null=True, db_column='SMSPROV', blank=True) # Field name made lowercase.
    datedeliv = models.DateTimeField(null=True, db_column='DATEDELIV', blank=True) # Field name made lowercase.
    sms_prov_id = models.CharField(max_length=765, db_column='SMS_PROV_ID', blank=True) # Field name made lowercase.
    sms_prov_status = models.CharField(max_length=765, db_column='SMS_PROV_STATUS', blank=True) # Field name made lowercase.
    sms_prov_status2 = models.CharField(max_length=765, db_column='SMS_PROV_STATUS2', blank=True) # Field name made lowercase.
    smscount = models.IntegerField(null=True, db_column='SMSCOUNT', blank=True) # Field name made lowercase.
    par1 = models.CharField(max_length=765, db_column='PAR1', blank=True) # Field name made lowercase.
    par2 = models.CharField(max_length=765, db_column='PAR2', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_sms'

class TblSmslist(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    smstext = models.TextField(db_column='SMSTEXT', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    ifopis = models.TextField(db_column='IFOPIS', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_smslist'

class TblStatAct(models.Model):
    code = models.IntegerField(db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_stat_act'

class TblStatPing(models.Model):
    code = models.IntegerField(db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_stat_ping'

class TblStreet(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    street = models.CharField(max_length=765, db_column='STREET', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    citycode = models.IntegerField(null=True, db_column='CITYCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_street'

class TblSwitch(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    skladcode = models.IntegerField(null=True, db_column='SKLADCODE', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    com_public = models.CharField(max_length=765, db_column='COM_PUBLIC', blank=True) # Field name made lowercase.
    com_private = models.CharField(max_length=765, db_column='COM_PRIVATE', blank=True) # Field name made lowercase.
    com_login = models.CharField(max_length=765, db_column='COM_LOGIN', blank=True) # Field name made lowercase.
    com_pass = models.CharField(max_length=765, db_column='COM_PASS', blank=True) # Field name made lowercase.
    pelengcode = models.IntegerField(null=True, db_column='PELENGCODE', blank=True) # Field name made lowercase.
    valuememo = models.TextField(db_column='VALUEMEMO', blank=True) # Field name made lowercase.
    snmpver = models.IntegerField(null=True, db_column='SNMPVER', blank=True) # Field name made lowercase.
    fdpver = models.IntegerField(null=True, db_column='FDPVER', blank=True) # Field name made lowercase.
    x1 = models.IntegerField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.IntegerField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    upport = models.CharField(max_length=120, db_column='UPPORT', blank=True) # Field name made lowercase.
    onsms = models.IntegerField(null=True, db_column='ONSMS', blank=True) # Field name made lowercase.
    issmssend = models.IntegerField(null=True, db_column='ISSMSSEND', blank=True) # Field name made lowercase.
    hash_port1 = models.CharField(max_length=765, db_column='HASH_PORT1', blank=True) # Field name made lowercase.
    hash_port2 = models.TextField(db_column='HASH_PORT2', blank=True) # Field name made lowercase.
    onmail = models.IntegerField(null=True, db_column='ONMAIL', blank=True) # Field name made lowercase.
    ismailsend = models.IntegerField(null=True, db_column='ISMAILSEND', blank=True) # Field name made lowercase.
    proshivka = models.CharField(max_length=765, db_column='PROSHIVKA', blank=True) # Field name made lowercase.
    proshivka_date = models.DateTimeField(null=True, db_column='PROSHIVKA_DATE', blank=True) # Field name made lowercase.
    cablelen = models.TextField(db_column='CABLELEN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_switch'

class TblSwitchStack(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    devcode = models.IntegerField(null=True, db_column='DEVCODE', blank=True) # Field name made lowercase.
    portcode = models.IntegerField(null=True, db_column='PORTCODE', blank=True) # Field name made lowercase.
    stackno = models.IntegerField(null=True, db_column='STACKNO', blank=True) # Field name made lowercase.
    portno = models.IntegerField(null=True, db_column='PORTNO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_switch_stack'

class TblTarifchange(models.Model):
    code = models.IntegerField(db_column='CODE') # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    groupn = models.CharField(max_length=114, db_column='GROUPN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tarifchange'

class TblTerminal(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    termcode = models.IntegerField(null=True, db_column='TERMCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    termnumber = models.IntegerField(null=True, db_column='TERMNUMBER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    dop = models.CharField(max_length=765, db_column='DOP', blank=True) # Field name made lowercase.
    transcode = models.IntegerField(null=True, db_column='TRANSCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_terminal'

class TblTmcCross(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    tmcparent = models.IntegerField(null=True, db_column='TMCPARENT', blank=True) # Field name made lowercase.
    tmcchild = models.IntegerField(null=True, db_column='TMCCHILD', blank=True) # Field name made lowercase.
    param1 = models.IntegerField(null=True, db_column='PARAM1', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tmc_cross'

class TblTovar(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    tovarcode = models.IntegerField(null=True, db_column='TOVARCODE', blank=True) # Field name made lowercase.
    count = models.IntegerField(null=True, db_column='COUNT', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    prodav = models.IntegerField(null=True, db_column='PRODAV', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    datelast = models.DateTimeField(null=True, db_column='DATELAST', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    sn = models.CharField(max_length=150, db_column='SN', blank=True) # Field name made lowercase.
    code1 = models.IntegerField(null=True, db_column='CODE1', blank=True) # Field name made lowercase.
    code2 = models.IntegerField(null=True, db_column='CODE2', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    skladcode = models.IntegerField(null=True, db_column='SKLADCODE', blank=True) # Field name made lowercase.
    operation = models.TextField(db_column='OPERATION', blank=True) # Field name made lowercase.
    scet = models.BigIntegerField(null=True, db_column='SCET', blank=True) # Field name made lowercase.
    inv = models.CharField(max_length=765, db_column='INV', blank=True) # Field name made lowercase.
    shtrih = models.CharField(max_length=765, db_column='SHTRIH', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tovar'

class TblTovarjournal(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    tovarcode = models.IntegerField(null=True, db_column='TOVARCODE', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    count = models.IntegerField(null=True, db_column='COUNT', blank=True) # Field name made lowercase.
    code1 = models.IntegerField(null=True, db_column='CODE1', blank=True) # Field name made lowercase.
    code2 = models.IntegerField(null=True, db_column='CODE2', blank=True) # Field name made lowercase.
    code3 = models.IntegerField(null=True, db_column='CODE3', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tovarjournal'

class TblTovarsklad(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=600, db_column='NAZV', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=750, db_column='OPIS', blank=True) # Field name made lowercase.
    regioncode = models.IntegerField(null=True, db_column='REGIONCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tovarsklad'

class TblTovartype(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    tovarnazv = models.CharField(max_length=600, db_column='TOVARNAZV', blank=True) # Field name made lowercase.
    edizm = models.CharField(max_length=30, db_column='EDIZM', blank=True) # Field name made lowercase.
    basecode = models.IntegerField(null=True, db_column='BASECODE', blank=True) # Field name made lowercase.
    elcount = models.FloatField(null=True, db_column='ELCOUNT', blank=True) # Field name made lowercase.
    typecode = models.IntegerField(null=True, db_column='TYPECODE', blank=True) # Field name made lowercase.
    reserv = models.TextField(db_column='RESERV', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_tovartype'

class TblTrash(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    opercode = models.IntegerField(null=True, db_column='OPERCODE', blank=True) # Field name made lowercase.
    datedel = models.DateTimeField(null=True, db_column='DATEDEL', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_trash'

class TblTrouble(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    datestart = models.DateTimeField(null=True, db_column='DATESTART', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    oper = models.IntegerField(null=True, db_column='OPER', blank=True) # Field name made lowercase.
    datefinish = models.DateTimeField(null=True, db_column='DATEFINISH', blank=True) # Field name made lowercase.
    opisanswer = models.TextField(db_column='OPISANSWER', blank=True) # Field name made lowercase.
    dateview = models.DateTimeField(null=True, db_column='DATEVIEW', blank=True) # Field name made lowercase.
    isarc = models.IntegerField(null=True, db_column='ISARC', blank=True) # Field name made lowercase.
    isall = models.IntegerField(null=True, db_column='ISALL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_trouble'

class TblTroubleAll(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    theme = models.CharField(max_length=750, db_column='THEME', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    isall = models.IntegerField(null=True, db_column='ISALL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_trouble_all'

class TblTurbo(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    turbocode = models.IntegerField(null=True, db_column='TURBOCODE', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    datestop = models.DateTimeField(null=True, db_column='DATESTOP', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column='STATUS', blank=True) # Field name made lowercase.
    profit = models.FloatField(null=True, db_column='PROFIT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_turbo'

class TblUnkmac(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    mac = models.CharField(max_length=36, db_column='MAC', blank=True) # Field name made lowercase.
    userip = models.FloatField(null=True, db_column='USERIP', blank=True) # Field name made lowercase.
    firstdate = models.DateTimeField(null=True, db_column='FIRSTDATE', blank=True) # Field name made lowercase.
    lastdate = models.DateTimeField(null=True, db_column='LASTDATE', blank=True) # Field name made lowercase.
    modcode = models.IntegerField(null=True, db_column='MODCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_unkmac'

class TblUscallUser(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    login = models.CharField(max_length=765, db_column='LOGIN', blank=True) # Field name made lowercase.
    pass_field = models.CharField(max_length=765, db_column='PASS', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    userip = models.CharField(max_length=45, db_column='USERIP', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    callno = models.CharField(max_length=60, db_column='CALLNO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_uscall_user'

class TblUzel(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    codenumber = models.CharField(max_length=600, db_column='CODENUMBER', blank=True) # Field name made lowercase.
    housecode = models.IntegerField(null=True, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    podezd = models.IntegerField(null=True, db_column='PODEZD', blank=True) # Field name made lowercase.
    location = models.CharField(max_length=600, db_column='LOCATION', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    opis = models.TextField(db_column='OPIS', blank=True) # Field name made lowercase.
    isupd = models.IntegerField(null=True, db_column='ISUPD', blank=True) # Field name made lowercase.
    ismufta = models.IntegerField(null=True, db_column='ISMUFTA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_uzel'

class TblVlan(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    nazv = models.CharField(max_length=765, db_column='NAZV', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    equip = models.TextField(db_column='EQUIP', blank=True) # Field name made lowercase.
    vlantag = models.CharField(max_length=765, db_column='VLANTAG', blank=True) # Field name made lowercase.
    vlantag2 = models.CharField(max_length=765, db_column='VLANTAG2', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_vlan'

class TblWebmoney(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    summa = models.FloatField(null=True, db_column='SUMMA', blank=True) # Field name made lowercase.
    datedo = models.DateTimeField(null=True, db_column='DATEDO', blank=True) # Field name made lowercase.
    paymentno = models.IntegerField(null=True, db_column='PAYMENTNO', blank=True) # Field name made lowercase.
    dopdata = models.TextField(db_column='DOPDATA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_webmoney'

class TblWifi(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    skladcode = models.IntegerField(null=True, db_column='SKLADCODE', blank=True) # Field name made lowercase.
    opis = models.CharField(max_length=765, db_column='OPIS', blank=True) # Field name made lowercase.
    port = models.IntegerField(null=True, db_column='PORT', blank=True) # Field name made lowercase.
    uzelcode = models.IntegerField(null=True, db_column='UZELCODE', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    dateadd = models.DateField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    pelengcode = models.IntegerField(null=True, db_column='PELENGCODE', blank=True) # Field name made lowercase.
    com_public = models.CharField(max_length=765, db_column='COM_PUBLIC', blank=True) # Field name made lowercase.
    com_private = models.CharField(max_length=765, db_column='COM_PRIVATE', blank=True) # Field name made lowercase.
    com_login = models.CharField(max_length=765, db_column='COM_LOGIN', blank=True) # Field name made lowercase.
    com_pass = models.CharField(max_length=765, db_column='COM_PASS', blank=True) # Field name made lowercase.
    snmpver = models.IntegerField(null=True, db_column='SNMPVER', blank=True) # Field name made lowercase.
    fdpver = models.IntegerField(null=True, db_column='FDPVER', blank=True) # Field name made lowercase.
    upport = models.CharField(max_length=30, db_column='UPPORT', blank=True) # Field name made lowercase.
    hash_port1 = models.CharField(max_length=765, db_column='HASH_PORT1', blank=True) # Field name made lowercase.
    hash_port2 = models.TextField(db_column='HASH_PORT2', blank=True) # Field name made lowercase.
    azimut = models.IntegerField(null=True, db_column='AZIMUT', blank=True) # Field name made lowercase.
    sectcoord = models.CharField(max_length=765, db_column='SECTCOORD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_wifi'

