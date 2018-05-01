import sqlite3


class JenkinsDatabase:
    def __init__(self, db=''):
        self.db = db
        self.connection = None
        self.cursor = None
        if db:
            self.connect()
            self.create_table()

    def connect(self, db=''):
        if db:
            self.db = db
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("CREATE TABLE if not exists jobs ('name' TEXT NOT NULL PRIMARY KEY UNIQUE, status TEXT, last_updated TEXT);")

    def exists(self, job_name):
        self.cursor.execute('SELECT 1 FROM jobs WHERE name=? LIMIT 1;', (job_name, ))
        return self.cursor.fetchone()

    def insert_or_update(self, rows):
        for row in rows:
            exists = self.exists(row['name'])
            if exists:
                self.cursor.execute('UPDATE jobs SET status=?, last_updated=? WHERE name=?;',
                                    (row['status'], row['last_updated'], row['name']))
            else:
                self.cursor.execute('INSERT INTO jobs VALUES (?,?,?);',
                                    (row['name'], row['status'], row['last_updated']))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None


class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def output(msg):
    print(msg)


def show_header(CONFIG):
    header_msg = 'Running jenkins demo script using the following arguments:\n'
    for param in CONFIG:
        header_msg += param + ': ' + str(CONFIG[param]) + '\n'
    header_msg += 'To change any of the arguments edit \'defaults.json\' or use the command line arguments\n'
    header_msg += 'For more info on the command line arguments run \'python run_demo.py -h\''
    output(bcolors.HEADER + header_msg + bcolors.ENDC)


def output_error(error_msg):
    output(bcolors.FAIL + error_msg + bcolors.ENDC)


def output_success(success_msg):
    output(bcolors.OKGREEN + success_msg + bcolors.ENDC)
