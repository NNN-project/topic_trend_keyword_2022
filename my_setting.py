# my_settings.py
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'topic_keywords_db',
        'USER': 'admin',
        'PASSWORD': '******',
        'HOST': 'tkt-db-ko.cnirlhwrm55r.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}
SECRET_KEY = 'azh7kn)z$e8^#ika=!$s74*g3xuf%2be^eos#58&ehwf1+3nkp'
