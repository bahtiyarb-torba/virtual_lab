from SimpleXMLRPCServer import SimpleXMLRPCServer
from security_util import expose, requires_user_privilege, requires_authentication_only, \
    requires_admin_privilege, is_exposed, is_authorized


class XenAPIExposer:
    """ This class exposes the actual xen_api with a remote RPC interface """

    def __init__(self):
        self.prefix = 'xenapi'

    def _dispatch(self, method, params):
        """ This method receives all the calls to the xen_api. Perfo """

        # check if method starts with correct prefix
        if not method.startswith(self.prefix + "."):
            raise Exception('method "%s" is not supported' % method)

        method_name = method.partition('.')[2]
        func = getattr(self, method_name)

        if not is_exposed(func):
            raise Exception('method "%s" is not supported' % method)

        is_authorized(func, params[0], params[1])

        return func(*params)

    @expose
    @requires_admin_privilege
    def public(self, user, passwd):
        return 'This is public'

    @expose
    def public2(self, user, passwd):
        return 'This is public'

    def private(self):
        return 'This is private'


server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
server.register_instance(XenAPIExposer())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'