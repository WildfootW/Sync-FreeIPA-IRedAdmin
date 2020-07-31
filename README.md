# Sync FreeIPA & IRedMail
###### tags: `readme`

# Reference
* [Reddit - iRedmail or MIAB](https://www.reddit.com/r/selfhosted/comments/7o5qwl/iredmail_or_miab/)
    * > I'm about to deploy my own email server and am planning on using iredmail, because of its (relativly) simple LDAP integration. It took me about a day to figure out in testing, but I got everything working perfectly.
      > Any features that are missing in the admin panel that are present in the pro panel can be configured on the command line. This page shows the differences between paid and free. https://www.iredmail.org/admin_panel.html
      > As far as I know, there isn't any missing functionality in iredmail, just missing config options in the admin panel, and as far as my environment is concerned, everything I could do in the web admin I can do from my IPA admin.
* [GitHub - ldap-mailcow](https://github.com/Programmierus/ldap-mailcow)
* [iRedMail Support → Sync mail users with another LDAP server](https://forum.iredmail.org/topic6064-iredmail-support-sync-mail-users-with-another-ldap-server.html)
    ```
    #!/bin/sh
    #
    # Sync users from another LDAP
    #
    # run in iRedMail-0.8.6/tools 
    #
    . ../conf/global
    . ../conf/core
    #
    # LDAP from which users will be synced (Source LDAP) fill in your data
    #
    urlAAI="ldap://sourceldap:389"
    basednAAI="dc=base,dc=ext"
    binddnAAI="cn=admin,dc=base,dc=ext"
    bindpwAAI="password"
    #
    # iRedMail LDAP (target LDAP) fill in your data
    #
    urlMAIL="ldap://targetldap:389"
    basednMAIL="o=domains,dc=base,dc=ext"
    binddnMAIL="cn=Manager,dc=base,dc=ext"
    bindpwMAIL="password"
    #
    # common variables from iRedMail setup
    #
    STORAGE_BASE_DIRECTORY="/var/vmail/vmail1"
    STORAGE_BASE="$(dirname ${STORAGE_BASE_DIRECTORY})"
    STORAGE_NODE="$(basename ${STORAGE_BASE_DIRECTORY})"
    #
    # get users uid from Source LDAP (I here have parameter which distinguish
    # different types of users(hrEduPersonPrimaryAffiliation=djelatnik) for employees in Source LDAP 
    #
    ldapsearch -H ${urlAAI} -x -D "${binddnAAI}" -w "${bindpwAAI}" -b "${basednAAI}" "(hrEduPersonPrimaryAffiliation=djelatnik)" "uid"  > AAI.ldif
    #
    # process .ldif output so in one line is only users uid
    #
    # example: AAI.ldif contains ONLY users uid each in newline
    # user1
    # user2
    # etc...
    #
    sed '/#/d' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    sed '/search:/d' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    sed '/result:/d' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    sed '/dn:/d' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    sed 's/uid: //' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    sed '/^$/d' < AAI.ldif > newAAI.ldif; mv newAAI.ldif AAI.ldif
    #
    # add users to array (each line in another member of array) and delete temporary file
    #
    declare -a AAIkorisnici
    let i=0
    while IFS=$'\n' read -r line_data; do
        AAIkorisnici[i]="${line_data}"
        ((++i))
    done < AAI.ldif
    rm -f AAI.ldif
    #
    # PROCESSING USERS
    #
    let i=0
    while (( ${#AAIkorisnici[@]} > i )); do
    #
    # check if user already in Target LDAP (already have mailbox)
    #
    checkuserMAIL=$(ldapsearch -x -H ${urlMAIL} -b "${basednMAIL}" -D "${binddnMAIL}" -w "${bindpwMAIL}" uid=${AAIkorisnici[i]} | grep uid: | awk '{print $1}')
    if [ "${checkuserMAIL}" = 'uid:' ]; 
        then
    #
    # user exist on Target LDAP ... so I will only synchronize password beetwen two LDAPs
    #
            printf "Korisnik ${AAIkorisnici[i]} postoji na mail serveru\n";
            printf "Sinhromizacija mail lozinke sa AAI za: ${AAIkorisnici[i]}\n";
    ldapsearch -H ${urlAAI} -x -D "${binddnAAI}" -w "${bindpwAAI}" -b "${basednAAI}" uid=${AAIkorisnici[i]} "(hrEduPersonPrimaryAffiliation=djelatnik)" "uid" "userPassword" | perl -MMIME::Base64 -MEncode=decode -n -00 -e 's/\n +//g;s/(?<=:: )(\S+)/decode("UTF-8",decode_base64($1))/eg;binmode(STDOUT, ":utf8");print' > userAAIpwtoMAILpw.ldif
    #
    # put user data in variables and delete temporary file
    #
    userUID=$(grep uid: userAAIpwtoMAILpw.ldif | awk '{print $2}')
    userPASSWORD=$(grep userPassword: userAAIpwtoMAILpw.ldif | awk '{print $2}')
    userMAIL=${userUID}@efzg.hr
    rm -f userAAIpwtoMAILpw.ldif

    ldapmodify -x -H ${urlMAIL} -D "${binddnMAIL}" -w "${bindpwMAIL}" <<EOF
    dn: mail=${userMAIL},ou=Users,domainName=efzg.hr,${basednMAIL}
    changetype: modify
    replace: userPassword
    userPassword: ${userPASSWORD}
    EOF

        else
    #
    # user does not exist on Target LDAP so it will be added
    #
            printf "Korisnik postoji u AAI ali ne i u mailu: ${AAIkorisnici[i]}\n";
        printf "Unosim korisnika u mail sustav : ${AAIkorisnici[i]}\n";
    #
    # get user data ftom Source LDAP (in my case i need: givenName, sn, userPassword, uid)
    #
    ldapsearch -H ${urlAAI} -x -D "${binddnAAI}" -w "${bindpwAAI}" -b "${basednAAI}" uid=${AAIkorisnici[i]} "(hrEduPersonPrimaryAffiliation=djelatnik)" "givenName" "sn" "userPassword" "uid"| perl -MMIME::Base64 -MEncode=decode -n -00 -e 's/\n +//g;s/(?<=:: )(\S+)/decode("UTF-8",decode_base64($1))/eg;binmode(STDOUT, ":utf8");print' > userAAItoMAIL.ldif
    #
    # put user data in variables and delete temporary file
    #
    userUID=$(grep uid: userAAItoMAIL.ldif | awk '{print $2}')
    userGIVENNAME=$(grep givenName: userAAItoMAIL.ldif | awk '{print $2}')
    userSN=$(grep sn: userAAItoMAIL.ldif | awk '{print $2}')
    userPASSWORD=$(grep userPassword: userAAItoMAIL.ldif | awk '{print $2}')
    userMAIL=${userUID}@efzg.hr
    maildir="$( hash_domain "efzg.hr")/$( hash_maildir ${userUID} )"
    rm -f userAAItoMAIL.ldif
    #
    # and finaly create user on mailserver....
    #
    ldapadd -x -H ${urlMAIL} -D "${binddnMAIL}" -w "${bindpwMAIL}" <<EOF
    dn: mail=${userMAIL},ou=Users,domainName=efzg.hr,${basednMAIL}
    objectClass: inetOrgPerson
    objectClass: shadowAccount
    objectClass: amavisAccount
    objectClass: mailUser
    objectClass: top
    accountStatus: active
    storageBaseDirectory: ${STORAGE_BASE}
    homeDirectory: ${STORAGE_BASE_DIRECTORY}/${maildir}
    mailMessageStore: ${STORAGE_NODE}/${maildir}
    mail: ${userMAIL}
    mailQuota: 1048576000
    userPassword: ${userPASSWORD}
    cn: ${userSN} ${userGIVENNAME}
    sn: ${userSN}
    givenName: ${userGIVENNAME}
    uid: ${userUID}
    shadowLastChange: 0
    amavisLocal: TRUE
    enabledService: internal
    enabledService: doveadm
    enabledService: lib-storage
    enabledService: mail
    enabledService: pop3
    enabledService: pop3secured
    enabledService: imap
    enabledService: imapsecured
    enabledService: managesieve
    enabledService: managesievesecured
    enabledService: sieve
    enabledService: sievesecured
    enabledService: smtp
    enabledService: smtpsecured
    enabledService: deliver
    enabledService: lda
    enabledService: forward
    enabledService: senderbcc
    enabledService: recipientbcc
    enabledService: shadowaddress
    enabledService: displayedInGlobalAddressBook
    EOF

        fi
    ((++i))
    done
    ```
* [iRedAdmin-Pro: RESTful API](https://docs.iredmail.org/iredadmin-pro.restful.api.html)
* [iRedMail - Integrate Microsoft Active Directory for user authentication and address book](https://docs.iredmail.org/active.directory.html)
    * > iRedAdmin-Pro doesn't work with Active Directory, so if you choose to authenticate mail users against Active Directory, you have to manage mail accounts with Active Directory management tools.
