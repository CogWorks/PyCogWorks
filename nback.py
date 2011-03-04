
class NBack(object):
    
    NBACK_NUMERIC = 0
    NBACK_ALPHA1 = 1
    NBACK_ALPHA2 = 2
    NBACK_ALPHA3 = 3
    

    def __init__(self, n=1, isi=4000, type=self.NB_ALPHA):
        super(NBack, self).__init__()
        
        self.n = n
        sefl.isi = isi
        self.type = type
        
    def _generate_stimuli_pool(self):
        
        pool = None
        
        if self.type == self.NBACK_NUMERIC:
            pool = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        elif self.type == self.NBACK_ALPHA1:
            pool = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            
        elif self.type == self.NBACK_ALPHA2:
            pool = ['b', 'c', 'd', 'g', 'j', 'k', 'l', 'm',
                    'n', 'p', 'r', 's', 't', 'x', 'y', 'z']            
        
        elif self.type == self.NBACK_ALPHA3:
            pool = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
            
        return pool
        
