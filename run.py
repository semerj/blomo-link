#!/usr/bin/env python
from app import app
import logging

#logger = logging.getLogger('werkzeug')
#handler = logging.FileHandler('access.log')
#logger.addHandler(handler)

app.run(debug=True)
