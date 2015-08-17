#!/usr/bin/env python

import os
import sys
# local
from app import create_app, db
from app.models import User, Role

#sys.path.append("lib/")

app = create_app('default')

if __name__ == '__main__':
    app.run()
    #app.run(host='10.0.1.5')
    
