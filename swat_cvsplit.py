# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)

import os

class alternate(object):
    def __init__(self):
        self.run()

    def get_project(self):
        project = input("Please insert the project path: ")
        # project = os.path.join(os.getcwd(), project+'.Sufi2.SwatCup')
        print(project)
        d = input("Is that correct (y or n)? ")
        if d == 'y':
            if os.path.exists(project):
                self.project = project
            else:
                print('Please try again.')
                self.project = None
        else:
            print('Please try again.')
            self.project = None

    def get_mode(self):
        cv = input("Do you want to calibrate or validate (type 'c' for calibration or 'v' for validation)? ")
        if cv == 'c':
            self.direction = 'calib'
        elif cv == 'v':
            self.direction = 'valid'
        else:
            print('Please try again.')
            self.project = None

    def make_backups(self):
        from shutil import copyfile

        self.observed = os.path.join(self.project, 'SUFI2.IN', 'observed.txt')
        self.observed_bak = os.path.join(self.project, 'SUFI2.IN', 'observed.txt')+'.bak'
        if not os.path.exists(self.observed_bak):
            copyfile(self.observed, self.observed_bak)

        self.observed_rch = os.path.join(self.project, 'SUFI2.IN', 'observed_rch.txt')
        self.observed_rch_bak = os.path.join(self.project, 'SUFI2.IN', 'observed_rch.txt')+'.bak'
        if not os.path.exists(self.observed_rch_bak):
            copyfile(self.observed_rch, self.observed_rch_bak)

    def modify(self, bak, obs):
        reader = open(bak, mode='r')
        writer = open(obs, mode='w')

        flow = False
        modify = False

        for i in reader.readlines():
            # this detects the 
            # flow dataset
            if 'FLOW' in i:
                flow = True
            elif i == '\n':
                if flow == True:
                    modify = True
                    count = 1
                else:
                    modify = False

            # this detects the number
            # of points and calculates
            # the split
            if ('number of data points' in i)  & (flow == True):
                total = int(i.split(':')[0])
                valid = int(total*0.3)
                train = total-valid
                split = {'total':total, 'valid':valid, 'train':train}
                if self.direction == 'valid':
                    i = i.replace(str(total), str(valid))
                elif self.direction == 'calib':
                    i = i.replace(str(total), str(train))

            if modify == True:
                flow = False
                if not i == '\n':
                    if self.direction == 'valid':
                        if count > train:   # in case of validation
                            writer.write(i)
                    elif self.direction == 'calib':
                        if count <= train:   # in case of validation
                            writer.write(i)
                    count += 1
                    continue

            writer.write(i)

    def run(self):
        self.get_project()
        self.get_mode()
        if not self.project == None:
            self.make_backups()
            self.modify(bak=self.observed_bak, obs=self.observed)
            self.modify(bak=self.observed_rch_bak, obs=self.observed_rch)

alternate()
