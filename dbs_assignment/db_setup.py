from dbs_assignment.database import Base, engine
import dbs_assignment.models


Base.metadata.create_all(engine)
