from datetime import datetime
from message import Message
from db import Session, engine, Base

Base.metadata.create_all(engine)
session = Session()
test_message = Message("Just a test message", "Oscar",
                       "google1021", datetime.now())


session.add(test_message)
session.commit()
session.close()
