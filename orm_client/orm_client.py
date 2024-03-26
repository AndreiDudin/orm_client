import uuid

import allure
import records
import structlog
from sqlalchemy import create_engine

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


class OrmClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def close_connection(self):
        self.db.close()

    def send_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        allure.attach(
            str(query.compile(compile_kwargs={"literal_binds": True})),
            name='ORM request',
            attachment_type=allure.attachment_type.TEXT
        )
        dataset = self.db.execute(statement=query)
        result = [row for row in dataset]
        log.msg(
            event='response',
            dataset=[dict(row) for row in result]
        )
        allure.attach(
            str(dataset),
            name='ORM response',
            attachment_type=allure.attachment_type.TEXT
        )
        return result

        # rows = db.query('select * from "public"."Users"')
        # for rows in rows.as_dict():
        #     print(rows)

    def send_bulk_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        allure.attach(
            str(query.compile(compile_kwargs={"literal_binds": True})),
            name='ORM request',
            attachment_type=allure.attachment_type.TEXT
        )
        self.db.execute(statement=query)
