
from freebsd_ipfw import Firewall as FirewallOld

from settings import *

class Firewall(FirewallOld):

    def sync_nat_rules(self):
        self.ipfw_rules_nat[self.cursor] = 'nat tablearg ip from table(%s) to any' % IPFW_NAT_TABLE
        self.cursor += IPFW_RULE_STEP
        for nat in self.nats:
            self.ipfw_rules_nat[self.cursor] = 'nat %s ip from any to %s' % (nat.ipfw_nat_id,nat.local_address)
            self.cursor += IPFW_RULE_STEP
