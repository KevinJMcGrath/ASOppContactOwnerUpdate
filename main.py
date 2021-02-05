from simple_salesforce import Salesforce

import config


def run_script():
    uname = config.SalesforceConfig['username']
    pwd = config.SalesforceConfig['password']
    sec_t = config.SalesforceConfig['security_token']

    # For Production Salesforce, login domain lives at https://login.salesforce.com
    # There, we pass 'login' as the value for the param domain
    sfdc_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='login')

    # For Sandbox, you need to change domain to test
    # URL for sandbox login is https://test.salesforce.com
    # sfdc_sandbox_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='test')




if __name__ == '__main__':
    run_script()