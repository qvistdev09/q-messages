from datetime import datetime
from message import Message
from db import Session, engine, Base

Base.metadata.create_all(engine)
session = Session()
test_message = Message("I'm getting along with Flask and Python!", "qvistdev09",
                       "appcreator", datetime.now())


session.add(test_message)
session.commit()
session.close()
