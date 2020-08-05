import imaplib
import email

IMAP_HOST = "imap.gmail.com"


class EmailImporter:
    def __init__(self, username, password, search_criteria, verbose, stdout):
        self.username = username
        self.password = password
        self.search_criteria = search_criteria
        self.verbose = verbose
        self.stdout = stdout
        self.imap_client = None

    def import_emails_body_list(self):
        self.__open_imap_connection()
        emails_id_list = self.__fetch_emails_id_list()
        emails_body_list = self.__fetch_emails_body_list(emails_id_list)
        self.__close_imap_connection()
        return emails_body_list

    def __open_imap_connection(self):
        self.imap_client = imaplib.IMAP4_SSL(IMAP_HOST)
        self.imap_client.login(self.username, self.password)

    def __fetch_emails_id_list(self):
        status, _ = self.imap_client.select("INBOX", readonly=True)
        if status != "OK":
            raise Exception("Could not select INBOX.")

        status, data = self.imap_client.search(None, self.search_criteria)
        if status != "OK":
            raise Exception("Could not search for emails.")

        id_list = data[0].decode("utf-8").split(' ')
        if self.verbose:
            self.stdout.write(
                "{} messages were found. Fetching will start immediately.".format(len(id_list)))
            self.stdout.write("Messages ids: {}".format(id_list))
            self.stdout.write('')

        return id_list

    def __fetch_emails_body_list(self, emails_id_list):
        email_body_list = []
        for email_id in emails_id_list:
            status, email_data = self.imap_client.fetch(email_id, '(RFC822)')
            if status != "OK":
                raise Exception("Could not fetch email with id {}".format(email_id))

            for email_part in email_data:
                if isinstance(email_part, tuple):
                    msg = email.message_from_bytes(email_part[1])

                    # Extract message body
                    body = None
                    if msg.is_multipart():
                        for part in msg.walk():
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    else:
                        body = msg.get_payload(decode=True).decode()
                    if body is None:
                        continue

                    email_body_list.append(body)
                    if self.verbose:
                        self.stdout.write("Data was fetched for {} messages out of {} messages".format(
                            len(email_body_list),
                            len(emails_id_list)
                        ))

        return email_body_list

    def __close_imap_connection(self):
        self.imap_client.close()
        self.imap_client.logout()
