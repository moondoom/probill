from django.db import models

class TblBase(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    codeti = models.CharField(max_length=108, db_column='CODETI', blank=True) # Field name made lowercase.
    groupn = models.CharField(max_length=114, db_column='GROUPN', blank=True) # Field name made lowercase.
    groupr = models.IntegerField(null=True, db_column='GROUPR', blank=True) # Field name made lowercase.
    isreg = models.IntegerField(null=True, db_column='ISREG', blank=True) # Field name made lowercase.
    logname = models.CharField(max_length=60, db_column='LOGNAME', blank=True) # Field name made lowercase.
    logpass = models.IntegerField(null=True, db_column='LOGPASS', blank=True) # Field name made lowercase.
    dognumber = models.CharField(max_length=60, db_column='DOGNUMBER', blank=True) # Field name made lowercase.
    datedog2 = models.CharField(max_length=30, db_column='DATEDOG2', blank=True) # Field name made lowercase.
    fio = models.CharField(max_length=765, db_column='FIO', blank=True) # Field name made lowercase.
    nick = models.CharField(max_length=90, db_column='NICK', blank=True) # Field name made lowercase.
    pass_field = models.CharField(max_length=150, db_column='PASS', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    housec = models.IntegerField(null=True, db_column='HOUSEC', blank=True) # Field name made lowercase.
    podezd = models.IntegerField(null=True, db_column='PODEZD', blank=True) # Field name made lowercase.
    housecode = models.CharField(max_length=30, db_column='HOUSECODE', blank=True) # Field name made lowercase.
    floor = models.IntegerField(null=True, db_column='FLOOR', blank=True) # Field name made lowercase.
    apart = models.IntegerField(null=True, db_column='APART', blank=True) # Field name made lowercase.
    apart_b = models.CharField(max_length=96, db_column='APART_B', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=300, db_column='EMAIL', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=765, db_column='TEL', blank=True) # Field name made lowercase.
    telmob = models.CharField(max_length=765, db_column='TELMOB', blank=True) # Field name made lowercase.
    browser = models.CharField(max_length=300, db_column='BROWSER', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    dop2 = models.TextField(db_column='DOP2', blank=True) # Field name made lowercase.
    scet = models.FloatField(null=True, db_column='SCET', blank=True) # Field name made lowercase.
    balans = models.FloatField(null=True, db_column='BALANS', blank=True) # Field name made lowercase.
    kredit = models.IntegerField(null=True, db_column='KREDIT', blank=True) # Field name made lowercase.
    inkredit = models.IntegerField(null=True, db_column='INKREDIT', blank=True) # Field name made lowercase.
    skidka = models.IntegerField(null=True, db_column='SKIDKA', blank=True) # Field name made lowercase.
    dateplus = models.DateField(null=True, db_column='DATEPLUS', blank=True) # Field name made lowercase.
    lastact = models.DateTimeField(null=True, db_column='LASTACT', blank=True) # Field name made lowercase.
    lastping = models.DateTimeField(null=True, db_column='LASTPING', blank=True, auto_now_add=True) # Field name made lowercase.
    workstatus = models.IntegerField(null=True, db_column='WORKSTATUS', blank=True) # Field name made lowercase.
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
    logonmac = models.CharField(max_length=51, db_column='LOGONMAC', blank=True) # Field name made lowercase.
    logonip = models.FloatField(null=True, db_column='LOGONIP', blank=True) # Field name made lowercase.
    dateakciya = models.DateField(null=True, db_column='DATEAKCIYA', blank=True) # Field name made lowercase.
    metr = models.IntegerField(null=True, db_column='METR', blank=True) # Field name made lowercase.
    dateadd = models.DateTimeField(null=True, db_column='DATEADD', blank=True) # Field name made lowercase.
    datecorrect = models.DateTimeField(null=True, db_column='DATECORRECT', blank=True) # Field name made lowercase.
    isupd = models.IntegerField(null=True, db_column='ISUPD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_base'


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

class TblGroup(models.Model):
    code = models.CharField(max_length=114, primary_key=True, db_column='CODE', blank=True) # Field name made lowercase.
    groupname = models.CharField(max_length=150, db_column='GROUPNAME', blank=True) # Field name made lowercase.
    price = models.FloatField(null=True, db_column='PRICE', blank=True) # Field name made lowercase.
    trafex = models.IntegerField(null=True, db_column='TRAFEX', blank=True) # Field name made lowercase.
    users = models.IntegerField(null=True, db_column='USERS', blank=True) # Field name made lowercase.
    trafbuh = models.IntegerField(null=True, db_column='TRAFBUH', blank=True) # Field name made lowercase.
    abon = models.FloatField(null=True, db_column='ABON', blank=True) # Field name made lowercase.
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
    priznak = models.IntegerField(null=True, db_column='PRIZNAK', blank=True) # Field name made lowercase.
    akciya_day = models.IntegerField(null=True, db_column='AKCIYA_DAY', blank=True) # Field name made lowercase.
    akciya_many = models.IntegerField(null=True, db_column='AKCIYA_MANY', blank=True) # Field name made lowercase.
    notsms = models.IntegerField(null=True, db_column='NOTSMS', blank=True) # Field name made lowercase.
    isturbo = models.IntegerField(null=True, db_column='ISTURBO', blank=True) # Field name made lowercase.
    speedtx = models.IntegerField(null=True, db_column='SPEEDTX', blank=True) # Field name made lowercase.
    speedrx = models.IntegerField(null=True, db_column='SPEEDRX', blank=True) # Field name made lowercase.
    dogroup = models.IntegerField(null=True, db_column='DOGROUP', blank=True) # Field name made lowercase.
    isupd = models.IntegerField(null=True, db_column='ISUPD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_group'


class TblHouse(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    streetcode = models.IntegerField(null=True, db_column='STREETCODE', blank=True) # Field name made lowercase.
    house = models.IntegerField(null=True, db_column='HOUSE', blank=True) # Field name made lowercase.
    house_b = models.CharField(max_length=765, db_column='HOUSE_B', blank=True) # Field name made lowercase.
    x1 = models.FloatField(null=True, db_column='X1', blank=True) # Field name made lowercase.
    y1 = models.FloatField(null=True, db_column='Y1', blank=True) # Field name made lowercase.
    x2 = models.FloatField(null=True, db_column='X2', blank=True) # Field name made lowercase.
    y2 = models.FloatField(null=True, db_column='Y2', blank=True) # Field name made lowercase.
    coord = models.TextField(db_column='COORD', blank=True) # Field name made lowercase.
    map = models.IntegerField(null=True, db_column='MAP', blank=True) # Field name made lowercase.
    dop = models.TextField(db_column='DOP', blank=True) # Field name made lowercase.
    podezd = models.IntegerField(null=True, db_column='PODEZD', blank=True) # Field name made lowercase.
    floor = models.IntegerField(null=True, db_column='FLOOR', blank=True) # Field name made lowercase.
    vihod = models.CharField(max_length=150, db_column='VIHOD', blank=True) # Field name made lowercase.
    kluch = models.CharField(max_length=750, db_column='KLUCH', blank=True) # Field name made lowercase.
    billingcode = models.IntegerField(null=True, db_column='BILLINGCODE', blank=True) # Field name made lowercase.
    workdop = models.CharField(max_length=765, db_column='WORKDOP', blank=True) # Field name made lowercase.
    workdop_date = models.DateTimeField(null=True, db_column='WORKDOP_DATE', blank=True) # Field name made lowercase.
    ismark = models.IntegerField(null=True, db_column='ISMARK', blank=True) # Field name made lowercase.
    ishide = models.IntegerField(null=True, db_column='ISHIDE', blank=True) # Field name made lowercase.
    apartc = models.IntegerField(null=True, db_column='APARTC', blank=True) # Field name made lowercase.
    notused = models.IntegerField(null=True, db_column='NOTUSED', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_house'

class TblIp(models.Model):
    code = models.IntegerField( db_column='CODE') # Field name made lowercase.
    typer = models.IntegerField(null=True, db_column='TYPER', blank=True) # Field name made lowercase.
    usercode = models.IntegerField(null=True, db_column='USERCODE', blank=True) # Field name made lowercase.
    userip = models.FloatField(primary_key=True, db_column='USERIP', blank=True) # Field name made lowercase.
    mac = models.CharField(max_length=51, db_column='MAC', blank=True) # Field name made lowercase.
    updmac = models.IntegerField(null=True, db_column='UPDMAC', blank=True) # Field name made lowercase.
    isupd = models.IntegerField(null=True, db_column='ISUPD', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_ip'

class TblStreet(models.Model):
    code = models.IntegerField(primary_key=True, db_column='CODE') # Field name made lowercase.
    street = models.CharField(max_length=150, db_column='STREET', blank=True) # Field name made lowercase.
    isdel = models.IntegerField(null=True, db_column='ISDEL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tbl_street'

