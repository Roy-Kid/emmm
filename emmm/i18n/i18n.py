import gettext, os
gettext.bindtextdomain('emmm', os.path.dirname(os.path.realpath(__file__))+'/i18n/language')
gettext.textdomain('emmm')
_ = gettext.gettext