# Sync FreeIPA & IRedMail
###### tags: `readme`
# Status: Cancel

# Goal
* One way from FreeIPA's to IRedMail
* All Users & Groups should in group "mail_group"
* User
    * Create / Delete
    * Enable / Disable (Cancel. Just Create:Create. Preserve:Disable)
    * Alias email address
        * Only match primary domain. maintain alias domain by duplicate primary domain address
    * Change password
    * Users create by FreeIPA have tag "managedbyipa"
* Group
    * As mailing list
    * Create / Delete
    * Sync user member

## step
1. Get groups and users within "mail_users" group
2. Collect group's name, member; User's name, password hash, mail address
3. ...

# requirements
* python3
    * ldap3

# Reference
* [Reddit - iRedmail or MIAB](https://www.reddit.com/r/selfhosted/comments/7o5qwl/iredmail_or_miab/)
    * > I'm about to deploy my own email server and am planning on using iredmail, because of its (relativly) simple LDAP integration. It took me about a day to figure out in testing, but I got everything working perfectly.
      > Any features that are missing in the admin panel that are present in the pro panel can be configured on the command line. This page shows the differences between paid and free. https://www.iredmail.org/admin_panel.html
      > As far as I know, there isn't any missing functionality in iredmail, just missing config options in the admin panel, and as far as my environment is concerned, everything I could do in the web admin I can do from my IPA admin.
* [GitHub - ldap-mailcow](https://github.com/Programmierus/ldap-mailcow)
* [iRedMail Support → Sync mail users with another LDAP server](https://forum.iredmail.org/topic6064-iredmail-support-sync-mail-users-with-another-ldap-server.html)
* [iRedAdmin-Pro: RESTful API](https://docs.iredmail.org/iredadmin-pro.restful.api.html)
* [iRedMail - Integrate Microsoft Active Directory for user authentication and address book](https://docs.iredmail.org/active.directory.html)
    * > iRedAdmin-Pro doesn't work with Active Directory, so if you choose to authenticate mail users against Active Directory, you have to manage mail accounts with Active Directory management tools.
* [iRedMail Support → Invalid DN syntax (34) for user](https://forum.iredmail.org/topic2281-invalid-dn-syntax-34-for-user.html)
    * > You can login to phpLDAPadmin with two accounts (LDAP DN), you can find them in root directory of iRedMail installation directory, e.g. /root/iRedMail-0.7.3-rc2/iRedMail.tips, includes password of them:
    * > cn=Manager,dc=xxx,dc=xxx: This is root dn, same as root user on Linux system in OpenLDAP server.
    * > cn=vmailadmin,dc=xxx,dc=xxx: This is a special account, used to manage mail account related LDAP data. It has read+write permissions under o=domains,dc=xxx,dc=xxx and o=domainAdmins,dc=xxx,dc=xxx.
* [V4/User Life-Cycle Management](https://www.freeipa.org/page/V4/User_Life-Cycle_Management)
* [CHAPTER 10. MANAGING USER ACCOUNTS USING THE IDM WEB UI](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_identity_management/managing-user-accounts-using-the-idm-web-ui_configuring-and-managing-idm)
* [Re: Freeipa-users Bash script to see if user is enabled or disabled?](https://www.redhat.com/archives/freeipa-users/2014-May/msg00047.html)
    - nothing, the attribute hasn't been set yet
    - FALSE, the user is enabled
    - TRUE, the user is disabled
* [how to read attributes for given DN in ldap3 (how to search with ldap3 if no filter)](https://stackoverflow.com/questions/47665285/how-to-read-attributes-for-given-dn-in-ldap3-how-to-search-with-ldap3-if-no-fil)
    * `search_filter= '(objectClass=*)', # required`
* [Extending the FreeIPA Server](https://www.freeipa.org/images/5/5b/FreeIPA33-extending-freeipa.pdf)
* [FreeIPA Directory Server](https://www.freeipa.org/page/Directory_Server)
    * `cn=users,cn=compat,dc=example,dc=com`
* [how to escape bracktes in search_filter? #153](https://github.com/cannatag/ldap3/issues/153)
    * `(&(objectClass=user)(memberof=CN=AB \28UMH\29,OU=Mailverteiler,OU=MSX,OU=Adressbuch,DC=x,DC=y,DC=z))`
* [Re: Freeipa-users Where and how are passwords stored?](https://www.redhat.com/archives/freeipa-users/2015-February/msg00178.html)
    * > The attributes themselves are protected by the access control instructions (ACI) so only a super priviledged admin or user himself can interact with this attribute.
* [Re: Freeipa-users How grant access to userPassword for System Accounts](https://www.redhat.com/archives/freeipa-users/2015-October/msg00315.html)
    * > aci: (targetattr = "userPassword") (target = "ldap:///cn=users,cn=accounts,dc=<my>,dc=<domain>") (version 3.0;acl "Allow password read";allow (read,compare,search)(groupdn = "ldap:///<system accounts group dn>");)

