from simple_salesforce import Salesforce

import config
import process_builder as pb

def run_script():

    exit_flag = True
    while exit_flag:
        opp_id = input('Please provide Opportunity Id: \n\n')

        if opp_id == 'q':
            exit(0)
        elif not opp_id.startswith('006'):
            print('This is not an Opportunity Id, why you so stupid, stupid?')
        else:
            success = execute_sfdc_update(opportunity_id=opp_id)

            if success:
                exit(0)


def execute_sfdc_update(opportunity_id: str):
    uname = config.SalesforceConfig['username']
    pwd = config.SalesforceConfig['password']
    sec_t = config.SalesforceConfig['security_token']

    # For Production Salesforce, login domain lives at https://login.salesforce.com
    # There, we pass 'login' as the value for the param domain
    # sfdc_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='login')

    # For Sandbox, you need to change domain to test
    # URL for sandbox login is https://test.salesforce.com
    # sfdc_sandbox_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='test')

    # f-string
    # my_string = f"blah blah blah {opportunity_id}"
    # my_string_2 = "blah blah blah" + opportunity_id

    # Step 0. Login to Salesforce, establish a "client" to be used for all SFDC work
    sfdc_client = Salesforce(username=uname, password=pwd, security_token=sec_t, domain='login')

    # Step 1. Turn off PBs
    pb.toggle_processes(sfdc_client=sfdc_client, activate=False, sobject='Contact')

    # Step 2. Query for Account Manager Id from Opportunity Account
    soql_opp = f"SELECT Id, AccountId, Account.Account_Manager_2__c, IsWon FROM Opportunity WHERE Id = '{opportunity_id}' LIMIT 1"
    opps = sfdc_client.query(soql_opp)['records']

    if not opps:
        print(f'Failed to retrieve Opportunity with Id {opportunity_id}. Please enter a new Id.')
        return False

    o = opps[0]
    account_id = o['AccountId']
    account_manager_id = o['Account']['Account_Manager_2__c']
    is_won = o['IsWon']

    if not is_won:
        print('This Opportunity is not marked Closed-Won, cannot continue.')
        return False

    # Step 3. Query for all Contacts associated with the Opp
    soql_contacts = f"SELECT Id, OwnerId FROM Contact WHERE AccountId = '{account_id}'"
    contacts = sfdc_client.query_all(soql_contacts)['response']

    # Step 4. Loop through all Contacts, if Contact Owner != Account AM, update Contact owner
    # For bulk updates, we need to setup a list of payloads
    contacts_for_update = []
    for cnt in contacts:
        cnt_id = cnt['Id']
        owner_id = cnt['OwnerId']

        if owner_id != account_manager_id:
            c = contact_payload(contact_id=cnt_id, account_manager_id=account_manager_id)

            contacts_for_update.append(c)

    # Step 5. Push Updates to Salesforce
    sfdc_client.bulk.Contact.update(contacts_for_update)

    # Step 6. Turn on PBs.
    pb.toggle_processes(sfdc_client=sfdc_client, activate=True, sobject='Contact')

    print('Done!')
    return True


def contact_payload(contact_id: str, account_manager_id: str):
    c = {
        "Id": contact_id,
        "OwnerId": account_manager_id
    }

    return c



if __name__ == '__main__':
    run_script()