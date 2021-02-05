from simple_salesforce import Salesforce

import config

def run_script():

    exit_flag = True
    while exit_flag:
        opp_id = input('Please provide Opportunity Id: \n\n')

        if opp_id == 'q':
            exit(0)
        elif not opp_id.startswith('006'):
            print('This is not an Opportunity Id, why you so stupid, stupid?')
        else:
            exit_flag = execute_sfdc_update(opportunity_id=opp_id)


def execute_sfdc_update(opportunity_id: str):
    uname = config.SalesforceConfig['username']
    pwd = config.SalesforceConfig['password']
    sec_t = config.SalesforceConfig['security_token']

    # For Production Salesforce, login domain lives at https://login.salesforce.com
    # There, we pass 'login' as the value for the param domain
    sfdc_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='login')

    # For Sandbox, you need to change domain to test
    # URL for sandbox login is https://test.salesforce.com
    # sfdc_sandbox_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='test')

    # f-string
    # my_string = f"blah blah blah {opportunity_id}"
    # my_string_2 = "blah blah blah" + opportunity_id


    # TODO: Add Process Builder On/Off

    # Step 1. Turn off PBs

    # Step 2. Query for Account Manager Id from Opportunity Account

    # Step 3. Query for all Contacts associated with the Opp

    # Step 4. Loop through all Contacts, if Contact Owner != Account AM, update Contact owner

    # Step 5. Push Updates to Salesforce

    # Step 6. Turn on PBs.


    soql_opp = f"SELECT Id, AccountId, Account.Account_Manager_2__c FROM Opportunity WHERE Id = '{opportunity_id}' LIMIT 1"

    opps_response = sfdc_client.query(soql_opp)

    opps = opps_response['records']
    o = None
    account_id = None
    account_manager_id = None

    if len(opps) > 0:
        o = opps[0]
        account_id = o['AccountId']
        account_manager_id = o['Account']['Account_Manager_2__c']
    else:
        print('This opp_id returned no Opportunity Record, please check again')
        return False

    soql_contacts = f"SELECT Id, OwnerId FROM Contact WHERE AccountId = '{account_id}'"

    contacts_for_update = []
    contacts_response = sfdc_client.query_all(soql_contacts)

    contacts = contacts_response['records']

    # For bulk updates, we need to setup a list of payloads

    for cnt in contacts:
        cnt_id = cnt['Id']
        owner_id = cnt['OwnerId']

        if owner_id != account_manager_id:
            c = contact_payload(contact_id=cnt_id, account_manager_id=account_manager_id)

            contacts_for_update.append(c)

    # 0063g000003963o
    sfdc_client.bulk.Contact.update(contacts_for_update)


def contact_payload(contact_id: str, account_manager_id: str):
    c = {
        "Id": contact_id,
        "OwnerId": account_manager_id
    }

    return c



if __name__ == '__main__':
    run_script()