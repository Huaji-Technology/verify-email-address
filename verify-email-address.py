#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Huaji-Tech Inc.
# All rights reserved.
#
# "Verify Email Address" version 1.0
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Huaji-Tech Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ---
# Author: Zichoole
# E-mail: zichoole@gmail.com
# Date  : 2017-09-20 12:20:00
#
# ---
# Description:
#   Verify if email addresses are valid by checking SMTP server.
#
# ---
# TODO:
#   1. Complete unittests.
#
################################################################################

import re
import sys
import smtplib
import dns.resolver


# Email address format regex.
EMAIL_ADDRESS_REGEX="^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"


# Check if the format of email address is valid.
def check_email_address(email_address):
    return re.match(EMAIL_ADDRESS_REGEX, email_address) != None


# Get the host by the email address.
def get_email_host(email_address):
    return email_address.split("@")[1]


# Find the hostname of mail server by DNS-MX records.
def resolve_mx(email_address):
    email_host = get_email_host(email_address)
    records = dns.resolver.query(email_host, "MX")
    host_items = {record.exchange:record.preference for record in records}
    return host_items.items()


# Verify if the email address is valid.
def verify_email_address(email_address):
    smtp = smtplib.SMTP()
    host_items = resolve_mx(email_address)
    for host_item in host_items:
        try:
            host = b".".join(host_item[0][:-1]).decode("utf-8")
            print(
                smtp.connect(host)
            )
            print(
                smtp.helo("huaji-tech.com")
            )
            #print(
            #    smtp.sendmail("test@huaji-tech.com", email_address, "IgnoreMessage")
            #)
            return True
        except Exception as e:
            print(e)
            continue
    return False


# Print the help infomation.
def print_help():
    print("Usage: python verify-email-address.py name@example.com\n")
    print("WARNING: Need python 3.x above!\n")


# Main function of this script.
def main():
    # Check arguments.
    if len(sys.argv) < 2:
        print("\nMissing email address as argument!\n")
        print_help()
        sys.exit(1)

    # Check the format of email address.
    email_address=sys.argv[1]
    if not check_email_address(email_address):
        print("Invalid format of email address!")
        sys.exit(1)

    # Verify if the email address is valid.
    if verify_email_address(email_address):
        print("The email address is valid.")
    else:
        print("The email address is invalid.")


# The entrance of this script.
if __name__ == "__main__":
    main()
