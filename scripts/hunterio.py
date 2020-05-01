from pyhunter import PyHunter
from settings import HUNTERIO_API_KEY

hunter = PyHunter(HUNTERIO_API_KEY)

if __name__ == '__main__':
    result = hunter.domain_search(domain='mandmpestcontrol.com', limit=10)
