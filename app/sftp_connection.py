import pysftp

sftpHost = '185.164.16.144'
sftpPort = 22
userName = 'michaln'
password = 'misH2911'


def sftp_get_files():
    """ this code will actually blindly accept any host key (cnopts.hostkeys = None), which is a security flaw."""
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=sftpHost, username=userName, password=password, cnopts=cnopts) as sftp:
        print("Connection succesfully established … ")
        print(sftp.pwd)
        # change to a remote directory
        sftp.cwd('../../var/tmp/csv_files/')
        print('change to a remote directory  {}'.format(sftp.pwd))
        directory_structure = sftp.listdir_attr()
        # Print data
        for attr in directory_structure:

            print(attr.filename)
            # Define the local path where the file will be saved

            localFilePath = 'static/files/{}'.format(attr.filename)
            print(localFilePath)
            sftp.get(attr.filename, localFilePath)

