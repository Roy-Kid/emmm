
import os
import subprocess
from mollab.plugins.input.IN_lmpdat import INlmpdat

class Polymerization:

    def __init__(self) -> None:
        # select polymerization type:
        # simple: just link two atoms
        # 
        self.polym_type = 'condensation'

        # only support one pair of linkers
        self.linker1type = ''
        self.linker2type = ''

        self.cutoff = 3

        self.invoke_lmps_cmd = 'mpirun -np 8 lmp'
        print(os.getcwd())
        os.chdir('./test/scripts')
        reader = INlmpdat()
        self.world = reader.read('data.lmps', {'atomStyle': 'full', 'bondStyle': 'harmonic', 'angleStyle': 'harmonic', 'dihedralStyle': 'opls', 'improperStyle': 'cvff', 'pairStyle': 'lj126'})
        self.atoms = self.world.atoms

    def _init(self):
        pass

    def _find_pair(self):

        linker1type = self.linker1type
        linker2type = self.linker2type

        linker1List = list()
        linker2List = list()

        # find linking atoms in system
        for atom in self.atoms:

            if atom.type == linker1type:
                linker1List.append(atom)
            elif atom.type == linker2type:
                linker2List.append(atom)

        # check bonding criteria for all pairs

        for linker1 in linker1List:

            for linker2 in linker2List:

                # Intra check
                # TODO: if define intra
                if linker1.molId == linker2.molId:
                    continue
                

                # Cutoff check
                # TODO: replace cutoff with variable
                distance = linker1.distance(linker2)
                if distance > self.cutoff:
                    continue

                # TODO: Alignment check

                # actual polymerization
                # simple mode: the concise way of condensation polymerization
                if self.polym_type == 'simple':
                    if linker1.distance(linker2) < self.cutoff:
                        linker1.add_linkedAtoms(linker2)



    def _final(self):
        pass


    def _energy_minimize(self):

        result = subprocess.run((self.invoke_lmps_cmd + '-in minimize.in').split(), shell=True)

        if result.returncode == 0:
            print('minimization perform successfully!')
        else:
            print(f'return code: {result.returncode}')

    def _isRelaxation(self, formedBondCount):
        if formedBondCount % 5 == 0:
            return True
        else:
            return False

    def _relaxation(self):
        print('start to relax system')
        result = subprocess.run((self.invoke_lmps_cmd + '-in relax.in').split(), shell=True)

        if result.returncode == 0:
            print('relaxation perform successfully!')
        else:
            print(f'return code: {result.returncode}')

    def _isRearrange(self, formedBondCount):
        if formedBondCount % 10 == 0:
            return True
        else:
            return False

    def _rearrange(self):
        print('start to rearrange system')
        result = subprocess.run((self.invoke_lmps_cmd + '-in rearrange.in').split(), shell=True)

        if result.returncode == 0:
            print('relaxation perform successfully!')
        else:
            print(f'return code: {result.returncode}')        

    def loop(self):

        formedBondCount = 0
        goalBondCount = 50

        attemptCount = 0
        max_attemptCount = 20

        print('polymerization start')
        print('initializing system...')
        self._init()
        print('initialization completed!')

        while formedBondCount < goalBondCount:

            print(f'current formed bond: ( {formedBondCount}/{goalBondCount} )')
            
            # if a pair of linkers reach the criteria
            # (link them) and return True
            # or return False to perform MD
            while not self._find_pair():
                print('attempt to find linker pair')
                print(f'attemption count: {attemptCount}')
                if attemptCount > max_attemptCount:
                    print("No pair was found within the maximum number of attempts.")
                    break # jump to finalize
                attemptCount += 1

                # perform a md to rearrangement structure

            print('perform energy minimization')
            self._energy_minimize()
            # perform MD to relaxation or rearrangement structure
            # set up how often to relaxation or rearrangement structure
            # here is a slot holder that you can add anything you want in a loop
            if self._isRelaxation(formedBondCount):
                self._relaxation()
            if self._isRearrange(formedBondCount):
                self._rearrange()

        print('finalizing system...')
        self._final()
        print('finalization completed!')

        print('polymerzation finished with safe and sound')
        print('GG & WP')

