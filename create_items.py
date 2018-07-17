#!/usr/bin/python
# -*- coding: utf-8 -*-

from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

root = makerequest.makerequest(app)
site = root.mysite
admin = root.acl_users.getUserById('admin')
admin = admin.__of__(site.acl_users)

newSecurityManager(None, admin)

from zope.site.hooks import setHooks
from zope.component.hooks import setSite
setHooks()
setSite(site)
site.setupCurrentSkin(site.REQUEST)


from plone import api
import transaction

mydict = {'news': 'News Item', 'events': 'Event'}

for k in mydict:
    folder = site[k]
    for i in range(1,10):
        item = api.content.create(
            type=mydict[k],
            title=u'%s %s' % (mydict[k], str(i)),
            container=site[k])
        item.description = u"%s %s" % ('Description #', str(i))
        item.reindexObject()

transaction.commit()

