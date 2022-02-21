import logging
from os import listdir
from os import remove
import salt.modules.yumpkg

log = logging.getLogger(__name__) # pylint: disable=invalid-name
__virtualname__ = "yumrepo"

def test():
    """
    Simple dummy rest to prove module is loaded. This should always return true

    CLI Example:
    salt '*' yumrepo.test
    """
    return True


def cleanup():
  DIR_PATH = '/etc/yum.repos.d/repos/'
  lis_files = listdir(DIR_PATH)
  delete_action = 0

  for file in lis_files:
    if not file.startswith('CentOS'):
      remove(DIR_PATH + "//" + file)
      delete_action += 1

  if delete_action == 0:
    return ('False')
  else:
    return ('True')

def list():
  DIR_PATH = '/etc/yum.repos.d/repos/'
  return (listdir(DIR_PATH))

def _osver():
 return(__grains__['osmajorrelease'])

def getrepo():
    data = {}
    ti = 'false'
#    osver = __grains__['osmajorrelease']
    osver = 8
    if osver == 8:
        good_repo = ['centos-appstream', 'centos-baseos', 'centos-extras' ]
    else:
        good_repo = ['centos-appstream7', 'centos-baseos7', 'centos-extras7' ]

    data = salt.modules.yumpkg.list_repos("/etc/yum.repos.d/")

    for repo_id,is_enable in data.items():
        if repo_id in good_repo:
           if int(is_enable.get("enabled")):
              ti = 'True'
           else:
              ti = 'False'
        else:
           if int(is_enable.get("enabled")):
              ti = 'False'

    return(ti)

def check_enable(repo_id):
    """
    Take repoid as agrument to check if it is enable

    salt "*" yumrepo.check_enable centos-appstream

    """
    data = salt.modules.yumpkg.list_repos("/etc/yum.repos.d/")
    data2 = data.get(repo_id)
    if int(data2.get("enabled")) == 1:
       return True
    else:
       return False

def getrepo_n():
    data = {}
    ex = 0
    log.debug("Getting the OS version using grains")
    osver = __grains__['osmajorrelease']
#    osver = 8
    log.debug("Initializating list for known repositories for CentOS7 and C8s")
    if osver == 8:
        good_repo = ['centos-appstream', 'centos-baseos', 'centos-extras' ]
    else:
        good_repo = ['centos-appstream7', 'centos-baseos7', 'centos-extras7' ]

    data = salt.modules.yumpkg.list_repos("/etc/yum.repos.d/")

    #for repo_id in data.keys():
    for repo_id in data.items():
        print(repo_id.key)
        if repo_id in good_repo:
           if check_enable(repo_id):
              ex += 1
           else:
              return False
        else:
           return False
    if int(ex) == 3:
       return True
    else:
       return False