# Sync FreeIPA & IRedMail
###### tags: `readme`

# Goal
* One way from FreeIPA's to IRedMail
* All Users & Groups should in group "mail_group"
* User
    * Create / Delete
    * Enable / Disable
    * Alias email address
    * Change password
    * Users create by FreeIPA have tag "managedbyipa"
* Group
    * As mailing list
    * Create / Delete
    * Sync user member


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
