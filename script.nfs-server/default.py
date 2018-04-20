import xbmc
import xbmcvfs
import xbmcaddon
from os import system


# addon
__addon__ = xbmcaddon.Addon()


def service(state):
    if state == 'stop':
        system('systemctl disable nfs-server')
        system('systemctl stop nfs-server')
    elif state == 'start':
        system('systemctl enable nfs-server')
        system('systemctl start nfs-server')
    else:
        if system('systemctl status nfs-server > /dev/null') == 0:
            return True


def writeexports():
    file = xbmcvfs.File(xbmc.translatePath('/storage/.config/exports'), 'w')
    for i in range(0, int(shares)):
        exec('folder{0} = __addon__.getSetting("SHARE_FOLDER{0}")'.format(i))
        exec('permission{0} = __addon__.getSetting("PERMISSION{0}")'.format(i))
        if eval('folder{0}'.format(i)):
            file.write('{0} *({1},insecure,anonuid=0,anongid=0,all_squash,no_subtree_check)\n'.format(eval('folder{0}'.format(i)), eval('permission{0}'.format(i))))
    file.close()
    system('exportfs -rav')


if __name__ == '__main__':
    # Open settings dialog
    __addon__.openSettings()
    shares = __addon__.getSetting('SHARES')
    if shares == '0' and service('status'):
        service('stop')
    elif not service('status') and shares != '0':
        service('start')
    writeexports()

