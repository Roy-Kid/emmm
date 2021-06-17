import gettext, os
gettext.bindtextdomain('mollab', os.path.dirname(os.path.realpath(__file__))+'/i18n/language')
gettext.textdomain('mollab')
_ = gettext.gettext