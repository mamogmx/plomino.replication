from Products.Five.browser import BrowserView
from plone import api
from Products.CMFCore.utils import getToolByName


class connections(BrowserView):
    """ A list of Database Connections
    """
    def connList(self):
        results = []
        site = api.portal.get()
        conn_folder = site['replication_connections']
        for conn in conn_folder:
            r = dict(
                id = conn.id,
                title = conn.title,
                url = conn.absolute_url(),
                conn_string = conn.conn_string,
                schema = conn.db_schema,
                table = conn.db_table
            )
            results.append(r)
        return results