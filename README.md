# pmauth
An authentication system based on password managers


# design diary

## 2025-11-07

website redirects to /login when authentication is needed, which
presents a standard login form with email and password fields, plus a
link "Reset password or create account"

first time user: the fields are blank.  The user will naturally enter
their email and click "Reset password or create account".  If the user
clicks the submit button of the bank form, or clicks the link without
filling in an email address, website presents the empty form again
with more verbose coaching that they need to enter their email address
and click the create account button

website makes a row in the accounts table with the email address and a
one-time token.  sends email to the user with a link to
/auth?token=XXX

user clicks on link in email

website looks up account based on the onetime token, yielding the
email address.  website generates a long random password - maybe 15 to
20 digits and numbers.  stores a standard password hash of this string
in the database.  displays a standard login/password form with the
login pre-filled with the email address and the password pre-filled.
includes the text "A random password has been generated for you and
filled in to this form.  Click Login to proceed to the site.  To save
time for future logins, click Yes when your password manager asks if
you want to save this password."

If the user clicks submit, we trust them to click yes for the password
manager.

notice that the server only holds the cleartext password long enough
to send the pre-filled login form.  the browser will send it back when
submitting the form, and the server will forget it right after it
computes the hash, as usual for incoming passwords.  so the only place
where the cleartext password is persistent is in the password manager

When the user returns from any brower that share access to that
password manager, the browser will pre-fill the form with the saved
password, the user will simply click Login, and win.

If the login form is submitted with an incorrect password, the website
displays "Incorrect password".  If the one-time token is in the
session, we know we're trying to create an account, but the user
messed up the pre-initialized password.  The server didn't keep a copy
of it, so it generates a new password and displays the pre-filled form
again, possible with coaching to get them to just click submit.  If we
don't have the one time token in the session, just display the blank
form again and hope the password manager fills it in and the user
doesn't disturb things this time.  Maybe offer some coaching.

Most users will be well served by this.  If they get a new laptop and
sync with their password manager before visiting our site, then their
login will be smooth.

A small number of users will visit from browsers that don't share a
password manager database.  There experience is a little bumpier but
we can still support them well.  To the above, add a checkbox to the
login form with text like: "If you keep having to reset your password,
checking this box enables extra server features that may help."  When
the login form is submitted with this box checked, we remember this
choice for this user in the server database. Instead of generating a
new random password every time a valid one time token is submitted, we
save the cleartext of the random long password and keep reusing it.
This is a little less secure, since the cleartext would be exposed if
the server database is stolen, but it allows the same password to be
propagated to disjoint password managers.  At least we're safe from a
bad guy trying to get the server to send the cleartext password since
the server only sends it when it has just received a valid one time
token, which proves the submitter has received a recent email.

If the user resets their password manager, or anything else goes
wrong, they can go to the login page, enter their email, and click
reset password.  This goes through the same flow as above,
authenticated by the fact that the form is submitted with the token
that is sent in email.  When the password manager detects that the
login was successful, it will prompt asking the user if they want to
update the password, and we trust them to say yes

## 2025-11-09

Instead of having people opt out of higher security, lets' make make
it easy to have basic security by default and a smooth path to opt
into higher security.  specifically, save the cleartext password for
new accounts in the server database, and reuse it for "forgot
password" requests.  Then, either the login form or on a user account
management page, have a flag for "i want higher security".  If this
request is submitted, store the flag in the server database and
destroy the current password.  The next time the user uses "forgot
password", the server will generate a new password but only store the
hash. Advise the user "Since you're using the high security option,
you may have to manually copy the password between password managers
in different domains"

